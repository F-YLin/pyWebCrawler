from urllib.parse import urlsplit
from bs4 import BeautifulSoup, Tag

def normalize_url(input_url: str) -> str:
    # Implementation for normalizing the URL
    # function should remove the scheme (http:// or https://) from the URL
    # and return the normalized URL in lowercase without trailing slashes
    parsed_url = urlsplit(input_url)
    netloc = parsed_url.netloc
    path = parsed_url.path.rstrip('/')
    output_url = f"{netloc}{path}"
    output_url = output_url.lower()
    return output_url

def get_heading_from_html(html: str) -> str:
    # Implementation for extracting heading from HTML
    # function should return the text content of the <h1> tag if present
    # or return the text content of <h2> tag as a fallback
    # Returns an empty string if neither an <h1> nor an <h2> tag is found
    soup = BeautifulSoup(html, 'html.parser')
    h1_tag = soup.find('h1')
    if h1_tag:
        return h1_tag.get_text(strip=True)
    h2_tag = soup.find('h2')
    if h2_tag:
        return h2_tag.get_text(strip=True)
    return ""

def get_first_paragraph_from_html(html: str) -> str:
    # Implementation for extracting the first paragraph from HTML
    # function should return the text content of the first <p> tag if present
    # Returns an empty string if no <p> tag is found
    soup = BeautifulSoup(html, 'html.parser')
    p_tag = soup.find('p')
    if p_tag:
        return p_tag.get_text(strip=True)
    return ""
