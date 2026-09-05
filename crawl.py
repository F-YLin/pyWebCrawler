from urllib.parse import urlsplit, urljoin
from bs4 import BeautifulSoup, Tag
from typing import TypedDict

class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list
    images: list

def normalize_url(input_url: str) -> str:
    # implementation for normalizing the URL
    # function should remove the scheme (http:// or https://) from the URL
    # and return the normalized URL in lowercase without trailing slashes
    parsed_url = urlsplit(input_url)
    netloc = parsed_url.netloc
    path = parsed_url.path.rstrip('/')
    output_url = f"{netloc}{path}"
    output_url = output_url.lower()
    return output_url

def get_heading_from_html(html: str) -> str:
    # implementation for extracting heading from HTML
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
    # implementation for extracting the first paragraph from HTML
    # function should return the text content of the first <p> tag if present
    # Returns an empty string if no <p> tag is found
    soup = BeautifulSoup(html, 'html.parser')
    p_tag = soup.find('p')
    if p_tag:
        return p_tag.get_text(strip=True)
    return ""

def get_urls_from_html(html: str, base_url: str) -> list:
    # implementation for extracting URLs from HTML
    # function should return un-normalized list of all the URLs found within the HTML
    # this function would later allow us to rewrite relative URLs to absolute URLs
    # parameter html is an HTML string
    # parameter base_url is the root URL of the target website
    soup = BeautifulSoup(html, 'html.parser')
    urls = []
    for tag in soup.find_all('a'):
        value = tag.get('href')
        if value:
            joined_url = urljoin(base_url, value)
            urls.append(joined_url)
    return urls

def get_images_from_html(html: str, base_url: str) -> list:
    # implementation for extracting image URLs from HTML
    # function should return a list of all the image URLs found within the HTML
    # parameter html is an HTML string
    # parameter base_url is the root URL of the target website
    soup = BeautifulSoup(html, 'html.parser')
    images = []
    for tag in soup.find_all('img'):
        value = tag.get('src')
        if value:
            joined_url = urljoin(base_url, value)
            images.append(joined_url)
    return images

def extract_page_data(html: str, page_url: str) -> PageData:
    # implementation for extracting all relevant data from HTML
    # function should return a dictionary containing the extracted data
    # with keys: url, heading, first_paragraph, outgoing_links, image_urls
    # parameter html is an HTML string
    # parameter page_url is the URL of the page being crawled
    return {
        "url": page_url,
        "heading": get_heading_from_html(html),
        "first_paragraph": get_first_paragraph_from_html(html),
        "outgoing_links": get_urls_from_html(html, page_url),
        "images": get_images_from_html(html, page_url)
    }