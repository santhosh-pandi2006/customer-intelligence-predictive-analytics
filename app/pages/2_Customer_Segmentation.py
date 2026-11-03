
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Customer Segmentation",
    page_icon="👥",
    layout="wide"
)

# ==========================================
# DATA LOADING
# ==========================================

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "processed"

rfm = pd.read_csv(
    DATA_DIR / "customer_rfm_segments.csv"
)

segment_analysis = pd.read_csv(
    DATA_DIR / "customer_segment_analysis.csv"
)

# ==========================================
# PAGE HEADER
# ==========================================

st.title("👥 Customer Segmentation Analysis")

st.write(
    "Understand customer behaviour using "
    "RFM (Recency, Frequency and Monetary) analysis."
)

st.divider()

st.success(
    f"Successfully loaded data for {rfm['Customer ID'].nunique():,} customers."
)
# Customer Segment Overview
st.divider()
st.header("📊 Customer Segment Overview")

# Calculate segment statistics
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

# Display KPI metrics
total_customers = len(rfm)
total_segments = rfm["Customer_Segment"].nunique()
total_revenue = rfm["Monetary"].sum()

col1, col2, col3 = st.columns(3)

col1.metric("Total Customers", f"{total_customers:,}")
col2.metric("Customer Segments", total_segments)
col3.metric("Total Customer Revenue", f"£{total_revenue:,.2f}")

# Display segment summary
st.subheader("Customer Segment Summary")
st.dataframe(
    segment_summary.sort_values(
        "Total_Customers", ascending=False
    ),
    width="stretch",
    hide_index=True
)
import matplotlib.pyplot as plt

st.divider()
st.header("📊 Customer Segment Visualizations")

col1, col2 = st.columns(2)

# Chart 1: Customer Distribution
with col1:
    st.subheader("Customer Distribution by Segment")

    fig1, ax1 = plt.subplots(figsize=(8, 6))

    ax1.pie(
        segment_summary["Total_Customers"],
        labels=segment_summary["Customer_Segment"],
        autopct="%1.1f%%",
        startangle=90,
        wedgeprops={"width": 0.45}
    )

    ax1.set_title("Customer Segment Distribution")
    fig1.tight_layout()

    st.pyplot(fig1)
    plt.close(fig1)


# Chart 2: Revenue Contribution
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
    ax2.set_title("Revenue by Customer Segment")
    fig2.tight_layout()

    st.pyplot(fig2)
    plt.close(fig2)