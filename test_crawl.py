import unittest
from crawl import normalize_url

class TestCrawl(unittest.TestCase):
    def test_normalize_url_with_https(self):
        # Test cases for normalize_url function
        input_url = "https://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_with_http(self):
        input_url = "http://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_with_trailing_slash(self):
        input_url = "https://www.boot.dev/blog/path/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_capital(self):
        input_url = "https://WWW.BOOT.DEV/BLOG/PATH"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_with_port(self):
        input_url = "https://www.boot.dev:8080/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev:8080/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_with_subdomain(self):
        input_url = "https://subdomain.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "subdomain.boot.dev/blog/path"
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()


