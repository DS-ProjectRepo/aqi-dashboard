import json
from datetime import datetime

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from scipy import stats

from aqi_utils import get_aqi_color, calculate_environmental_risk_index, calculate_trend_score
from data_loading import MONTH_ORDER


def render_executive_overview(filtered: pd.DataFrame) -> None:
    st.markdown("## 🎖️ Executive Analytics Overview")

    m1, m2, m3, m4, m5 = st.columns(5)
    city_group = filtered.groupby("City")["AQI_avg"].mean()

    with m1:
        avg_aqi = filtered["AQI_avg"].mean()
        st.metric("📈 Average AQI", f"{avg_aqi:.1f}")

    with m2:
        median_aqi = filtered["AQI_avg"].median()
        delta = f"{((median_aqi - avg_aqi) / avg_aqi * 100):.1f}%" if avg_aqi else "0.0%"
        st.metric("🎯 Median AQI", f"{median_aqi:.1f}", delta)

    with m3:
        st.metric(
            "🌐 Coverage",
            f"{filtered['City'].nunique()} Cities",
            f"{filtered['StateName'].nunique()} States",
        )

    with m4:
        polluted_pct = (
            len(city_group[city_group > 150]) / len(city_group) * 100
            if len(city_group)
            else 0
        )
        st.metric("🚨 High Pollution Cities", f"{polluted_pct:.1f}%")

    with m5:
        healthy = len(city_group[city_group <= 100])
        healthy_pct = healthy / len(city_group) * 100 if len(city_group) else 0
        st.metric("✅ Healthy Cities", f"{healthy}", f"{healthy_pct:.0f}%")

    a1, a2, a3, a4, a5 = st.columns(5)

    with a1:
        eri = calculate_environmental_risk_index(filtered)
        st.metric("⚠️ Environmental Risk Index", f"{eri:.1f}/100")

    with a2:
        trend = calculate_trend_score(filtered)
        label = "Worsening" if trend > 0 else "Improving"
        st.metric("📊 Pollution Trend", f"{abs(trend):.1f}%", label)

    with a3:
        q1 = filtered["AQI_avg"].quantile(0.25)
        q3 = filtered["AQI_avg"].quantile(0.75)
        iqr = q3 - q1
        anomalies = filtered[
            (filtered["AQI_avg"] > q3 + 1.5 * iqr)
            | (filtered["AQI_avg"] < q1 - 1.5 * iqr)
        ]
        anomaly_pct = len(anomalies) / len(filtered) * 100 if len(filtered) else 0
        st.metric("🔍 Anomaly Rate", f"{anomaly_pct:.2f}%", f"{len(anomalies)} records")

    with a4:
        if not city_group.empty:
            worst_city = city_group.idxmax()
            best_city = city_group.idxmin()
            spread = city_group.max() - city_group.min()
            st.metric("🎯 Pollution Spread", f"{spread:.1f}", f"{worst_city} → {best_city}")
        else:
            st.metric("🎯 Pollution Spread", "0.0", "N/A")

    with a5:
        dominant_cat = filtered["AQI_Category"].value_counts().index[0]
        dominant_pct = (
            filtered["AQI_Category"].value_counts().values[0] / len(filtered) * 100
        )
        st.metric("🎭 Dominant Category", dominant_cat, f"{dominant_pct:.1f}%")


def render_data_quality(filtered: pd.DataFrame) -> None:
    st.markdown(
        f"""
<div class="data-quality">
<b>📊 Data Quality Snapshot</b><br/>
Records: {len(filtered):,} | Cities: {filtered['City'].nunique()} | States: {filtered['StateName'].nunique()}<br/>
Date Range: {filtered['Date'].min().strftime('%d-%b-%Y')} → {filtered['Date'].max().strftime('%d-%b-%Y')}<br/>
AQI Completeness: {(1 - filtered['AQI_avg'].isna().sum() / len(filtered)) * 100:.1f}%
</div>
""",
        unsafe_allow_html=True,
    )


