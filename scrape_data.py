import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

visited_urls = set()
max_depth = 5


def scrape_website(url, depth=0):
    if depth > max_depth or url in visited_urls:
        return

    visited_urls.add(url)

    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"Failed to retrieve {url}. Status code: {response.status_code}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract and save text content
        text_content = soup.get_text(separator=' ', strip=True)
        with open('scraped_data.txt', 'a', encoding='utf-8') as file:
            file.write(f"URL: {url}\n{text_content}\n\n{'=' * 50}\n\n")

        print(f"Scraped content from {url} (Depth: {depth})")

        # Find and follow links
        base_url = "{0.scheme}://{0.netloc}".format(urlparse(url))
        for link in soup.find_all('a', href=True):
            next_url = urljoin(base_url, link['href'])
            if urlparse(next_url).netloc == urlparse(base_url).netloc:
                time.sleep(1)  # Be polite, wait between requests
                scrape_website(next_url, depth + 1)

    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")


# Example usage
start_url = "https://www.montclair.edu/"  # Replace with the actual URL you want to start scraping from
scrape_website(start_url)