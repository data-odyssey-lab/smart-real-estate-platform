# Data Engineering Team — Smart Real Estate Analytics Platform

## Overview

The Data Engineering team is responsible for building and maintaining the data infrastructure that powers the Smart Real Estate Analytics Platform.

This includes collecting raw real estate data, transforming it into structured and reliable datasets, and delivering analytics-ready and ML-ready data to downstream teams.

This team forms the foundation of the platform by ensuring data is accurate, consistent, traceable, and accessible.

---

## Quick Start

### Prerequisites
- Python 3.10+
- Docker & Docker Compose
- Git
- Access to Supabase credentials (request from DE team lead)

### Setup

```bash
# Clone the repository
git clone git@github.com:data-odyssey-lab/smart-real-estate-platform.git
cd smart-real-estate-platform/data-engineering

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your Supabase credentials (request from DE lead)
```

### Running the Pipeline Locally

```bash
# Test the pipeline locally (1 page scrape)
python3 test_pipeline.py

# Start Airflow (full pipeline)
cd airflow
docker compose up -d

# Trigger the DAG manually
docker compose exec airflow-webserver airflow dags trigger smart_real_estate_pipeline
```

### Environment Variables

```
SUPABASE_DB=postgres
SUPABASE_USER=postgres.your_project_ref
SUPABASE_PASSWORD=your_password
SUPABASE_HOST=db.your_project_ref.supabase.co
SUPABASE_PORT=5432
```

---

## Core Responsibilities

### 1. Data Collection and Ingestion

* Identify and integrate real estate data sources
* Implement web scraping pipelines for property listing platforms
* Ensure reliable, scalable, and repeatable data extraction processes

### 2. Web Scraping and Data Acquisition

* Develop and maintain scrapers for multiple property websites
* Handle pagination, dynamic content, and anti-bot mechanisms
* Normalize raw scraped data into a unified schema across sources

### 3. ETL / ELT Pipeline Development

* Design and implement data pipelines for processing raw data
* Transform raw listings into clean, standardized datasets
* Detect and flag outliers in price and floor size fields
* Support batch data processing workflows

### 4. Database Design and Management

* Design and maintain relational database schemas (PostgreSQL)
* Manage schema migrations and versioning
* Provision and manage read-only roles for Analytics and ML teams
* Cloud-hosted on Supabase PostgreSQL

### 5. Data Quality Validation

* Define and implement validation rules for incoming and processed data
* Detect missing values, duplicates, inconsistencies, and anomalies
* Flag outliers with traceable raw-field pairs (price_raw / price, floor_size_raw / floor_size)
* Enforce schema integrity and data consistency standards

### 6. Workflow Orchestration

* Build and maintain Airflow DAGs for automated workflows
* Schedule scraping, ETL, and data publishing jobs
* Monitor pipeline execution, failures, and retries

---

## Project Scope (V1)

### Geographic Coverage (Property24)

* Nairobi County (initial focus) — constituency-level granularity confirmed
* Kiambu 
* Thika
* Kikuyu
* Juja
* Ruiru
* Kitengela

Future Expansion:

* Rongai
* Machakos
* Kajiado

For Buyrentkenya, only listings from Nairobi are scraped. Geographical expansion is underway.

---

## What's Been Built (Current State)

### Data Sources
| Source | Status | Pages/Run | Est. Listings/Run |
|---|---|---|---|
| Property24 Kenya | ✅ Live | 50 | ~1,050 |
| BuyRentKenya | ✅ Live | 50 | ~300 |

### Pipeline
| Stage | Status | Notes |
|---|---|---|
| Scraping | ✅ Done | Both sources, paginated, schema normalized |
| Transform | ✅ Done | Price cleaning, floor size cleaning, outlier flagging |
| Location Normalization | ✅ Done | 31 locations mapped to Nairobi constituencies |
| Load | ✅ Done | Supabase PostgreSQL, deduplication via UNIQUE constraint |
| Export | ✅ Done | Daily CSV export to `airflow/exports/` |
| Orchestration | ✅ Done | Airflow DAG running daily (`smart_real_estate_pipeline`) |

### Database
| Item | Detail |
|---|---|
| Host | Supabase PostgreSQL (cloud-hosted) |
| Table | `property_listings` |
| Total listings | ~8,700+ (as of July 2026) |
| Read-only roles | Provisioned for Analytics and ML teams |

---

## Deliverables

### 1. Data Source Identification ✅
* Property24 Kenya and BuyRentKenya identified and integrated
* Both scraped via Python (BeautifulSoup, Requests)
* Daily update frequency via Airflow scheduler

### 2. Database Schema ✅
* PostgreSQL schema with typed columns
* Core table: `property_listings`
* Raw-field traceability pairs for price and floor size
* Constituency field for location normalization
* Outlier flag columns (`price_flag`, `floor_size_flag`)
* Source column for per-source data quality tracking

