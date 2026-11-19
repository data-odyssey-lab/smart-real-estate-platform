from bs4 import BeautifulSoup
import requests
import time
from urllib.parse import urljoin
from scraper.schema_normalizer import normalize_schema

base_url = "https://www.property24.co.ke/property-for-sale-in-{region}-c{region_code}?page={page_number}"

headers = {
    "User-Agent": "Mozilla/5.0"
}

regions = {
    'nairobi': 1890,
    'thika': 1850,
    'kiambu': 1851,
    'kikuyu': 1847,
    'juja': 1846,
    'ruiru': 1849,
    'kitengela': 1871
}

def get_page(url):
    session = requests.Session()
    session.headers.update(headers)
    response = session.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retrieve page: {url}. Status code: {response.status_code}")
        return None

def safe_get_text(element):
    return element.text.strip() if element else 'N/A'

def scrape_property24(pages=50):
    all_listings = []

    for region_name, region_code in regions.items():
        print(f"\nScraping region: {region_name} (c{region_code})")

        for page_number in range(1, pages + 1):
            url = base_url.format(
                region = region_name,
                region_code = region_code, 
                page_number=page_number)
            page_content = get_page(url)

            if page_content:
                soup = BeautifulSoup(page_content, 'html.parser')
                listings = soup.find_all('div', class_='p24_regularTile')
                print(f"Scraped page {page_number} with {len(listings)} listings.")

                for listing in listings:
                    a_tag = listing.find('a')
                    href = a_tag['href'] if a_tag and a_tag.get('href') else None
                    full_url = urljoin("https://www.property24.co.ke", href) if href else 'N/A'

                    listing_data = {
                        'source': 'property24',
                        'title': safe_get_text(listing.find('span', class_='p24_propertyTitle')),
                        'price': safe_get_text(listing.find('span', class_='p24_price')),
                        'region': region_name,
                        'location': safe_get_text(listing.find('span', class_='p24_location')),
                        'address': safe_get_text(listing.find('span', class_='p24_address')),
                        'bedrooms': safe_get_text(listing.find('span', title='Bedrooms')),
                        'bathrooms': safe_get_text(listing.find('span', title='Bathrooms')),
                        'floor_size': safe_get_text(listing.find('span', title='Floor Size')),
                        'excerpt': safe_get_text(listing.find('span', class_='p24_excerpt')),
                        'link': full_url
                    }
                    all_listings.append(normalize_schema(listing_data))
            else:
                print(f"Skipping page {page_number} due to retrieval failure.")

            time.sleep(2)

    return all_listings
