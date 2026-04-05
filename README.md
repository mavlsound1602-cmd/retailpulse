# RetailPulse — Demand Forecasting & Inventory Optimization

End-to-end supply chain analytics project built on 125 million rows of real retail data from Corporación Favorita (Ecuador).

## Project Summary

| Metric | Value |
|--------|-------|
| Dataset size | 125M rows, 4.7GB |
| Date range | Jan 2013 — Aug 2017 |
| Stores | 54 |
| Unique SKUs | 4,036 |
| A-class items forecasted | 1,111 |
| Models trained | 1,019 |
| Best MAE% (SARIMA) | 16.4% |
| Best MAE% (LightGBM) | 18.1% |
| Annual revenue tracked | $8.27M |
| Revenue at risk | $4.52M |
| Stockout cost estimated | $1.47M |

## Tech Stack

| Layer | Tool |
|-------|------|
| Data processing | pandas, numpy |
| ML forecasting | LightGBM, scikit-learn |
| Time series | statsmodels (SARIMA) |
| SQL analytics | DuckDB |
| Visualization | Plotly, matplotlib |
| Dashboard | Streamlit |

## Key Features

### 1. ABC-XYZ Segmentation
Classified 4,036 SKUs by sales volume (ABC) and demand variability (XYZ).

### 2. Dual Forecasting Strategy
- SARIMA(1,1,1)(1,1,1,7) for AY items — achieved 16.4% MAE
- LightGBM for AZ items — achieved 18.1% MAE
- SARIMA outperforms LightGBM when weekly seasonality is the dominant signal

### 3. External Signal Engineering
LightGBM models use oil prices, holiday flags, promotion indicators,
lag features (7, 14, 28 days) and rolling averages.
Oil price ranked 5th in feature importance.

### 4. Inventory Optimization
Safety Stock, Reorder Point and EOQ calculated at 95% service level per SKU.

### 5. Business Impact
- $4.52M annual revenue at risk from forecast error
- $1.47M estimated stockout losses
- 94 items in critical reorder status at any given time

### 6. SQL Analytics Layer
10 DuckDB queries across store performance, seasonality, YoY growth, oil correlation.

## Dashboard
5-tab Streamlit dashboard:
1. P&L and Inventory
2. Store Performance
3. Seasonality
4. External Signals
5. Model Comparison

## Results

| Model | MAE% | Best For |
|-------|------|----------|
| SARIMA(1,1,1)(1,1,1,7) | 16.4% | AY items — stable weekly pattern |
| LightGBM + external features | 18.1% | AZ items — erratic demand |
| LightGBM baseline | 19.3% | Before oil and holiday features |

## Setup
pip install pandas numpy lightgbm statsmodels duckdb plotly streamlit scikit-learn kaggle
streamlit run dashboard/app.py

## Data Source
Corporación Favorita Grocery Sales Forecasting — Kaggle competition dataset.
https://www.kaggle.com/c/favorita-grocery-sales-forecasting

## Author
Built as a portfolio project demonstrating end-to-end data analytics
and supply chain forecasting on production-scale data.
