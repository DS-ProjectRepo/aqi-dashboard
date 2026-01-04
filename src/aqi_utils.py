import numpy as np
import pandas as pd


def classify_aqi(aqi_value: float) -> str:
    if pd.isna(aqi_value):
        return "Unknown"
    if aqi_value <= 50:
        return "🟢 Good"
    if aqi_value <= 100:
        return "🟡 Satisfactory"
    if aqi_value <= 200:
        return "🟠 Moderate"
    if aqi_value <= 300:
        return "🔴 Poor"
    if aqi_value <= 400:
        return "🔴 Very Poor"
    return "⚫ Severe"


def get_aqi_color(aqi_value: float) -> str:
    if aqi_value <= 50:
        return "#10B981"
    if aqi_value <= 100:
        return "#F59E0B"
    if aqi_value <= 200:
        return "#F97316"
    if aqi_value <= 300:
        return "#EF4444"
    if aqi_value <= 400:
        return "#991B1B"
    return "#1F2937"


def calculate_environmental_risk_index(df: pd.DataFrame) -> float:
    if df.empty:
        return 0.0
    avg_aqi = df["AQI_avg"].mean()
    max_aqi = df["AQI_avg"].max()
    std_aqi = df["AQI_avg"].std()
    score = (avg_aqi / 500) * 40 + (max_aqi / 500) * 40 + (std_aqi / 100) * 20
    return max(0.0, min(100.0, score))


def calculate_trend_score(df: pd.DataFrame) -> float:
    if "Month" not in df.columns or df.empty:
        return 0.0
    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December",
    ]
    monthly = df.groupby("Month")["AQI_avg"].mean()
    monthly = monthly.reindex([m for m in month_order if m in monthly.index])
    if len(monthly) < 2:
        return 0.0
    first_half = monthly.iloc[: len(monthly) // 2].mean()
    second_half = monthly.iloc[len(monthly) // 2 :].mean()
    if first_half == 0 or np.isnan(first_half):
        return 0.0
    trend = (second_half - first_half) / first_half * 100
    return max(-100.0, min(100.0, trend))
