from connection import get_db_connection

CREATE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS property_listings (
    id SERIAL PRIMARY KEY,
    
    -- Raw scraped fields(for tracability)
    title TEXT,
    price_raw TEXT,
    floor_size_raw TEXT,

    -- cleaned numeric fields(for ML and Analytics)
    price NUMERIC,
    bedrooms SMALLINT,
    bathrooms SMALLINT,
    floor_size NUMERIC,

    -- Location fields
    location TEXT,
    address TEXT,

    -- Other fields
    excerpt TEXT,
    link TEXT UNIQUE,

    -- Metadata
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

def create_tables():
    conn = None
    cur = None

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(CREATE_TABLE_QUERY)
        conn.commit()
        print("Tables created successfully.")
    except Exception as e:
        conn.rollback()
        raise
    finally:
        if cur: cur.close()
        if conn: conn.close()

if __name__ == "__main__":
    create_tables()