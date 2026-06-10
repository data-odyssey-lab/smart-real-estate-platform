from connection import get_db_connection

CREATE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS property_listings (
    id SERIAL PRIMARY KEY,
    title TEXT,
    price TEXT,
    location TEXT,
    address TEXT,
    bedrooms TEXT,
    bathrooms TEXT,
    floor_size TEXT,
    excerpt TEXT,
    link TEXT UNIQUE,
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
        print(f"Error creating tables: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    create_tables()