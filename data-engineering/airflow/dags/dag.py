from datetime import datetime, timedelta
import json
import sys
from airflow import DAG
from airflow.operators.python import PythonOperator

# import your project functions
from scraper.property24scraper import scrape_property24
from scraper.buyrentkenya import scrape_buyrentkenya
from database.transform import clean_listings
from database.insert_data import insert_many_listings
from database.export_data import export_to_csv
# Default DAG arguments
default_args = {
    "owner": "warren",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}

RAW_PATH_P24 = "/tmp/listings_raw_property24.json"
RAW_PATH_BRK = "/tmp/listings_raw_buyrentkenya.json"
RAW_PATH = "/tmp/listings_raw.json"
CLEANED_PATH = "/tmp/listings_cleaned.json"

# Scrape property24 task
def scrape_property24_task(ti):
    listings = scrape_property24()

    if not listings:
        raise ValueError("No listings scraped from Property24")
    
    with open(RAW_PATH_P24, "w") as f:
        json.dump(listings, f)
    
    # return instead of xcom push
    print(f"Scraped {len(listings)} listings from Property24 and saved to {RAW_PATH_P24}")

# Scrape buyrentkenya task
def scrape_buyrentkenya_task(ti):
    listings = scrape_buyrentkenya()

    if not listings:
        raise ValueError("No listings scraped from BuyRentKenya")

    with open(RAW_PATH_BRK, "w") as f:
        json.dump(listings, f)

    print(f"Scraped {len(listings)} listings from BuyRentKenya and saved to {RAW_PATH_BRK}")

# merge task
def merge_task(ti):
    with open(RAW_PATH_P24) as f:
        p24_listings = json.load(f)

    with open(RAW_PATH_BRK) as f:
        brk_listings = json.load(f)

    all_listings = p24_listings + brk_listings

    with open(RAW_PATH, "w") as f:
        json.dump(all_listings, f)

    print(f"Merged {len(p24_listings)} Property24 listings and {len(brk_listings)} BuyRentKenya listings into {len(all_listings)} total listings. Saved to {RAW_PATH}")

# Transform task
def transform_task(ti):
    with open(RAW_PATH) as f:
        raw_listings = json.load(f)
    
    cleaned = clean_listings(raw_listings)

    with open(CLEANED_PATH, "w") as f:
        json.dump(cleaned, f)
    
    # return instead of xcom_push
    print(f"Transformed {len(cleaned)} listings. Saved to {CLEANED_PATH}")

# load task
def load_task(ti):
    with open(CLEANED_PATH) as f:
        listings = json.load(f)

    if not listings:
        raise ValueError("No cleaned listings to insert")

    insert_many_listings(listings)

# export task
def export_task(ti):
    export_to_csv()


# DAG defination
with DAG(
    dag_id="smart_real_estate_pipeline",
    default_args=default_args,
    description="Scrape Property24 and BuyRentKenya, transform, and load into PostgreSQL",
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["real_estate", "scraping", "postgres"],
) as dag:

    scrape_property24_op = PythonOperator(
        task_id="scrape_property24",
        python_callable=scrape_property24_task,
    )

    scrape_buyrentkenya_op = PythonOperator(
        task_id="scrape_buyrentkenya",
        python_callable=scrape_buyrentkenya_task,
    )

    merge_listings_op = PythonOperator(
        task_id="merge_listings",
        python_callable=merge_task,
    )

    transform_listings_op = PythonOperator(
        task_id="transform_listings",
        python_callable=transform_task,
    )

    load_listings_op = PythonOperator(
        task_id="load_listings",
        python_callable=load_task,
    )
    export_listings_op = PythonOperator(
        task_id = "export_listings",
        python_callable=export_task,
    )

    # pipeline order
    [scrape_property24_op, scrape_buyrentkenya_op] >> merge_listings_op >> transform_listings_op >> load_listings_op >> export_listings_op
    
    