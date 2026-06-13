from datetime import datetime, timedelta
import json
import sys
from airflow import DAG
from airflow.operators.python import PythonOperator

# import your project functions
from scraper.property24scraper import scrape_property24
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

RAW_PATH = "/tmp/listings_raw.json"
CLEANED_PATH = "/tmp/listings_cleaned.json"

# Scraping task
def scrape_task(ti):
    listings = scrape_property24()

    if not listings:
        raise ValueError("No listings scraped from Property24")
    
    with open(RAW_PATH, "w") as f:
        json.dump(listings, f)
    
    # return instead of xcom push
    print(f"Scraped {len(listings)} listings and saved to {RAW_PATH}")

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
    dag_id="property24_pipeline",
    default_args=default_args,
    description="Scrape Property24, transform, and load into PostgreSQL",
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["real_estate", "scraping", "postgres"],
) as dag:

    scrape_property = PythonOperator(
        task_id="scrape_property",
        python_callable=scrape_task,
    )

    transform_property = PythonOperator(
        task_id="transform_property",
        python_callable=transform_task,
    )

    load_property = PythonOperator(
        task_id="load_property",
        python_callable=load_task,
    )
    export_property = PythonOperator(
        task_id = "export_property",
        python_callable=export_task,
    )

    # pipeline order
    scrape_property >> transform_property >> load_property >> export_property
    
    