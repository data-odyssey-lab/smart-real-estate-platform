from datetime import datetime, timedelta
import sys
from airflow import DAG
from airflow.operators.python import PythonOperator

# import your project functions
from scraper.property24scraper import scrape_property24
from database.insert_data import insert_property_listing
# Default DAG arguments
default_args = {
    "owner": "warren",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}

# Scraping task
def scrape_task(ti):
    listings = scrape_property24()

    # Push data to XCom 
    ti.xcom_push(key="listings", value=listings)

# Load task
def load_task(ti):
    listings = ti.xcom_pull(key="listings", task_ids="scrape_property")

    if not listings:
        raise ValueError("No listings received from scraper")

    for listing in listings:
        insert_property_listing(listing)

# DAG definition
with DAG(
    dag_id="property24_pipeline",
    default_args=default_args,
    description="Scrape Property24 and load into PostgreSQL",
    schedule_interval="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["real_estate", "scraping", "postgres"],
) as dag:

    scrape_property = PythonOperator(
        task_id="scrape_property",
        python_callable=scrape_task,
    )

    load_property = PythonOperator(
        task_id="load_property",
        python_callable=load_task,
    )

    # pipeline order
    scrape_property >> load_property