### 3. Data Ingestion Pipeline ✅
* End-to-end pipeline: scrape → transform → load → export
* Schema normalization across sources via `schema_normalizer.py`
* Modular design — adding a new source requires only a scraper module and schema mapping

### 4. Data Architecture Documentation ✅
* Data dictionary available in `docs/data_dictionary.md`
* Pipeline design documented in `docs/`
* Source inventory documented in `docs/data_dictionary.md`

---

## ML Team Data Requirements (Confirmed Contracts)

### 1. Confirmed ML Requirements

| Requirement | Status | Notes |
|---|---|---|
| Geographic scope | ✅ Confirmed | Nairobi (V1), future multi-city expansion planned |
| Required property features | ✅ Confirmed | price, location, bedrooms, bathrooms, floor size, description |
| Historical price data | ⚠️ Not Available | Limits time-series forecasting in V1. Daily snapshots planned for V2 |
| Neighborhood granularity | ✅ Confirmed | Constituency level |

### 2. Open ML / Cross-Team Questions

| Question | Depends On | Status |
|---|---|---|
| Investment outcome labels for Stage 2 | ML + Analytics + DE | Pending |
| Listings outside Nairobi (Mavoko constituency) | DE + ML | Pending — decision on inclusion/exclusion |

### 3. Data Engineering Interpretation of ML Requirements

Based on ML inputs, Data Engineering has ensured:

- A standardized property schema supporting all required features across two sources
- Constituency-level location normalization (31 Nairobi estate locations mapped)
- Outlier detection and flagging for price (< KSh 500K) and floor size (< 10m² or > 2,000m²)
- Source tracking — every listing tagged `property24` or `buyrentkenya`
- Dataset structure compatible with:
  - Regression models (Stage 1 price prediction)
  - Scoring/classification models (Stage 2 investment analysis)

---

## Folder Structure

```text
data-engineering/

.
├── README.md
├── airflow
│   ├── config
│   ├── dags
│   ├── docker-compose.yaml
│   ├── dump.sql
│   ├── exports
│   ├── init-db
│   ├── logs
│   └── plugins
├── database
│   ├── __init__.py
│   ├── __pycache__
│   ├── connection.py
│   ├── create_tables.py
│   ├── export_data.py
│   ├── insert_data.py
│   ├── location_normalizer.py
│   └── transform.py
├── docs
│   ├── data_dictionary.md
│   └── images
├── notebooks
│   └── EDA.ipynb
├── requirements.txt
├── scraper
│   ├── __init__.py
│   ├── __pycache__
│   ├── buyrentkenya.py
│   ├── property24scraper.py
│   └── schema_normalizer.py
└── tests
    └── test_pipeline.py
```

---

## Data Flow Overview

```
Property24 + BuyRentKenya
        ↓
   scrape_task (paginated, 50 pages per source)
        ↓
   /tmp/listings_raw.json
        ↓
   transform_task (clean, normalize, flag outliers, map constituencies)
        ↓
   /tmp/listings_cleaned.json
        ↓
   load_task (insert to Supabase, ON CONFLICT DO NOTHING)
        ↓
   export_task (CSV to airflow/exports/)
        ↓
   Supabase PostgreSQL + CSV exports
   (consumed by Analytics and ML teams)
```

---

## Dependencies on Other Teams

| Dependency | Team | Status |
|---|---|---|
| Investment scoring inputs | Analytics Team | Pending |
| Reporting metrics definitions | Analytics Team | Pending |
| Model retraining feedback | ML Team | Ongoing — outlier ranges confirmed |

---

## Success Metrics

| Metric | Target | Current Status |
|---|---|---|
| Automated daily ingestion | ✅ | Running via Airflow |
| Data validity after cleaning | > 95% | Price > 99%, Location 100% |
| Duplication rate | 0% | Enforced via UNIQUE constraint on `link` |
| Schema consistency across sources | ✅ | Enforced via `schema_normalizer.py` |
| ML-ready dataset delivery | ✅ | Supabase access + daily CSV export |
| Analytics-ready dataset delivery | ✅ | Supabase access + daily CSV export |

---

## Branch Naming Convention

```
feat/     → new features       e.g. feat/buyrentkenya-scraper
fix/      → bug fixes          e.g. fix/dag-start-date
database/ → schema/DB changes  e.g. database/schema-transform
infra/    → infrastructure     e.g. infra/airflow-docker
chore/    → housekeeping       e.g. chore/update-gitignore
```
---

## Notes
- Always branch off `main`. Open a PR to merge back. Never push directly to `main`.
- The csv exports are not included in this repo due to their large volume, to access them contact the DE team directly or export directly from the database.

---

Data Engineering Team | Smart Real Estate Analytics Platform | 2026