# Company Revenue and Client Intelligence Dashboard

Data-Driven Strategy for Marketplace Operations

## Project Overview

This project analyzes a transactional dataset of 5,000+ historical deals from the event-driven company to identify conversion patterns and optimize sales outreach. By engineering a Lead Value Index (LVI), I transformed raw transactional data into a prioritized sales framework that accounts for both deal size and the statistical probability of closing.

## Technical Stack

- **Analysis:** Python (Pandas, NumPy)
- **Visualization:** Plotly (Express & Subplots)
- **Deployment:** Dash (Plotly), GitHub, Render
- **Data Source:** Sell CRM API (live integration)

## Key Analytical Steps

### 1. Data Wrangling & Cleaning

- **Multi-Source Merging:** Combined `deals.csv` and `contacts.csv` to reconstruct missing client segment data.
- **Temporal Filtering:** Focused on post-2022 data to ensure insights reflected current market trends.
- **Target Engineering:** Defined a binary `converted` feature based on "Event Complete" vs. "Cancelled/Unqualified" outcomes.

### 2. Lead Value Index (LVI) Modeling

Because a high-value quote does not always equal high-value revenue, I calculated the Expected Value for every industry segment and price band:
LVI = Avg. Deal Value × Conversion Rate

This revealed the "Sweet Spot"—segments with moderate deal sizes ($1.5k–$2.5k) that outperformed larger deals in total expected revenue due to higher conversion rates.

## 3. Priority Matrix

The final output is a quadrant-based Priority Matrix used for resource allocation:

- **Strategic Priority:** High Value / High Conversion (Focus here)
- **Revenue Leakage:** High Value / Low Conversion (Investigate pricing/friction)
- **Efficiency Wins:** Low Value / High Conversion (Automate these)
- **Low ROI:** Low Value / Low Conversion (Deprioritize)

## How to Use the Dashboard

### Access the Live Dashboard

- **URL:** https://company-dash-demo.onrender.com
- **Username:** `admin`
- **Password:** `demo`

### Explore the Data

- **Tab 1 (Client Segment Overview):** View portfolio health with KPIs and segment-level conversion metrics
- **Tab 2 (Segment Deep Dive):** Analyze deal band performance within each segment
- **Tab 3 (Opportunity Analysis):** Use the Priority Matrix to identify strategic opportunities and revenue leakage

### Run Locally (Development)
```bash
git clone https://github.com/pathesa/company-dash-demo.git
cd company-dash-demo
pip install -r requirements.txt
python app.py
```

Dashboard runs on `http://localhost:8050`

**Note:** Local version uses sample data (see `/data` folder)

## Data Privacy

- Dashboard is password-protected for secure access
- Production uses live Sell CRM API with authenticated credentials
- Sample data provided for local development and demonstrations
- No sensitive client information is exposed in the repository

## Technologies & Concepts

- **Data Pipeline:** ETL with pandas and API integration
- **Statistical Analysis:** Correlation matrices, cohort analysis, temporal trends
- **Visualization Best Practices:** Interactive dashboards, quadrant analysis, heatmaps
- **DevOps:** CI/CD pipeline via GitHub and Render for automated deployment

## Deployment

Deployed on Render with:
- Automated CI/CD pipeline via GitHub
- Environment-based configuration for credentials
- 15-minute idle sleep (free tier) with ~30-second wake-up time
- Live Sell CRM API integration for real-time data refresh

## Future Enhancements

- Time-series forecasting for revenue trends
- API integration with Sell CRM for automated lead scoring
- New vs Repeat Client Analysis

## Screenshots
<img width="1404" height="665" alt="Screenshot 2025-12-29 at 12 23 40 PM" src="https://github.com/user-attachments/assets/df31e2d4-e6c0-46d5-b186-053ea7c0d3ad" />
<img width="1431" height="639" alt="Screenshot 2025-12-29 at 12 24 46 PM" src="https://github.com/user-attachments/assets/21522897-e45a-4029-a9d5-16f0ac0430a6" />
<img width="1416" height="627" alt="Screenshot 2025-12-29 at 12 25 04 PM" src="https://github.com/user-attachments/assets/e932482f-f813-47d5-b11f-fe7b6dfb6b44" />


## Contact

Samantha Pathe | [GitHub](https://github.com/pathesa) | [Email](mailto:pathesa@gmail.com)