def render_temporal_distribution(filtered: pd.DataFrame) -> None:
    st.markdown("## 📈 Temporal & Distribution Analysis")

    t1, t2 = st.columns(2)

    with t1:
        monthly_df = (
            filtered.groupby("Month", as_index=False)["AQI_avg"]
            .agg(mean="mean", std="std", count="count")
        )
        monthly_df["Month"] = pd.Categorical(
            monthly_df["Month"], categories=MONTH_ORDER, ordered=True
        )
        monthly_df = monthly_df.sort_values("Month").dropna(subset=["Month"])

        fig_trend = go.Figure()
        fig_trend.add_trace(
            go.Scatter(
                x=monthly_df["Month"].astype(str),
                y=monthly_df["mean"],
                mode="lines+markers",
                name="Monthly Avg",
                line=dict(color="#667eea", width=4),
                marker=dict(size=10),
            )
        )
        fig_trend.add_trace(
            go.Scatter(
                x=monthly_df["Month"].astype(str),
                y=monthly_df["mean"] + monthly_df["std"],
                mode="lines",
                line_color="rgba(0,0,0,0)",
                showlegend=False,
            )
        )
        fig_trend.add_trace(
            go.Scatter(
                x=monthly_df["Month"].astype(str),
                y=monthly_df["mean"] - monthly_df["std"],
                mode="lines",
                fill="tonexty",
                line_color="rgba(0,0,0,0)",
                name="±1σ band",
                fillcolor="rgba(102, 126, 234, 0.2)",
            )
        )
        fig_trend.update_layout(
            title="Monthly AQI Trend with Confidence Bands",
            xaxis_title="Month",
            yaxis_title="Average AQI",
            hovermode="x unified",
            template="plotly_white",
            height=420,
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    with t2:
        fig_dist = px.violin(
            filtered,
            y="AQI_avg",
            x="AQI_Category",
            color="AQI_Category",
            points="outliers",
            title="AQI Distribution by Category (Violin Plot)",
            labels={"AQI_avg": "AQI Value", "AQI_Category": "Category"},
            color_discrete_sequence=[
                "#10B981",
                "#F59E0B",
                "#F97316",
                "#EF4444",
                "#991B1B",
                "#1F2937",
            ],
            height=420,
        )
        fig_dist.update_layout(template="plotly_white", showlegend=False)
        st.plotly_chart(fig_dist, use_container_width=True)

    st.divider()


def render_city_rankings(filtered: pd.DataFrame) -> None:
    st.markdown("## 🏙️ City Rankings")

    city_group = filtered.groupby("City")["AQI_avg"].mean()
    c1, c2 = st.columns(2)

    with c1:
        top_cities = city_group.sort_values(ascending=False).head(15)
        fig_top = go.Figure(
            data=[
                go.Bar(
                    y=top_cities.index,
                    x=top_cities.values,
                    orientation="h",
                    marker=dict(color=[get_aqi_color(v) for v in top_cities.values]),
                    text=np.round(top_cities.values, 1),
                    textposition="auto",
                )
            ]
        )
        fig_top.update_layout(
            title="🔴 Top 15 Most Polluted Cities",
            xaxis_title="Average AQI",
            yaxis_title="City",
            template="plotly_white",
            height=480,
            margin=dict(l=160),
        )
        st.plotly_chart(fig_top, use_container_width=True)

    with c2:
        clean_cities = city_group.sort_values(ascending=True).head(15)
        fig_clean = go.Figure(
            data=[
                go.Bar(
                    y=clean_cities.index,
                    x=clean_cities.values,
                    orientation="h",
                    marker=dict(color=[get_aqi_color(v) for v in clean_cities.values]),
                    text=np.round(clean_cities.values, 1),
                    textposition="auto",
                )
            ]
        )
        fig_clean.update_layout(
            title="🟢 Top 15 Cleanest Cities",
            xaxis_title="Average AQI",
            yaxis_title="City",
            template="plotly_white",
            height=480,
            margin=dict(l=160),
        )
        st.plotly_chart(fig_clean, use_container_width=True)

    st.divider()

def render_stats_anomalies(filtered: pd.DataFrame) -> None:
    st.markdown("## 📊 Statistical Summary & Anomalies")

    s1, s2 = st.columns(2)

    with s1:
        series = filtered["AQI_avg"].dropna()
        stats_df = pd.DataFrame(
            {
                "Metric": [
                    "Mean",
                    "Median",
                    "Std Deviation",
                    "Min",
                    "Q1 (25%)",
                    "Q3 (75%)",
                    "Max",
                    "IQR",
                    "Skewness",
                    "Kurtosis",
                    "Coeff. of Variation",
                ],
                "Value": [
                    f"{series.mean():.2f}",
                    f"{series.median():.2f}",
                    f"{series.std():.2f}",
                    f"{series.min():.2f}",
                    f"{series.quantile(0.25):.2f}",
                    f"{series.quantile(0.75):.2f}",
                    f"{series.max():.2f}",
                    f"{series.quantile(0.75) - series.quantile(0.25):.2f}",
                    f"{stats.skew(series):.2f}",
                    f"{stats.kurtosis(series):.2f}",
                    f"{(series.std() / series.mean()) * 100:.2f}%",
                ],
            }
        )
        st.dataframe(stats_df, use_container_width=True, hide_index=True)

    with s2:
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        anomalies = filtered[
            (filtered["AQI_avg"] > Q3 + 1.5 * IQR)
            | (filtered["AQI_avg"] < Q1 - 1.5 * IQR)
        ]
        anomaly_pct = len(anomalies) / len(filtered) * 100 if len(filtered) else 0
        st.info(
            f"🔍 **Anomaly Detection (IQR method)**: {len(anomalies)} records "
            f"({anomaly_pct:.2f}%) are statistical outliers."
        )
        st.dataframe(
            anomalies[["Date", "StateName", "City", "AQI_avg"]].head(20),
            use_container_width=True,
        )

    st.divider()


def render_category_correlation(filtered: pd.DataFrame) -> None:
    st.markdown("## 🔬 Category Distribution & Correlation")

    i1, i2 = st.columns(2)

    with i1:
        cat_counts = filtered["AQI_Category"].value_counts()
        fig_cat = px.pie(
            values=cat_counts.values,
            names=cat_counts.index,
            title="AQI Category Distribution",
        )
        st.plotly_chart(fig_cat, use_container_width=True)

    with i2:
        numeric_cols = [c for c in ["AQI_avg", "AQI_max", "AQI_min"] if c in filtered]
        num_df = filtered[numeric_cols].dropna()
        if not num_df.empty:
            corr = num_df.corr()
            fig_corr = go.Figure(
                data=go.Heatmap(
                    z=corr.values,
                    x=corr.columns,
                    y=corr.columns,
                    colorscale="RdBu",
                    zmid=0,
                    zmin=-1,
                    zmax=1,
                    text=np.round(corr.values, 2),
                    texttemplate="%{text}",
                )
            )
            fig_corr.update_layout(
                title="Correlation Matrix (AQI Metrics)",
                template="plotly_white",
                height=400,
            )
            st.plotly_chart(fig_corr, use_container_width=True)

    st.divider()