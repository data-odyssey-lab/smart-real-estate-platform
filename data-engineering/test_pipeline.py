from scraper.property24scraper import scrape_property24
from scraper.buyrentkenya import scrape_buyrentkenya
from database.transform import clean_listings
from database.insert_data import insert_many_listings

# Step 1 - Scrape
print("Scraping Property24...")
raw_listings = scrape_property24(pages=1)
print(f"Scraped {len(raw_listings)} listings")
print("Sample raw:", raw_listings[0])

print("Scraping BuyRentKenya...")
brk_listings = scrape_buyrentkenya(pages=1)
print(f"Scraped {len(brk_listings)} listings")
print("Sample raw:", brk_listings[0])

combined_listings = raw_listings + brk_listings
print(f"Total combined listings: {len(combined_listings)}")

# Step 2 - Transform
print("\nTransforming...")
cleaned = clean_listings(combined_listings)
print(f"Cleaned {len(cleaned)} listings")
print("Sample cleaned:", cleaned[0])

# Step 3 - Load
print("\nLoading into PostgreSQL...")
insert_many_listings(cleaned)