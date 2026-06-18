import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

def export_to_csv():
    conn = psycopg2.connect(
        dbname=os.getenv("SUPABASE_DB"),
        user=os.getenv("SUPABASE_USER"),
        password=os.getenv("SUPABASE_PASSWORD"),
        host=os.getenv("SUPABASE_HOST"),
        port=os.getenv("SUPABASE_PORT")
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM property_listings")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()

    df = pd.DataFrame(rows, columns=columns)

    filename = f"property_listings_{datetime.today().strftime('%Y-%m-%d')}.csv"
    filepath = f"/opt/airflow/exports/{filename}"

    df.to_csv(filepath, index=False)
    print(f"Exported {len(df)} listings to {filepath}")

if __name__ == "__main__":
    export_to_csv()