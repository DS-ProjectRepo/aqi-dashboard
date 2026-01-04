import pandas as pd
import streamlit as st

from aqi_utils import classify_aqi

MONTH_ORDER = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]


@st.cache_data(ttl=3600)
def load_raw_ndap(path: str = "data/raw/ndap_air_quality_index_cities.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    df["AQI_avg"] = pd.to_numeric(df.get("AQIavg", df.get("AQI_avg")), errors="coerce")
    df["AQI_max"] = pd.to_numeric(df.get("AQImax", df.get("AQI_max")), errors="coerce")
    df["AQI_min"] = pd.to_numeric(df.get("AQImin", df.get("AQI_min")), errors="coerce")
    df["Date"] = pd.to_datetime(df.get("Date"), errors="coerce")
    if "Month" in df.columns:
        df["Month"] = df["Month"].astype(str).str.split(",").str[0].str.strip()
    else:
        df["Month"] = df["Date"].dt.strftime("%B")
    df = df.dropna(subset=["AQI_avg"])
    df["AQI_Category"] = df["AQI_avg"].apply(classify_aqi)
    return df
