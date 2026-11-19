from database.connection import get_db_connection

INSERT_QUERY = """
INSERT INTO raw.raw_listings (
    title,
    source,
    price_raw,
    region,
    location,
    constituency,
    address,
    bedrooms,
    bathrooms,
    floor_size_raw,
    excerpt,
    link,
    source_listing_id,
    content_hash
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT(content_hash) DO NOTHING; -- Ignore duplicates
"""

def insert_many_listings(listings, batch_size=500):
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        for i in range(0, len(listings), batch_size):
            batch = listings[i:i + batch_size]
            values = [(l['title'],
                       l['source'],
                       l['price_raw'],
                    #    l['price'],
                    #    l['price_flag'],
                       l['region'],
                       l['location'],
                       l['constituency'],
                       l['address'],
                       l['bedrooms'],
                       l['bathrooms'],
                       l['floor_size_raw'],
                    #    l['floor_size'],
                    #    l['floor_size_flag'],
                       l['excerpt'],
                       l['link'],
                       l['source_listing_id'],
                       l['content_hash']
                       ) for l in batch
                       ]
            cur.executemany(INSERT_QUERY, values)
            conn.commit()
            print(f"Inserted batch {i//batch_size + 1} ({len(batch)} listings)")

    except Exception as e:
        if conn:
            conn.rollback()
        raise
    finally:
        if cur: cur.close()
        if conn: conn.close()