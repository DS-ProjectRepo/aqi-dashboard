import os
import sys
import warnings

import streamlit as st

warnings.filterwarnings("ignore")

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from src.data_loading import load_raw_ndap 
from src.sections import ( 
    render_executive_overview,
    render_data_quality,
    render_temporal_distribution,
    render_city_rankings,
    render_stats_anomalies,
    render_category_correlation,
)

st.set_page_config(
    page_title="Air Quality Index Analytics Platform | Elite Edition",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

custom_css = """
<style>
    .sticky-filters {
        position: sticky;
        top: 0;
        z-index: 999;
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 20px 20px 12px 20px;
        border-bottom: 2px solid #667eea;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
        border-radius: 0 0 14px 14px;
    }
    [data-testid="stMetricValue"] {
        font-size: 30px !important;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    [data-testid="stMetricLabel"] {
        font-size: 13px !important;
        color: #94a3b8;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    h1 {
        background: linear-gradient(135deg, #647dee 0%, #7f53ac 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        letter-spacing: -1px;
    }
    /* Data Quality Snapshot – High Contrast */
.data-quality {
    background: linear-gradient(
        135deg,
        rgba(99, 102, 241, 0.12) 0%,
        rgba(16, 185, 129, 0.12) 100%
    );
    border-left: 6px solid #6366f1;
    padding: 16px 20px;
    border-radius: 12px;
    margin: 16px 0 24px 0;
    font-size: 14px;
    color: #0f172a;
    box-shadow: 0 6px 24px rgba(0, 0, 0, 0.12);
    backdrop-filter: blur(6px);
}

/* Dark theme override */
@media (prefers-color-scheme: dark) {
    .data-quality {
        color: #e5e7eb;
        background: linear-gradient(
            135deg,
            rgba(99, 102, 241, 0.18) 0%,
            rgba(16, 185, 129, 0.18) 100%
        );
        border-left: 6px solid #22d3ee;
    }
}

</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

df = load_raw_ndap()  


col_title, col_metric = st.columns([4, 1])  # wider title, narrow metric

with col_title:
    st.title("🌍 Air Quality Index Analytics Platform — India (2020)")
    st.markdown(
        "<div style='margin-top:-10px;'>"
        "<p style='font-size:16px;font-weight:600;'>Comprehensive Environmental Intelligence System</p>"
        "<p style='font-size:13px;color:#9ca3af;margin-top:-10px;'>Government of India | NDAP</p>"
        "</div>",
        unsafe_allow_html=True,
    )

with col_metric:
    st.markdown(
        """
        <div style="text-align:right;margin-top:18px;">
            <p style="font-size:13px;color:#9ca3af;margin-bottom:0;">Data Points</p>
            <p style="font-size:26px;font-weight:700;margin-top:0;">{:,}</p>
        </div>
        """.format(len(df)),
        unsafe_allow_html=True,
    )


f1, f2, f3, f4, f5 = st.columns(5)

with f1:
    states = sorted(df["StateName"].dropna().unique())
    selected_states = st.multiselect(
        "📍 States",
        options=states,
        default=[],
        key="states_filter",
    )
filtered = df[df["StateName"].isin(selected_states)] if selected_states else df.copy()

with f2:
    cities = sorted(filtered["City"].dropna().unique())
    selected_cities = st.multiselect(
        "🏙️ Cities",
        options=cities,
        default=[],
        key="cities_filter",
    )
if selected_cities:
    filtered = filtered[filtered["City"].isin(selected_cities)]

with f3:
    months_available = sorted(filtered["Month"].dropna().unique())
    month = st.selectbox(
        "🗓️ Month",
        ["All"] + months_available if len(months_available) > 0 else ["All"],
        index=0,
        key="month_filter",
    )
if month != "All":
    filtered = filtered[filtered["Month"] == month]

with f4:
    cats = sorted(filtered["AQI_Category"].unique())
    sel_cats = st.multiselect(
        "🎨 Categories",
        options=cats,
        default=[],
        key="cat_filter",
    )
if sel_cats:
    filtered = filtered[filtered["AQI_Category"].isin(sel_cats)]

with f5:
    min_aqi, max_aqi = st.slider(
        "AQI Range", 0, 500, (0, 500), key="aqi_range_filter"
    )
    filtered = filtered[
        (filtered["AQI_avg"] >= min_aqi) & (filtered["AQI_avg"] <= max_aqi)
    ]

st.markdown("</div>", unsafe_allow_html=True)

if filtered.empty:
    st.info("No data yet. Select states/cities/month/categories above to view analytics.")
    st.stop()

render_executive_overview(filtered)
render_data_quality(filtered)

render_temporal_distribution(filtered)
render_city_rankings(filtered)
render_stats_anomalies(filtered)
render_category_correlation(filtered)

st.caption(
    """
**Data Source:** NDAP, Government of India  
**Coverage:** City-level AQI data for the year 2020  

"""
)
