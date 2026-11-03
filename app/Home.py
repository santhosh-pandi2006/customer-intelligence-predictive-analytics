
import streamlit as st
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

# Project paths
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data" / "processed"

# Page configuration
st.set_page_config(
    page_title="Customer Intelligence Platform",
    page_icon="📊",
    layout="wide"
)

# Custom Dashboard Styling
st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #F4F6FC;
}

/* Main content spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Main headings */
h1, h2, h3 {
    color: #172554;
    font-weight: 700;
}

/* KPI metric cards */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #FFFFFF, #E8EEFF);
    padding: 22px 20px;
    border-radius: 15px;
    border-left: 5px solid #6366F1;
    box-shadow: 0 4px 12px rgba(31, 41, 55, 0.08);
}

/* KPI labels */
[data-testid="stMetricLabel"] {
    color: #475569;
    font-weight: 600;
}

/* KPI values */
[data-testid="stMetricValue"] {
    color: #312E81;
    font-weight: 800;
}

/* Divider */
hr {
    border-color: #D8DEEE;
}

/* Information box */
.stAlert {
    border-radius: 12px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #172554, #312E81);
}

[data-testid="stSidebar"] * {
    color: white;
}

</style>
""", unsafe_allow_html=True)


# Load datasets
# Load datasets
sales = pd.read_csv(
    DATA_DIR / "cleaned_sales.csv",
    dtype={"Invoice": str, "StockCode": str},
    parse_dates=["InvoiceDate"],
    low_memory=False
)

rfm = pd.read_csv(DATA_DIR / "customer_rfm_segments.csv")
churn = pd.read_csv(DATA_DIR / "customer_churn_analysis.csv")
rfm = pd.read_csv(DATA_DIR / "customer_rfm_segments.csv")
churn = pd.read_csv(DATA_DIR / "customer_churn_analysis.csv")

# Dashboard heading

# Gradient Dashboard Header

# Gradient Dashboard Header
st.markdown("""
<div style="
    background: linear-gradient(120deg, #172554, #4F46E5, #9333EA);
    padding: 35px;
    border-radius: 18px;
    margin-bottom: 25px;
    box-shadow: 0 6px 18px rgba(79, 70, 229, 0.20);
">
    <h1 style="color: white; font-size: 32px; margin-bottom: 10px;">
        📊 Customer Intelligence & Predictive Analytics
    </h1>
    <p style="color: #E0E7FF; font-size: 16px; margin: 0;">
        Transforming retail data into actionable business insights through analytics and machine learning.
    </p>
</div>
""", unsafe_allow_html=True)



st.divider()

# Calculate KPIs
total_customers = rfm["Customer ID"].nunique()
total_revenue = sales["Revenue"].sum()
total_orders = sales["Invoice"].nunique()
churned_customers = (churn["Churn_Status"] == "Churned").sum()

# Display KPI cards
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Customers", f"{total_customers:,}")
col2.metric("Total Revenue", f"£{total_revenue / 1_000_000:.2f}M")
col3.metric("Total Orders", f"{total_orders:,}")
col4.metric("Churned Customers", f"{churned_customers:,}")

st.divider()

# Project overview
st.subheader("Project Overview")

st.write("""
This platform analyzes retail transaction data to understand
customer purchasing behaviour and business performance.

**Key modules:**
- Sales Analytics
- Customer Segmentation (RFM)
- Customer Churn Prediction
- Customer Risk Analysis
- SHAP Model Explainability
""")

st.info("Use the sidebar to explore the different analytics modules.")


# ==========================================
# BUSINESS ANALYTICS OVERVIEW
# ==========================================

st.divider()
st.header("📈 Business Analytics Overview")

# Prepare monthly revenue
sales["Month"] = sales["InvoiceDate"].dt.to_period("M").astype(str)

monthly_revenue = (
    sales.groupby("Month")["Revenue"]
    .sum()
    .reset_index()
)

# Prepare customer segment distribution
segment_counts = rfm["Customer_Segment"].value_counts()

# Display charts side by side
col1, col2 = st.columns(2)

with col1:
    st.subheader("Monthly Revenue Trend")

    fig1, ax1 = plt.subplots(figsize=(9, 5))

    ax1.plot(
        monthly_revenue["Month"],
        monthly_revenue["Revenue"],
        marker="o",
        linewidth=3,
        color="#6366F1"
    )

    ax1.fill_between(
        range(len(monthly_revenue)),
        monthly_revenue["Revenue"],
        color="#818CF8",
        alpha=0.20
    )

    ax1.set_ylabel("Revenue (£)")
    ax1.set_xlabel("Month")
    ax1.tick_params(axis="x", rotation=45)
    ax1.grid(alpha=0.25)

    fig1.tight_layout()
    st.pyplot(fig1)
    plt.close(fig1)

with col2:
    st.subheader("Customer Segmentation")

    fig2, ax2 = plt.subplots(figsize=(9, 5))

    colors = [
        "#6366F1", "#EC4899", "#14B8A6",
        "#F59E0B", "#8B5CF6", "#06B6D4",
        "#F97316"
    ]

    ax2.pie(
        segment_counts.values,
        labels=segment_counts.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=colors,
        wedgeprops={"width": 0.42, "edgecolor": "white"}
    )

    ax2.set_title("Customer Distribution")
    fig2.tight_layout()
    st.pyplot(fig2)
    plt.close(fig2)

# ==========================================
# BUSINESS INSIGHTS
# ==========================================

st.divider()
st.header("💡 Key Business Insights")

# Calculate insights
highest_month = monthly_revenue.loc[
    monthly_revenue["Revenue"].idxmax()
]

largest_segment = segment_counts.idxmax()
largest_segment_count = segment_counts.max()

total_segments = len(segment_counts)

# Display colorful insight cards
insight1, insight2, insight3 = st.columns(3)

with insight1:
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #1D4ED8, #6366F1);
        padding: 22px;
        border-radius: 15px;
        color: white;
        min-height: 145px;
    ">
        <h4 style="color: white;">🏆 Highest Revenue Month</h4>
        <h2 style="color: white;">{highest_month['Month']}</h2>
        <p>£{highest_month['Revenue']:,.2f}</p>
    </div>
    """, unsafe_allow_html=True)

with insight2:
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #047857, #10B981);
        padding: 22px;
        border-radius: 15px;
        color: white;
        min-height: 145px;
    ">
        <h4 style="color: white;">👥 Largest Customer Segment</h4>
        <h2 style="color: white;">{largest_segment}</h2>
        <p>{largest_segment_count:,} customers</p>
    </div>
    """, unsafe_allow_html=True)

with insight3:
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #C2410C, #F97316);
        padding: 22px;
        border-radius: 15px;
        color: white;
        min-height: 145px;
    ">
        <h4 style="color: white;">📊 Customer Segments</h4>
        <h2 style="color: white;">{total_segments}</h2>
        <p>RFM customer categories</p>
    </div>
    """, unsafe_allow_html=True)
