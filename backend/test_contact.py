import unittest

from contact import detail_code, event_contact, phones_from_page


class ContactTest(unittest.TestCase):
    def test_detail_code_only_for_culture_portal(self):
        self.assertEqual(detail_code("https://culture.seoul.go.kr/culture/culture/cultureEvent/view.do?cultcode=159930&menuNo=200008"), "159930")
        self.assertIsNone(detail_code("https://example.com/culture/culture/cultureEvent/view.do?cultcode=1"))
        self.assertIsNone(detail_code("https://culture.seoul.go.kr/other?cultcode=1"))
        self.assertIsNone(detail_code("https://culture.seoul.go.kr/culture/culture/cultureEvent/view.do?cultcode=abc"))

    def test_phones_from_first_inquiry(self):
        page = "<li><strong>문의</strong> 070-8680-8477 / 02-337-3103</li><a>홈페이지</a><footer>문의 02-2133-2538</footer>"
        self.assertEqual(phones_from_page(page), ["070-8680-8477", "02-337-3103"])

    def test_no_inquiry_means_no_phone(self):
        self.assertEqual(phones_from_page("<p>전화 없음</p>"), [])

    def test_rejects_other_urls(self):
        status, body = event_contact({"url": "https://evil.example/x"})
        self.assertEqual(status, 400)
        self.assertEqual(body["status"], "need_input")


if __name__ == "__main__":
    unittest.main()
