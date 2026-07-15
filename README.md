# Company Revenue and Client Intelligence Dashboard

## Project Overview

This project builds an end-to-end analytics pipeline that extracts live CRM data, cleans and transforms transactional records, and powers an interactive dashboard for analyzing 5,000+ deals. The dashboard helps identify conversion patterns, evaluate customer segments, and uncover opportunities to improve sales performance.

## Technical Stack

- **Analysis:** Python (Pandas, NumPy)
- **Visualization:** Plotly (Express & Subplots)
- **Deployment:** Dash (Plotly), GitHub, Render
- **Data Source:** Sell CRM API (live integration)

## Analytical Steps

### 1. Data Wrangling & Feature Engineering

- Retrieved live deal, contact and stage data from the Sell CRM API.
- Flattened nested JSON custom fields into tabular datasets.
- Merged deal and contact records to recover missing client segments.
- Filtered historial data to completed, cancelled and unqualified opportunities after 2022.
- Engineered analysis features including:
  - Binary conversion outcome
  - Lead time
  - Deal size bands
  - Standardized client segment categories

### 2. Conversion & Revenue Analysis

Rather than evaluating opportunities solely based on quote value, I combined historical conversion rates with average deal size to estimate expected revenue across client segment deal bands. This analysis identified segments that consistently generated the highest expected return, as well as high-value segments where low conversion rates represented potential revenue opportunities.

## 3. Interactive Dashboard

Built an interactive dashboard to explore:

- Conversion rates by client segment
- Revenue contribution by segment and deal size
- Expected revenue across customer groups
- Missed revenue from unconverted opportunities
- Priority matrix comparing conversion rate and expected revenue

## How to Use the Dashboard

### Access the Live Dashboard

- **URL:** https://company-dash-demo.onrender.com
- **Username:** `admin`
- **Password:** `demo`

- **Tab 1 (Client Segment Overview):** View portfolio health with KPIs and segment-level conversion metrics
- **Tab 2 (Segment Deep Dive):** Analyze deal band performance within each segment
- **Tab 3 (Opportunity Analysis):** Use the Priority Matrix to identify strategic opportunities and revenue leakage

## Data Privacy

- Dashboard is password-protected for secure access
- Production uses live Sell CRM API with authenticated credentials
- No sensitive client information is exposed in the repository

## Technologies & Concepts

- **Data Engineering:** REST API integration, ETL pipeline, data cleaning and transformation with pandas
- **Data Analysis:** Feature engineering, conversion analysis, expected value analysis, customer segmentation
- **Visualization:** Interactive dashboards built with Plotly Dash
- **Deployment:** GitHub, Render, environment variables, automated deployment

## Deployment

Deployed on Render with:
- Automated CI/CD pipeline via GitHub
- Environment-based configuration for credentials
- 15-minute idle sleep with ~30-second wake-up time
- Live Sell CRM API integration for real-time data refresh

## Future Enhancements

- Time-series forecasting for revenue trends
- New vs Repeat Client Analysis

## Screenshots
<img width="1404" height="665" alt="Screenshot 2025-12-29 at 12 23 40 PM" src="https://github.com/user-attachments/assets/df31e2d4-e6c0-46d5-b186-053ea7c0d3ad" />
<img width="1431" height="639" alt="Screenshot 2025-12-29 at 12 24 46 PM" src="https://github.com/user-attachments/assets/21522897-e45a-4029-a9d5-16f0ac0430a6" />
<img width="1416" height="627" alt="Screenshot 2025-12-29 at 12 25 04 PM" src="https://github.com/user-attachments/assets/e932482f-f813-47d5-b11f-fe7b6dfb6b44" />


## Contact

Samantha Pathe | [GitHub](https://github.com/pathesa) | [Email](mailto:pathesa@gmail.com)
