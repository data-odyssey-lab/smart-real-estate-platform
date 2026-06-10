# imports
from bs4 import BeautifulSoup
import requests
import time
from urllib import request
from urllib.parse import urljoin
import csv

base_url = "https://www.property24.co.ke/property-for-sale-in-nairobi-c1890?page={page_number}"


# function to get the page content
def get_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retrieve page: {url}. Status code: {response.status_code}")
        return None

# function to safely extract text from an element, returning 'N/A' if the element is not found
def safe_get_text(element):
    return element.text.strip() if element else 'N/A'

all_listings = [] # list to store all the listings data
# opening a csv file to write the listings data, using 'utf-8' encoding to handle special characters
with open('property_listings.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Title', 'Price', 'Location', 'Address', 'Bedrooms', 'Bathrooms', 'Floor Size', 'Excerpt'])  # writing the header row
    for page_number in range(1, 6):  # Scrape the first 5 pages
        url = base_url.format(page_number=page_number)
        page_content = get_page(url)
        
        if page_content:
            soup = BeautifulSoup(page_content, 'html.parser')
            listings = soup.find_all('div', class_='p24_regularTile')
            print(f"Scraped page {page_number} with {len(listings)} listings.")

            # iterating through each listing
            for listing in listings:
                title = safe_get_text(listing.find('span', class_='p24_propertyTitle'))
                price = safe_get_text(listing.find('span', class_='p24_price'))
                location = safe_get_text(listing.find('span', class_='p24_location'))
                address = safe_get_text(listing.find('span', class_='p24_address'))
                bedrooms = safe_get_text(listing.find('span', title='Bedrooms'))
                bathrooms = safe_get_text(listing.find('span', title='Bathrooms'))
                floor_size = safe_get_text(listing.find('span', title='Floor Size'))
                excerpt = safe_get_text(listing.find('span', class_='p24_excerpt'))
                # url extraction with error handling
                a_tag = listing.find('a')
                url = a_tag['href'] if a_tag and a_tag.get('href') else None
                if url:
                    full_url = urljoin("https://www.property24.co.ke", url)
                else:
                    full_url = 'N/A'
                    
                # creating a dictionary to store the listing data
                listing_data = {
                    'title': title,
                    'price': price,
                    'location': location,
                    'address': address,
                    'bedrooms': bedrooms,
                    'bathrooms': bathrooms,
                    'floor_size': floor_size,
                    'excerpt': excerpt,
                    'link': full_url
                }

                # appending the listing data to the all_listings list
                all_listings.append(listing_data)
                # appending each row to the csv file
                writer.writerow(listing_data.values())
        else:
            print(f"Skipping page {page_number} due to retrieval failure.")
        # adding a delay to avoid overwhelming the server
        time.sleep(2)