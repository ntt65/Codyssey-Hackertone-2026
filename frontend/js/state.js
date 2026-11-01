/**
 * 대화·추천 상태. 새로고침해도 대화와 결과가 남도록 sessionStorage 에 보관해요.
 * (전체 대화 기록을 영구 저장하지 않아요. 탭을 닫으면 사라져요 — PRD H14)
 *
 * draft: 지금까지 정해진 조건 {startLocation, startQuery, date, startTime, endTime, category}
 * confirmed: 사용자가 확인한 조건 이름들 (바꾸려면 변경 전후 확인)
 * messages: 대화 [{role:'user'|'ai', text, cards?: string[], cardSnapshots?: object, note?}]
 * candidates: 지금까지 받은 후보 (id → 후보). 카드·상세·지도·저장이 같은 객체를 써요.
 * shown: 대화에 보여준 후보 id 순서 / pending: 확인 기다리는 변경 {field, before, after}
 */
/** Keep the original API available only when explicitly requested for compatibility. */
export const usesAgentV3 = new URLSearchParams(location.search).get('agent') !== 'legacy';

/** Create a local storage identifier; server conversation handles are issued separately. */
export function localId() {
  return globalThis.crypto?.randomUUID?.() || `${Date.now().toString(36)}-${Math.random().toString(36).slice(2)}-${Math.random().toString(36).slice(2)}`;
}

/** An anonymous browser namespace is not an authentication credential. */
function visitorNamespace() {
  try {
    const key = 'lab678_visitor_v3';
    let id = localStorage.getItem(key);
    if (!id || !/^[a-zA-Z0-9-]{12,100}$/.test(id)) { id = localId(); localStorage.setItem(key, id); }
    return id;
  } catch { return localId(); }
}

const visitorId = visitorNamespace();
const POINTER = `lab678_chat_v3:${visitorId}:active`;
let localConversation = localId();
try { localConversation = sessionStorage.getItem(POINTER) || localConversation; } catch { /* Memory remains usable. */ }
/** Select the tab's conversation namespace while retaining the original legacy store. */
const storageKey = () => usesAgentV3 ? `lab678_chat_v3:${visitorId}:${localConversation}` : 'lab678_chat';

const empty = () => ({
  draft: {},
  confirmed: [],
  revision: 0,
  messages: [],
  candidates: {},
  pool: [],
  shown: [],
  pending: null,
  pendingQueue: [],
  pendingApplied: false,
  lastRequest: null,
  poolContext: null,
  clarification: null,
  sourceCheckedAt: null,
  selectedCandidate: null, // 상세에서 열람하는 snapshot이며 선택이나 확정으로 취급하지 않아요.
  selectedContent: null, // 서버가 현재 표시 batch에서 확인한 임시 선택이에요.
  agent: { version: 3, conversation: null, domain: null, failedEvent: null, pendingRequest: null, pendingRestore: null },
  sound: false,
  mode: 'text',
});

function load() {
  try {
    const stored = JSON.parse(sessionStorage.getItem(storageKey()) || '{}');
    return { ...empty(), ...stored, agent: { ...empty().agent, ...(stored.agent || {}) } };
  } catch {
    return empty();
  }
}

export const state = load();

/** 지금 상태를 저장해요. 저장이 막혀도 화면은 계속 동작해요. */
export function save() {
  try {
    sessionStorage.setItem(storageKey(), JSON.stringify(state));
    if (usesAgentV3) sessionStorage.setItem(POINTER, localConversation);
  } catch { /* 무시 */ }
}

/** 새 대화로 비우기 */
export function resetChat() {
  const { sound, mode } = state;
  if (usesAgentV3) localConversation = localId();
  Object.assign(state, empty(), { sound, mode });
  save();
}

/** Fork a copied live tab without modifying the original tab's conversation. */
export function forkConversation() { resetChat(); }

/**
 * id 로 후보를 찾아요. 대화 카드·S04·S08 이 같은 객체를 써요. 저장한 장소도 찾아봐요.
 * @param {string} id
 */
export function candidateById(id) {
  return state.candidates[id] || null;
}
