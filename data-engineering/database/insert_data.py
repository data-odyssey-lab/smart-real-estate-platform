from database.connection import get_db_connection

INSERT_QUERY = """
INSERT INTO property_listings (
    title,
    price,
    location,
    address,
    bedrooms,
    bathrooms,
    floor_size,
    excerpt,
    link
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (link) DO NOTHING;
"""

def insert_property_listing(listing):
    conn = None
    cur = None

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            INSERT_QUERY, 
            (
                listing['title'],
                listing['price'],
                listing['location'],
                listing['address'],
                listing['bedrooms'],
                listing['bathrooms'],
                listing['floor_size'],
                listing['excerpt'],
                listing['link']
        )
    )
        conn.commit()

        print("Property listing inserted successfully.")
    except Exception as e:
        print(f"Error inserting property listing: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()