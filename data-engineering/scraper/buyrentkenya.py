from bs4 import BeautifulSoup
import requests
import time
from urllib.parse import urljoin
from scraper.schema_normalizer import normalize_schema

base_url = "https://www.buyrentkenya.com/property-for-sale/nairobi"

headers = {
    "User-Agent": "Mozilla/5.0"
}

def build_url(page_number):
    if page_number == 1:
        return base_url
    else:
        return f"{base_url}?page={page_number}"

def get_page(url):
    session = requests.Session()
    session.headers.update(headers)
    response = session.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retrive page: {url}. Status code : {response.status_code}")

def safe_get_text(element):
    return element.text.strip() if element else 'N/A'

def scrape_buyrentkenya(pages=50):
    all_listings = []

    for page_number in range(1, pages + 1):
        url = build_url(page_number)
        print(f"Scraping page {page_number}: {url}")

        page_content = get_page(url)
        if page_content:
            soup = BeautifulSoup(page_content, 'html.parser')
            listings = soup.find_all('div', class_='listing-card relative mb-5 w-full md:mx-0 md:min-h-56')
            print(f"Scraped page with {len(listings)} listings.")

            for listing in listings:
                rooms = listing.find_all('span', class_='whitespace-nowrap')
                a_tag = listing.find('a', class_='absolute left-0 top-0 z-10 h-full w-full')
                href = a_tag['href'] if a_tag and a_tag.get('href') else None
                full_url = urljoin(url, href) if href else 'N/A'

                listing_data = {
                    'source': 'buyrentkenya',
                    'title': safe_get_text(listing.find('h2', class_='font-semibold md:hidden')),
                    'price': safe_get_text(listing.find('a', class_='pointer-events-none z-10 no-underline')),
                    'location': safe_get_text(listing.find('p', class_='w-full truncate font-normal capitalize')),
                    'bedrooms': safe_get_text(rooms[0]) if len(rooms) > 0 else None,
                    'bathrooms': safe_get_text(rooms[1]) if len(rooms) > 1 else None,
                    'link': full_url
                }
                all_listings.append(normalize_schema(listing_data))
        else:
            print(f"Skipping page {page_number} due to retrieval failure.")

    return all_listings