from bs4 import BeautifulSoup
import requests
import time
from urllib.parse import urljoin

base_url = "https://www.property24.co.ke/property-for-sale-in-nairobi-c1890?page={page_number}"

def get_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retrieve page: {url}. Status code: {response.status_code}")
        return None

def safe_get_text(element):
    return element.text.strip() if element else 'N/A'

def scrape_property24(pages=5):
    all_listings = []

    for page_number in range(1, pages + 1):
        url = base_url.format(page_number=page_number)
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
                    'title': safe_get_text(listing.find('span', class_='p24_propertyTitle')),
                    'price': safe_get_text(listing.find('span', class_='p24_price')),
                    'location': safe_get_text(listing.find('span', class_='p24_location')),
                    'address': safe_get_text(listing.find('span', class_='p24_address')),
                    'bedrooms': safe_get_text(listing.find('span', title='Bedrooms')),
                    'bathrooms': safe_get_text(listing.find('span', title='Bathrooms')),
                    'floor_size': safe_get_text(listing.find('span', title='Floor Size')),
                    'excerpt': safe_get_text(listing.find('span', class_='p24_excerpt')),
                    'link': full_url
                }
                all_listings.append(listing_data)
        else:
            print(f"Skipping page {page_number} due to retrieval failure.")

        time.sleep(2)

    return all_listings
