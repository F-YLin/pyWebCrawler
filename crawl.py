from asyncio import tasks
from types import TracebackType
from urllib.parse import urlsplit, urljoin
from bs4 import BeautifulSoup, Tag
from typing import TypedDict
import requests

import asyncio
import aiohttp

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

class AsyncCrawler:
    def __init__(self, base_url: str, max_concurrency: int, max_pages: int) -> None:
        self.base_url = base_url
        self.base_domain = urlsplit(base_url).netloc
        self.page_data: dict[str, PageData] = {}
        self.lock = asyncio.Lock()
        self.max_concurrency = 3
        self.semaphore = asyncio.Semaphore(self.max_concurrency)
        self.session: aiohttp.ClientSession | None = None
        self.max_concurrency = max_concurrency
        self.max_pages = max_pages
        self.should_stop = False
        self.all_tasks: set[asyncio.Task[None]] = set()

    async def __aenter__(self) -> "AsyncCrawler":
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(
            self, 
            exc_type: Type[BaseException] | None, 
            exc_val: BaseException | None, 
            exc_tb: Traceback | None,
    ) -> None:
        if self.session is not None:
            await self.session.close()

    async def add_page_visit(self, normalized_url: str) -> None:
        async with self.lock:
            if self.should_stop:
                return False
            if normalized_url in self.page_data:
                return False
            if len(self.page_data) >= self.max_pages:
                self.should_stop = True
                print("Reached maximum number of pages to crawl.")
                for task in self.all_tasks:
                    if not task.done():
                        task.cancel()
                return False
            return True

    # new updated method under async
    async def get_html(self, url:str) -> str | None:
        # implementation for fetching HTML content from a URL
        # uses a User-agent header so servers recognize the request
        # Raise an error for failed requests or non-HTML responses
        # returns the webpage's HTML content as a string
        if self.session is None:
            return None
        try:
            async with self.session.get(url) as response:

                if response.status > 399:
                    print(f"Error: HTTP {response.status} for {url}")
                    return None

                content_type = response.headers.get("content-type", "")
                if "text/html" not in content_type:
                    print(f"Error: Non-HTML content {content_type} for {url}")
                    return None

                return await response.text()
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    # new updated method under async 
    async def crawl_page(self, current_url: str) -> None:
        if self.should_stop:
            return

        normalized_url = normalize_url(current_url)

        is_new = await self.add_page_visit(normalized_url)
        if not is_new:
            return

        async with self.semaphore:
            print(
                f"Crawling {current_url} (Active: {self.max_concurrency - self.semaphore._value})"
            )
            html = await self.get_html(current_url)
            if html is None:
                return

            page_info = extract_page_data(html, current_url)
            async with self.lock:
                self.page_data[normalized_url] = page_info

            next_urls = get_urls_from_html(html, self.base_url)

        if self.should_stop:
            return

        tasks: list[asyncio.Task[None]] = []
        for next_url in next_urls:
            task = asyncio.create_task(self.crawl_page(next_url))
            tasks.append(task)
            self.all_tasks.add(task)

        if tasks:
            try:
                await asyncio.gather(*tasks, return_exceptions=True)
            finally:
                for task in tasks:
                    self.all_tasks.discard(task)

    async def crawl(self) -> dict[str, PageData]:
        await self.crawl_page(self.base_url)
        return self.page_data

async def crawl_site_async(
    base_url: str, max_concurrency: int, max_pages: int
) -> dict[str, PageData]:
    async with AsyncCrawler(base_url, max_concurrency, max_pages) as crawler:
        return await crawler.crawl()