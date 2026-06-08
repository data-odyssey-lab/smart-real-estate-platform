# Machine Learning Team — Smart Real Estate Analytics Platform

## Overview
This folder contains all machine learning work for the Smart Real Estate Analytics Platform. The ML team is responsible for developing a two-stage predictive system that first estimates median house prices across districts or neighborhoods in Nairobi, then generates investment attractiveness scores to help investors make data-driven capital allocation decisions.

---

## Problem Statement
Real estate investors currently rely on manual estimation and expert judgment to identify areas worth investing in — a process that is costly time-consuming, and prone to significant error. This project aims to replace that process with a data-driven, two-stage ML system that predicts median house prices and ranks neighborhoods or districts by investment attractiveness.

---

## System Design: Two-Stage ML Pipeline

### Stage 1 — House Price Prediction
Given property and neighborhood-level features in Nairobi, predict the median house price
per district.

| Dimension | Detail |
|---|---|
| **Problem type** | Supervised, regression |
| **Target variable** | Median house price per district(neighborhood-level) |
| **Granularity** | District level |
| **Candidate algorithms** | Linear Regression (baseline), Random Forest, XGBoost, LightGBM |
| **Evaluation metrics** | RMSE, MAE, R² |

### Stage 2 — Investment Scoring
Using Stage 1 price predictions alongside additional market signals, generate an investment
score that ranks districts (neighborhood-level) by investment attractiveness.

| Dimension | Detail |
|---|---|
| **Problem type** | Regression (scoring) or Classification (invest / don't invest) leaning towards classification|
| **Target variable** | Investment attractiveness score or category |
| **Input** | Stage 1 predictions + price trends, demand indicators, infrastructure signals |
| **Approach** | Rule-based scoring layer (v1), ML model (v2 if labeled outcome data available) |
| **Evaluation metrics** | Spearman correlation (if scoring), Precision/Recall (if classifying) |

---

## Deliverables

- [ ] Problem statement definition
- [ ] Target prediction variables confirmed with Data Engineering team
- [ ] Initial ML pipeline design document
- [ ] Candidate algorithms and evaluation metrics finalized
- [ ] Exploratory Data Analysis (EDA)
- [ ] Feature engineering
- [ ] Stage 1 model — price prediction
- [ ] Stage 2 model — investment scoring
- [ ] Model evaluation report
- [ ] Model deployment plan

---

## Folder Structure
```text
ml/
├── README.md
├── docs/
│   ├── problem_statement.md
│   ├── ml_pipeline_design.md
│   └── evaluation_metrics.md
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_feature_engineering.ipynb
│   └── 03_model_training.ipynb
├── src/
└── models/
```

---

## Open Questions & Dependencies

| Question | Depends On | Status |
|---|---|---|
| Is the data scoped to one city or multiple? | Data Engineering | Nairobi (v1), multi-city expansion planned |
| What property features are available in the dataset? | Data Engineering | Price, location, bedrooms, bathrooms, floor size, description |
| Is historical price data available for trend forecasting? | Data Engineering | Not currently — limits trend forecasting  |
| Are labeled investment outcome labels available for Stage 2? | Analytics + Data Engineering | Pending |
| What is the neighborhood-level granularity? estate, neighborhood, is it Nairobi or even counties neighboring Nairobi | Data Engineering | Pending |

---

## Notes
- Stage 2 will use a rule-based scoring approach in v1 due to likely absence of labeled
  investment outcome data. This will be revisited once the dataset is fully scoped.
- All notebooks follow the naming convention `##_description.ipynb` for ordered execution.

---

*ML Team | Smart Real Estate Analytics Platform | 2026*