from database.connection import get_db_connection

INSERT_QUERY = """
INSERT INTO property_listings (
    title,
    price_raw,
    price,
    price_flag,
    location,
    constituency,
    address,
    bedrooms,
    bathrooms,
    floor_size_raw,
    floor_size,
    floor_size_flag,
    excerpt,
    link
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )
ON CONFLICT (link) DO NOTHING; -- Ignore duplicates based on unique link constraint
"""

def insert_many_listings(listings):
    conn = None
    cur = None

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        values = [
            (
                i['title'],
                i['price_raw'],
                i['price'],
                i['price_flag'],
                i['location'],
                i['constituency'],
                i['address'],
                i['bedrooms'],
                i['bathrooms'],
                i['floor_size_raw'],
                i['floor_size'],
                i['floor_size_flag'],
                i['excerpt'],
                i['link'],
            )
            for i in listings
        ]
        cur.executemany(INSERT_QUERY, values)
        conn.commit()
        print(f"Successfully inserted {len(values)} property listings.")

    except Exception as e:
        if conn:
            conn.rollback()
        raise

    finally:
        if cur: cur.close()
        if conn: conn.close()