from scraper.property24scraper import scrape_property24
from database.transform import clean_listings
from database.insert_data import insert_many_listings

# Step 1 - Scrape
print("Scraping...")
raw_listings = scrape_property24(pages=1)
print(f"Scraped {len(raw_listings)} listings")
print("Sample raw:", raw_listings[0])

# Step 2 - Transform
print("\nTransforming...")
cleaned = clean_listings(raw_listings)
print(f"Cleaned {len(cleaned)} listings")
print("Sample cleaned:", cleaned[0])

# Step 3 - Load
print("\nLoading into PostgreSQL...")
insert_many_listings(cleaned)