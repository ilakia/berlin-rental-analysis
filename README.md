# Berlin Rental Market Analysis

An end-to-end data project exploring Airbnb pricing trends across Berlin neighbourhoods — from raw data ingestion to an interactive dashboard with an ML-based price predictor.

**Data source:** [Inside Airbnb](http://insideairbnb.com/get-the-data/) — 9,220 listings across 138 neighbourhoods

---

## Why This Project

Berlin has one of the most dynamic short-term rental markets in Europe, with significant price variation across neighbourhoods. This project was built to practise a full data workflow — cleaning messy real-world data, extracting meaningful insights through analysis, and presenting findings in an accessible, interactive format.

The dataset was chosen because it is publicly available, well-structured enough to work with but messy enough to require real cleaning, and locally relevant — useful context for understanding the Berlin housing market ahead of relocating there.

---

## What Was Built

- **ETL pipeline** — raw CSV ingestion, data cleaning, outlier removal, and structured output saved for reuse
- **Exploratory analysis** — pricing by neighbourhood, room type, superhost status, and guest capacity
- **Interactive dashboard** — filterable charts, a price map, and a data explorer built with Streamlit
- **ML price predictor** — a Linear Regression model that estimates nightly price based on listing features

---

## Tech Stack

| Tool | Purpose |
|---|---|
| **pandas** | Data cleaning, transformation, and aggregation |
| **scikit-learn** | Building and evaluating the price prediction model |
| **Plotly** | Interactive charts and the neighbourhood map |
| **Streamlit** | Dashboard framework — chosen for its Python-native workflow and clean output |

Streamlit was preferred over Tableau or Power BI because it keeps the entire project within Python, making the pipeline and visualisation layer consistent and easier to maintain.

---

## Project Structure

```
berlin-rental-analysis/
├── raw/                  # Source data from Inside Airbnb
├── processed/            # Cleaned, analysis-ready CSVs
├── notebooks/
│   ├── 01_explore.ipynb  # Data cleaning and EDA
│   ├── 02_analysis.ipynb # Neighbourhood and pricing analysis
│   └── 03_model.ipynb    # Price prediction model
├── models/               # Trained model pipeline and metadata
└── dashboard/
    └── app.py            # Streamlit dashboard
```

---

## Price Predictor

A Linear Regression model trained on 9,088 listings using neighbourhood, room type, number of guests, bedrooms, beds, and bathrooms as features.

**MAE: €46.95 · R²: 0.345**

Size-related features (accommodates, bedrooms) were the strongest predictors — consistent with the finding that size drives price more than ratings or host status in the Berlin market.

---

*Varshini · [LinkedIn](https://www.linkedin.com/in/varshini-ilakia-m-9a744a74/) · [GitHub](https://github.com/ilakia)*
