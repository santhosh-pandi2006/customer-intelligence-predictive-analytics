
import sys
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Customer Segmentation",
    layout="wide"
)

# ==========================================
# IMPORT SHARED STYLING
# ==========================================

APP_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP_DIR))

from common_style import apply_app_style

apply_app_style()

# ==========================================
# PROJECT PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "processed"

# ==========================================
# LOAD DATASETS
# ==========================================

@st.cache_data
def load_segmentation_data():
    rfm_data = pd.read_csv(
        DATA_DIR / "customer_rfm_segments.csv"
    )

    segment_data = pd.read_csv(
        DATA_DIR / "customer_segment_analysis.csv"
    )

    return rfm_data, segment_data


rfm, segment_analysis = load_segmentation_data()

# ==========================================
# THEME-AWARE CHART SETTINGS
# ==========================================

theme = st.get_option("theme.base") or "light"

if theme == "dark":
    chart_bg = "#0E1117"
    chart_text = "#FAFAFA"
    grid_color = "#64748B"
else:
    chart_bg = "#FFFFFF"
    chart_text = "#172554"
    grid_color = "#CBD5E1"


def style_chart(fig, ax):
    fig.patch.set_facecolor(chart_bg)
    ax.set_facecolor(chart_bg)

    ax.tick_params(colors=chart_text)
    ax.xaxis.label.set_color(chart_text)
    ax.yaxis.label.set_color(chart_text)
    ax.title.set_color(chart_text)

    for spine in ax.spines.values():
        spine.set_color(grid_color)

    ax.grid(
        color=grid_color,
        alpha=0.25
    )


# ==========================================
# PAGE HEADER
# ==========================================

st.title("Customer Segmentation Analysis")

st.write(
    "Understand customer behaviour using "
    "RFM (Recency, Frequency and Monetary) analysis."
)

st.divider()

st.success(
    f"Successfully loaded data for "
    f"{rfm['Customer ID'].nunique():,} customers."
)

# ==========================================
# CUSTOMER SEGMENT OVERVIEW
# ==========================================

st.divider()

st.header("Customer Segment Overview")

segment_summary = (
    rfm.groupby("Customer_Segment")
    .agg(
        Total_Customers=("Customer ID", "count"),
        Total_Revenue=("Monetary", "sum"),
        Average_Recency=("Recency", "mean"),
        Average_Frequency=("Frequency", "mean")
    )
    .reset_index()
)

# ==========================================
# KPI CALCULATIONS
# ==========================================

total_customers = len(rfm)
total_segments = rfm["Customer_Segment"].nunique()
total_revenue = rfm["Monetary"].sum()

# ==========================================
# KPI DISPLAY
# ==========================================

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Customers",
    f"{total_customers:,}"
)

col2.metric(
    "Customer Segments",
    f"{total_segments:,}"
)

col3.metric(
    "Total Customer Revenue",
    f"£{total_revenue:,.2f}"
)

# ==========================================
# CUSTOMER SEGMENT SUMMARY
# ==========================================

st.divider()

st.subheader("Customer Segment Summary")

st.dataframe(
    segment_summary.sort_values(
        "Total_Customers",
        ascending=False
    ),
    width="stretch",
    hide_index=True
)

# ==========================================
# CUSTOMER SEGMENT VISUALIZATIONS
# ==========================================

st.divider()

st.header("Customer Segment Visualizations")

col1, col2 = st.columns(2)

# ==========================================
# CHART 1: CUSTOMER DISTRIBUTION
# ==========================================

with col1:
    st.subheader("Customer Distribution by Segment")

    fig1, ax1 = plt.subplots(figsize=(8, 6))

    wedges, texts, autotexts = ax1.pie(
        segment_summary["Total_Customers"],
        labels=segment_summary["Customer_Segment"],
        autopct="%1.1f%%",
        startangle=90,
        wedgeprops={
            "width": 0.45,
            "edgecolor": chart_bg
        }
    )

    for text in texts:
        text.set_color(chart_text)
        text.set_fontsize(9)

    for autotext in autotexts:
        autotext.set_color(chart_text)
        autotext.set_fontweight("bold")

    ax1.set_title(
        "Customer Segment Distribution",
        color=chart_text
    )

    fig1.patch.set_facecolor(chart_bg)

    fig1.tight_layout()

    st.pyplot(
        fig1,
        use_container_width=True
    )

    plt.close(fig1)

# ==========================================
# CHART 2: REVENUE CONTRIBUTION
# ==========================================

with col2:
    st.subheader("Revenue Contribution by Segment")

    revenue_data = segment_summary.sort_values(
        by="Total_Revenue",
        ascending=True
    )

    fig2, ax2 = plt.subplots(figsize=(8, 6))

    ax2.barh(
        revenue_data["Customer_Segment"],
        revenue_data["Total_Revenue"],
        color="#6366F1"
    )

    ax2.set_xlabel("Revenue (£)")

    ax2.set_title(
        "Revenue by Customer Segment"
    )

    style_chart(fig2, ax2)

    fig2.tight_layout()

    st.pyplot(
        fig2,
        use_container_width=True
    )

    plt.close(fig2)
