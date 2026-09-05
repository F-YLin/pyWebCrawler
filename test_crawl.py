import unittest
from crawl import extract_page_data, get_heading_from_html, get_images_from_html, get_urls_from_html, normalize_url, get_first_paragraph_from_html

class TestCrawl(unittest.TestCase):
    # Test cases for normalize_url function
    def test_normalize_url_with_https(self):
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

    # Test cases for get_heading_from_html function
    def test_get_heading_from_html_basic(self):
        input_body = "<html><body><h1>Test Title</h1></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_h2_fallback(self):
        input_body = "<html><body><h2>Fallback Title</h2></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Fallback Title"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_no_heading(self):
        input_body = "<html><body><p>No heading here</p></body></html>"
        actual = get_heading_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    # Test cases for get_first_paragraph_from_html function
    def test_get_first_paragraph_from_html_main(self):
        input_body = """<html><body><p>Outside paragraph.</p>
            <main>
                <p>Inside main paragraph.</p>
            </main>
        </body></html>"""

        actual = get_first_paragraph_from_html(input_body)
        expected = "Outside paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_p(self):
        input_body = "<html><body><p>First paragraph.</p><p>Second paragraph.</p></body></html>"
        actual = get_first_paragraph_from_html(input_body)
        expected = "First paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_empty(self):
        input_body = "<html><body><div>No paragraphs here.</div></body></html>"
        actual = get_first_paragraph_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    # Test cases for get_urls_from_html function
    def test_get_urls_from_html(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_relative_url(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="/some-path">A link</a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/some-path"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_multiple_urls(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="/some-path">A link</a><a href="https://example.com">Another link</a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/some-path", "https://example.com"]
        self.assertEqual(actual, expected)

    # Test cases for get_images_from_html function
    def test_get_images_from_html(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/some-image.jpg" alt="Some image"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/some-image.jpg"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_multiple_images(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/some-image.jpg" alt="Some image"><img src="/another-image.png" alt="Another image"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/some-image.jpg", "https://crawler-test.com/another-image.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_empty(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><div>No images here.</div></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

    # Test cases for extract_page_data function
    def test_extract_page_data_basic(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h1>Test Heading</h1>
            <p>This is a test paragraph.</p>
            <a href="/some-path">A link</a>
            <img src="/some-image.jpg" alt="Some image">
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Heading",
            "first_paragraph": "This is a test paragraph.",
            "outgoing_links": ["https://crawler-test.com/some-path"],
            "images": ["https://crawler-test.com/some-image.jpg"]
        }
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()


