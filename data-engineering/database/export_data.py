import pandas as pd
from connection import get_db_connection
from pathlib import Path
from datetime import datetime

def export_to_csv():
    conn = get_db_connection()
    
    df = pd.read_sql("SELECT * FROM property_listings", conn)
    conn.close()

    export_dir = Path(__file__).resolve().parent.parent / "exports"
    export_dir.mkdir(exist_ok=True)

    filename = f"property_listings_{datetime.today().strftime('%Y-%m-%d')}.csv"
    filepath = export_dir / filename

    df.to_csv(filepath, index=False)
    print(f"Exported {len(df)} listings to {filepath}")

if __name__ == "__main__":
    export_to_csv()