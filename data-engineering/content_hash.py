from database.connection import get_db_connection
from database.transform import generate_content_hash


def backfill_content_hash():
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT
                id,
                title,
                price_raw,
                location,
                bedrooms,
                bathrooms
            FROM property_listings
            WHERE content_hash IS NULL;
        """)

        rows = cur.fetchall()
        updated = 0

        for row in rows:
            listing = {
                "title": row[1],
                "price_raw": row[2],
                "location": row[3],
                "bedrooms": row[4],
                "bathrooms": row[5]
            }

            content_hash = generate_content_hash(listing)

            cur.execute("""
                UPDATE property_listings
                SET content_hash = %s
                WHERE id = %s;
            """, (content_hash, row[0]))

            updated += 1

        conn.commit()
        print(f"Updated {updated} rows.")

    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")

    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    backfill_content_hash()