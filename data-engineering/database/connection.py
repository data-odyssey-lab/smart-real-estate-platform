import psycopg2
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

def get_db_connection():
    try:
        connection = psycopg2.connect(
            database=os.getenv("SUPABASE_DB"),
            user=os.getenv("SUPABASE_USER"),
            password=os.getenv("SUPABASE_PASSWORD"),
            host=os.getenv("SUPABASE_HOST"),
            port=os.getenv("SUPABASE_PORT"),
            sslmode='require',
            options="-c statement_timeout=30000"
        )
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None