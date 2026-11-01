/** Canonical agent transport and tab lease, independent of chat rendering and speech. */
import { state, save, localId, forkConversation } from './state.js';
import { requestAgent, releaseAgentConnection } from './api.js';

const documentId = localId();
let generation = 0;
let opening = null;
let heartbeat = null;
let request = null;
let snapshotListener = () => {};
let forkListener = () => {};

/** Connect existing views to canonical snapshots without importing their renderer. */
export function configureAgent({ onSnapshot, onFork }) {
  snapshotListener = onSnapshot;
  forkListener = onFork;
}

/** Whether this document currently owns the verified writer connection. */
export function agentConnected() { return state.agent.conversation?.document_id === documentId && !!heartbeat; }

/** Return the current revision, lease and sequence with a fresh idempotency identifier. */
function envelope() {
  const meta = state.agent.conversation || {};
  return { conversation_id: meta.conversation_id, epoch: meta.epoch, document_id: documentId,
    lease_generation: meta.lease_generation, expected_revision: meta.revision,
    turn_seq: meta.next_turn_seq, turn_id: localId() };
}

/** Commit a complete server snapshot; UI fields are projected only by the registered view. */
function apply(response) {
  if (response.conversation) state.agent.conversation = response.conversation;
  if (response.state) state.agent.domain = response.state;
  snapshotListener(response);
  save();
}

/** Restore user claims only; cached coordinates, verification and tool facts are never imported. */
function restoreSnapshot(previous) {
  const conditions = { ...(previous.conditions || {}) };
  if (conditions.start_location) conditions.start_location = { label: conditions.start_location.label };
  return { understanding: { goal: previous.understanding?.goal, service: previous.understanding?.service,
    preferences: (previous.understanding?.preferences || []).map(({ id, dimension, value, polarity, strength, scope }) => ({ id, dimension, value, polarity, strength, scope })) },
  conditions, hypotheses: (previous.hypotheses || []).filter((item) => item.strength === 'hard')
    .map(({ id, field, value, strength, status }) => ({ id, field, value, strength, status })), active_question: previous.active_question };
}

/** Reconnect reloads, fork copied live tabs, and recover expired conversations as unverified claims. */
export async function ensureAgent() {
  if (state.agent.conversation?.document_id === documentId && heartbeat && !state.agent.pendingRestore) return true;
  if (opening) return opening;
  const mine = generation;
  const task = (async () => {
    const previous = state.agent.pendingRestore || state.agent.domain;
    const handle = envelope();
    const reloading = performance.getEntriesByType('navigation')[0]?.type === 'reload';
    const mode = reloading && handle.conversation_id ? 'resume' : 'open';
    let response = await requestAgent({ ...handle, event: { type: 'open', mode } });
    if (response.code === 'lease_busy' && mode === 'resume') {
      await new Promise((resolve) => setTimeout(resolve, Math.min(10000, Math.max(100, (response.data?.retry_after_seconds || 1) * 1000 + 50))));
      if (mine !== generation) return false;
      response = await requestAgent({ ...handle, event: { type: 'open', mode } });
    }
    if (mine !== generation) return false;
    let restore = !!state.agent.pendingRestore;
    if (['conversation_expired', 'epoch_mismatch', 'conversation_not_found', 'invalid_conversation'].includes(response.code)) {
      response = await requestAgent({ document_id: documentId, event: { type: 'open' } });
      restore = !!previous;
    }
    if (mine !== generation) return false;
    if (response.kind !== 'ok') throw new Error(response.message);
    if (response.data.forked) { forkConversation(); restore = false; forkListener(); }
    apply(response.data);
    clearInterval(heartbeat);
    heartbeat = setInterval(async () => {
      if (!state.agent.conversation) return;
      const atCall = generation;
      const result = await requestAgent({ ...envelope(), event: { type: 'heartbeat' } });
      if (atCall !== generation) return;
      const meta = result.data?.conversation;
      if (result.kind === 'ok' && meta?.conversation_id === state.agent.conversation?.conversation_id
          && meta.revision >= (state.agent.conversation?.revision || 0)) { state.agent.conversation = meta; save(); }
      else if ([409, 410].includes(result.status)) { clearInterval(heartbeat); heartbeat = null; }
    }, 5000);
    if (restore) {
      const snapshot = restoreSnapshot(previous);
      const restored = await requestAgent({ ...envelope(), event: { type: 'restore', snapshot } });
      if (mine !== generation) return false;
      if (restored.kind !== 'ok') {
        state.agent.pendingRestore = snapshot;
        apply({ state: previous, conversation: restored.data?.conversation || state.agent.conversation });
        throw new Error(restored.message);
      }
      apply(restored.data);
      state.agent.pendingRestore = null;
      save();
    }
    return true;
  })();
  opening = task;
  try { return await task; } finally { if (opening === task) opening = null; }
}

/** Send one event with retry-safe identity and discard every response from a replaced conversation. */
export async function sendAgent(event) {
  const mine = generation;
  if (!await ensureAgent() || mine !== generation) return null;
  request = new AbortController();
  const previous = state.agent.pendingRequest;
  const payload = previous && previous.document_id === documentId && JSON.stringify(previous.event) === JSON.stringify(event)
    ? previous : { ...envelope(), event };
  state.agent.pendingRequest = payload;
  save();
  const result = await requestAgent(payload, request.signal);
  if (mine !== generation) return null;
  if (result.status && result.code !== 'turn_in_progress') state.agent.pendingRequest = null;
  if (result.data?.state || result.data?.conversation) apply(result.data);
  state.agent.failedEvent = result.kind === 'ok' ? null : result.data?.state?.last_tool_action?.failed
    ? { type: 'retry_tool', action_id: result.data.state.last_tool_action.id }
    : result.data?.state?.failed_event || (!result.data?.state ? event : null);
  request = null;
  save();
  return result;
}

/** Stop pending work before reset/unload; server leases also fence a lost release request. */
export function releaseAgent() {
  ++generation;
  request?.abort(); request = null; opening = null;
  clearInterval(heartbeat); heartbeat = null;
  if (state.agent.conversation) releaseAgentConnection({ ...envelope(), event: { type: 'release' } });
}
