# Data Dictionary — Smart Real Estate Analytics Platform

**Team:** Data Engineering
**Version:** V1
**Last Updated:** June 2026
**Database:** PostgreSQL (`real_estate_db`)
**Geographic Scope:** Nairobi County, Kenya

---

## Overview

This document describes all data assets produced and maintained by the Data Engineering team. It is the primary reference for the Analytics and ML teams when consuming data from the platform.

---

## Table: `property_listings`

The core table of the platform. Each row represents a single property listing scraped from Property24 Kenya.

**Source:** [property24.co.ke](https://www.property24.co.ke)
**Update Frequency:** Daily (via Airflow DAG `property24_pipeline`)
**Primary Key:** `id`
**Deduplication Key:** `link` (unique constraint)

---

### Column Definitions

| Column | Data Type | Nullable | Description | Example |
|---|---|---|---|---|
| `id` | SERIAL | No | Auto-incrementing unique identifier for each listing | `1`, `2`, `3` |
| `title` | TEXT | Yes | Property listing title as scraped | `"3 Bedroom Apartment / Flat"` |
| `price_raw` | TEXT | Yes | Original price string as scraped, preserved for traceability | `"KSh 15,000,000"` |
| `price` | NUMERIC | Yes | Cleaned numeric price in Kenyan Shillings (KES) | `15000000` |
| `location` | TEXT | Yes | Neighborhood or area name | `"Westlands"`, `"Kilimani"` |
| `address` | TEXT | Yes | Full address string as scraped | `"Westlands, Westlands, Nairobi"` |
| `bedrooms` | SMALLINT | Yes | Number of bedrooms | `1`, `2`, `3`, `4` |
| `bathrooms` | SMALLINT | Yes | Number of bathrooms | `1`, `2`, `3` |
| `floor_size_raw` | TEXT | Yes | Original floor size string as scraped, preserved for traceability | `"120 m²"` |
| `floor_size` | NUMERIC | Yes | Cleaned numeric floor size in square metres (m²) | `120.0` |
| `excerpt` | TEXT | Yes | Short property description from the listing | `"Newly built apartment in the heart of..."` |
| `link` | TEXT | No | Full URL to the original listing page. Used as deduplication key | `"https://www.property24.co.ke/..."` |
| `scraped_at` | TIMESTAMP | No | Timestamp of when the record was inserted. Defaults to current time | `2026-06-11 10:12:09` |

---

### Notes on Key Fields

**`price` vs `price_raw`**
The raw string (`price_raw`) is kept for traceability — so you can always audit what was originally on the website. The cleaned numeric field (`price`) is what should be used for analysis and modelling. If `price` is NULL, the raw string could not be parsed to a number.

**`floor_size` vs `floor_size_raw`**
Same pattern as price. Use `floor_size` for analysis. `floor_size_raw` is the audit trail.

**`location` field**
Currently stores the neighborhood name as scraped (e.g. `"Westlands"`, `"Kilimani"`). Neighborhood granularity normalization (estate → neighborhood → constituency hierarchy) is a pending cross-team decision. Do not use this field for constituency-level aggregations until normalization is confirmed.

**`bedrooms` and `bathrooms`**
Stored as SMALLINT. Values are cleaned from strings (e.g. `"3"` → `3`). NULL means the value was missing or unparseable from the listing.

**`scraped_at`**
This is the ingestion timestamp, not the listing publication date. Property24 does not expose listing dates in the scraped fields in V1.

---

## Data Quality Standards

| Metric | Target | Notes |
|---|---|---|
| Duplicate listings | 0% | Enforced via UNIQUE constraint on `link` |
| Price validity | > 90% non-null | Some listings don't display price |
| Bedrooms validity | > 85% non-null | Some listings omit bedroom count |
| Floor size validity | > 80% non-null | Floor size is frequently missing |
| Location validity | > 99% non-null | Always present in scraped data |

---

## Known Limitations (V1)

| Limitation | Impact | Planned Resolution |
|---|---|---|
| No historical price data | Cannot do time-series forecasting or trend analysis | Future V2 — archive daily snapshots |
| Single data source (Property24 only) | Limited coverage of Nairobi listings | BuyRentKenya scraper in progress |
| Location not normalized | Cannot reliably aggregate at contituency level | Pending cross-team decision on granularity |
| No listing publication date | Cannot determine how fresh a listing is | Under investigation |
| No property type classification | Cannot filter by apartment vs house vs land | To be derived from `title` field in feature engineering |

---

## How to Access the Data

### Option 1 — CSV Export
A CSV export of the latest dataset is published to the `/data-engineering/exports/` folder in the shared repository after each daily pipeline run.

File naming convention:
```
property_listings_YYYY-MM-DD.csv
```

### Option 2 — Read-Only Database Access
A read-only database user is available for direct PostgreSQL access via DBeaver or pandas.

```
Host:     <to be shared via secure channel>
Port:     5433
Database: real_estate_db
User:     analyst
Password: <to be shared via secure channel>
```

Permissions: `SELECT` only on all tables in the `public` schema.

### Option 3 — Python (pandas)
```python
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://analyst:<password>@<host>:5432/real_estate_db")
df = pd.read_sql("SELECT * FROM property_listings", engine)
```

---

## Sample Queries

### Count total listings
```sql
SELECT COUNT(*) FROM property_listings;
```

### Listings by neighborhood
```sql
SELECT location, COUNT(*) as listing_count
FROM property_listings
GROUP BY location
ORDER BY listing_count DESC;
```

### Average price by neighborhood
```sql
SELECT location,
       ROUND(AVG(price)) as avg_price,
       COUNT(*) as listing_count
FROM property_listings
WHERE price IS NOT NULL
GROUP BY location
ORDER BY avg_price DESC;
```

### Price distribution by bedrooms
```sql
SELECT bedrooms,
       ROUND(AVG(price)) as avg_price,
       ROUND(MIN(price)) as min_price,
       ROUND(MAX(price)) as max_price,
       COUNT(*) as count
FROM property_listings
WHERE price IS NOT NULL AND bedrooms IS NOT NULL
GROUP BY bedrooms
ORDER BY bedrooms;
```

### Listings with missing price (for data quality monitoring)
```sql
SELECT COUNT(*) as missing_price
FROM property_listings
WHERE price IS NULL;
```

---

## Changelog

| Version | Date | Author | Changes |
|---|---|---|---|
| V1.0 | June 2026 | Warren Otieno | Initial schema and dictionary — Property24 source |

---

*Data Dictionary | Smart Real Estate Analytics Platform | Data Engineering Team | 2026*
