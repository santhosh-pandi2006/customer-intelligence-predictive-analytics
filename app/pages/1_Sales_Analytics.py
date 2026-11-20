
import sys
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Sales Analytics",
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
# LOAD SALES DATA
# ==========================================

@st.cache_data
def load_sales_data():
    data = pd.read_csv(
        DATA_DIR / "cleaned_sales.csv",
        dtype={
            "Invoice": str,
            "StockCode": str
        },
        parse_dates=["InvoiceDate"],
        low_memory=False
    )
    return data

sales = load_sales_data()

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

    ax.grid(color=grid_color, alpha=0.25)


# ==========================================
# PAGE HEADER
# ==========================================

st.title("Sales Analytics")

st.write(
    "Explore revenue, orders, products and geographic sales performance."
)

st.divider()

st.caption(f"Total transaction records: {len(sales):,}")

# ==========================================
# SALES KPI CALCULATIONS
# ==========================================

total_revenue = sales["Revenue"].sum()
total_orders = sales["Invoice"].nunique()
total_customers = sales["Customer ID"].nunique()
total_quantity = sales["Quantity"].sum()

# ==========================================
# SALES PERFORMANCE OVERVIEW
# ==========================================

st.divider()
st.subheader("Sales Performance Overview")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown(f"""
    <div style="
        background:linear-gradient(135deg,#1D4ED8,#6366F1);
        padding:20px;
        border-radius:15px;
        color:white;
        min-height:130px;
    ">
        <h4 style="color:white;">Total Revenue</h4>
        <h2 style="color:white;">£{total_revenue / 1_000_000:.2f}M</h2>
        <p>Recorded sales revenue</p>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown(f"""
    <div style="
        background:linear-gradient(135deg,#047857,#10B981);
        padding:20px;
        border-radius:15px;
        color:white;
        min-height:130px;
    ">
        <h4 style="color:white;">Total Orders</h4>
        <h2 style="color:white;">{total_orders:,}</h2>
        <p>Unique invoices</p>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown(f"""
    <div style="
        background:linear-gradient(135deg,#7E22CE,#A855F7);
        padding:20px;
        border-radius:15px;
        color:white;
        min-height:130px;
    ">
        <h4 style="color:white;">Total Customers</h4>
        <h2 style="color:white;">{total_customers:,}</h2>
        <p>Identified customers</p>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown(f"""
    <div style="
        background:linear-gradient(135deg,#C2410C,#F97316);
        padding:20px;
        border-radius:15px;
        color:white;
        min-height:130px;
    ">
        <h4 style="color:white;">Quantity Sold</h4>
        <h2 style="color:white;">{total_quantity:,}</h2>
        <p>Total units</p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# SALES TREND AND GEOGRAPHIC ANALYSIS
# ==========================================

st.divider()

st.header("Sales Trends & Geographic Performance")

sales["Month"] = sales["InvoiceDate"].dt.to_period("M").astype(str)

monthly_revenue = (
    sales.groupby("Month")["Revenue"]
    .sum()
    .reset_index()
)

country_revenue = (
    sales.groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .sort_values()
)

col1, col2 = st.columns(2)

# ==========================================
# CHART 1: MONTHLY REVENUE
# ==========================================

with col1:
    st.subheader("Monthly Revenue Trend")

    fig1, ax1 = plt.subplots(figsize=(9, 5))

    ax1.plot(
        monthly_revenue["Month"],
        monthly_revenue["Revenue"],
        marker="o",
        linewidth=3,
        markersize=7,
        color="#818CF8"
    )

    ax1.fill_between(
        range(len(monthly_revenue)),
        monthly_revenue["Revenue"],
        color="#818CF8",
        alpha=0.20
    )

    ax1.set_xlabel("Month")
    ax1.set_ylabel("Revenue (£)")
    ax1.tick_params(axis="x", rotation=45)

    style_chart(fig1, ax1)

    fig1.tight_layout()
    st.pyplot(fig1, use_container_width=True)
    plt.close(fig1)

# ==========================================
# CHART 2: COUNTRY-WISE REVENUE
# ==========================================

with col2:
    st.subheader("Top 10 Countries by Revenue")

    fig2, ax2 = plt.subplots(figsize=(9, 5))

    country_revenue.plot(
        kind="barh",
        ax=ax2,
        color=[
            "#06B6D4", "#8B5CF6", "#F59E0B",
            "#EC4899", "#14B8A6", "#6366F1",
            "#F97316", "#0EA5E9", "#A855F7", "#10B981"
        ]
    )

    ax2.set_xlabel("Revenue (£)")
    ax2.set_ylabel("Country")

    style_chart(fig2, ax2)

    fig2.tight_layout()
    st.pyplot(fig2, use_container_width=True)
    plt.close(fig2)

# ==========================================
# TOP PRODUCT PERFORMANCE ANALYSIS
# ==========================================

st.divider()

st.header("Top Performing Products")

special_descriptions = [
    "AMAZON FEE",
    "Adjust bad debt",
    "POSTAGE",
    "DOTCOM POSTAGE",
    "Manual"
]

product_sales = sales[
    ~sales["Description"].isin(special_descriptions)
].copy()

product_summary = (
    product_sales.groupby(["StockCode", "Description"])
    .agg(
        Total_Quantity=("Quantity", "sum"),
        Total_Revenue=("Revenue", "sum"),
        Total_Orders=("Invoice", "nunique")
    )
    .reset_index()
)

top_revenue = (
    product_summary.nlargest(10, "Total_Revenue")
    .sort_values("Total_Revenue")
)

top_quantity = (
    product_summary.nlargest(10, "Total_Quantity")
    .sort_values("Total_Quantity")
)

col1, col2 = st.columns(2)

# ==========================================
# CHART 1: TOP PRODUCTS BY REVENUE
# ==========================================

with col1:
    st.subheader("Top 10 Products by Revenue")

    fig3, ax3 = plt.subplots(figsize=(10, 6))

    ax3.barh(
        top_revenue["Description"],
        top_revenue["Total_Revenue"],
        color=plt.cm.viridis(
            np.linspace(0.25, 0.9, len(top_revenue))
        )
    )

    ax3.set_xlabel("Revenue (£)")
    ax3.set_ylabel("Product")

    style_chart(fig3, ax3)

    fig3.tight_layout()
    st.pyplot(fig3, use_container_width=True)
    plt.close(fig3)

# ==========================================
# CHART 2: TOP PRODUCTS BY QUANTITY
# ==========================================

with col2:
    st.subheader("Top 10 Products by Quantity")

    fig4, ax4 = plt.subplots(figsize=(10, 6))

    ax4.barh(
        top_quantity["Description"],
        top_quantity["Total_Quantity"],
        color=plt.cm.plasma(
            np.linspace(0.25, 0.9, len(top_quantity))
        )
    )

    ax4.set_xlabel("Quantity Sold")
    ax4.set_ylabel("Product")

    style_chart(fig4, ax4)

    fig4.tight_layout()
    st.pyplot(fig4, use_container_width=True)
    plt.close(fig4)

# ==========================================
# PRODUCT PERFORMANCE TABLE
# ==========================================

st.subheader("Product Performance Details")

st.dataframe(
    product_summary.sort_values(
        "Total_Revenue",
        ascending=False
    ).head(10),
    width="stretch",
    hide_index=True
)
