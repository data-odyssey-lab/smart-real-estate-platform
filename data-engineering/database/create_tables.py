from connection import get_db_connection

CREATE_RAW_SCHEMA_QUERY = """
    CREATE SCHEMA IF NOT EXISTS raw; 
"""
CREATE_RAW_LISTINGS_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS raw.raw_listings (
    raw_id      bigserial PRIMARY KEY,
    title       text,
    source      text NOT NULL,
    price_raw      text,
    location    text,
    constituency text,
    address     text,
    bedrooms    text,
    bathrooms   text,
    floor_size_raw  text,
    excerpt     text,
    link        text,
    scrape_date DATE NOT NULL DEFAULT CURRENT_DATE,
    content_hash TEXT UNIQUE,
    scraped_at  timestamptz NOT NULL DEFAULT now()
);
"""
CREATE_RAW_INDEX = """
CREATE INDEX IF NOT EXISTS ix_raw_listings_scrape_date
ON raw.raw_listings (scrape_date);
"""

def create_tables():
    conn = None
    cur = None

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(CREATE_RAW_SCHEMA_QUERY)
        cur.execute(CREATE_RAW_LISTINGS_TABLE_QUERY)
        cur.execute(CREATE_RAW_INDEX)
        conn.commit()
        print("Raw table created successfully.")
    except Exception as e:
        conn.rollback()
        raise
    finally:
        if cur: cur.close()
        if conn: conn.close()

if __name__ == "__main__":
    create_tables()