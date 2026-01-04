# 🌍 Air Quality Index Analytics Platform

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28-red?logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

**A production-grade environmental data analytics dashboard analyzing 200+ Indian cities' air quality metrics from the National Data & Analytics Platform (NDAP).**

## 🎯 Overview

This dashboard provides **comprehensive environmental intelligence** for Indian cities, featuring:

- **Real-time filtering** with sticky top controls (state, city, month, AQI category, range)
- **Executive KPIs** with 5 advanced custom metrics
- **8+ interactive visualizations** (trends, distributions, heatmaps, correlations)
- **Statistical rigor** (11 metrics including skewness, kurtosis, anomaly detection)
- **Professional UI/UX** with dark theme and gradient styling
- **Modular architecture** for easy maintenance and scaling

## ✨ Features

### 📊 Executive Analytics
- Average AQI, Median AQI, Coverage metrics
- Environmental Risk Index (custom weighted metric)
- Pollution Trend Score (-100% to +100%)
- Anomaly Rate (IQR-based detection)
- Pollution Spread analysis
- Dominant Category tracking

### 📈 Visualizations
1. **Monthly Trend** with confidence bands (±1σ)
2. **Violin Distribution** plot by AQI category
3. **Top 15 Most Polluted Cities** (horizontal bar)
4. **Top 15 Cleanest Cities** (horizontal bar)
5. **State-wise Heatmap** (monthly AQI by state)
6. **Category Distribution** (pie chart)
7. **Correlation Matrix** (AQI metrics)
8. **Anomaly Detection** table (IQR method)

### 🔧 Advanced Analytics
- Descriptive statistics (mean, median, std, quartiles)
- Skewness & Kurtosis analysis
- IQR-based outlier detection
- Confidence interval visualization
- Multi-level filtering (states → cities → categories → AQI range)

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/DS-ProjectRepo/aqi-dashboard.git
cd aqi-dashboard

Create virtual environment

bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies

bash
pip install -r requirements.txt
Ensure data file exists

text
data/raw/ndap_air_quality_index_cities.csv
(Should contain AQI data from NDAP)

Run the app

bash
streamlit run app.py
Visit: http://localhost:8501

📁 Project Structure
text
aqi-dashboard/
├── app.py                          # Main Streamlit application
├── src/
│   ├── __init__.py
│   ├── data_loading.py            # Data I/O, caching, normalization
│   ├── aqi_utils.py               # AQI classification, metrics
│   └── sections.py                # All UI sections (8 render functions)
├── data/
│   └── raw/
│       └── ndap_air_quality_index_cities.csv
├── .streamlit/
│   └── config.toml                # Streamlit theme configuration
├── requirements.txt               # Python dependencies
├── .gitignore
└── README.md
🔑 Key Technologies
Component	Technology
Framework	Streamlit 1.28
Visualization	Plotly 5.13+
Data Processing	Pandas, NumPy
Statistics	SciPy
Styling	Custom CSS + HTML
📊 Data Source
Source: National Data & Analytics Platform (NDAP), Government of India

Coverage: 200+ Indian cities

Time Period: 2020

Metrics: AQI (Average, Min, Max)

Categories: Good, Satisfactory, Moderate, Poor, Very Poor, Severe

🎓 How to Use
Select Filters (top sticky bar):

Choose states (multiple selection)

Select cities (auto-populated based on state)

Pick a month (or "All")

Select AQI categories

Adjust AQI range slider

View Insights:

Executive summary cards appear instantly

Scroll to see 8+ interactive visualizations

Hover over charts for details

Tables are sortable and searchable

Data Quality:

Snapshot badge shows records, coverage, date range

Completeness percentage displayed

Anomalies automatically flagged

📈 Advanced Metrics Explained
Environmental Risk Index (0–100)
Weighted composite of:

Average AQI: 40%

Maximum AQI: 40%

Standard Deviation: 20%

Interpretation: Higher = more pollution risk

Pollution Trend Score (-100% to +100%)
Negative: Air quality improving

Positive: Air quality worsening

Based on: First half vs. second half of year

Anomaly Rate
Uses 1.5 × IQR method:

Identifies statistical outliers

Shows % of unusual AQI readings

Useful for spotting data quality issues

🎨 UI/UX Features
Sticky Filters: Stay visible while scrolling

Dark Theme: Professional, eye-friendly

Color-coded AQI: Green (good) → Red (severe)

Responsive Layout: Works on desktop & tablet

Real-time Updates: Instant filtering (caching optimized)

🔬 Statistical Methods
Descriptive Statistics: Mean, median, std, quartiles, IQR

Distribution Analysis: Violin plots, histograms

Anomaly Detection: IQR method (1.5 × IQR threshold)

Correlation: Pearson correlation matrix

Skewness & Kurtosis: Distribution shape analysis

Confidence Intervals: ±1σ bands on trends

🚢 Deployment
Option 1: Streamlit Cloud (Recommended)
Push code to GitHub

Visit https://share.streamlit.io

Sign in with GitHub

Select repo → deploy

Live in 2 minutes!

Option 2: Docker
bash
docker build -t aqi-dashboard .
docker run -p 8501:8501 aqi-dashboard
Option 3: Railway.app
bash
railway login
railway link
railway up
💼 Portfolio Highlights
This project demonstrates:

✅ Data Science Skills

Statistical analysis (11+ metrics)

Anomaly detection (IQR method)

Time-series visualization

Distribution analysis

✅ Software Engineering

Modular architecture (src/ package)

Caching & performance optimization

Error handling & validation

Professional code organization

✅ UI/UX Design

Custom CSS styling

Responsive layout

Real-time filtering

Professional color schemes

✅ DevOps

Git version control

Cloud deployment ready

Docker containerization

Requirements management

📋 Requirements
text
streamlit==1.28.0
pandas>=1.3.0
numpy>=1.21.0
scipy>=1.7.0
plotly>=5.13.0
🤝 Contributing
Contributions welcome! Areas for enhancement:

Real-time data ingestion from APIs

Machine learning predictions

Health impact analysis

Seasonal decomposition

Multi-year trend analysis

📝 License
MIT License - feel free to use for personal/commercial projects

👤 Author
Created as a portfolio project demonstrating professional data analytics skills.

📞 Contact
GitHub: DS-ProjectRepo

Project: 
AQI Dashboard

⭐ If you find this useful, please star the repository!