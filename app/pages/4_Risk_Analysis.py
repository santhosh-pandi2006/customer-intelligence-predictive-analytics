
from pathlib import Path

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Customer Risk Analysis",
    page_icon="⚠️",
    layout="wide"
)

st.title("⚠️ Customer Risk Analysis")

st.write(
    "Identify customers at risk of churn and "
    "prioritize retention strategies."
)

# --------------------------------------------------
# 2. LOAD CUSTOMER PREDICTIONS
# --------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parents[2]

DATA_PATH = (
    ROOT_DIR
    / "data"
    / "processed"
    / "customer_churn_predictions.csv"
)

@st.cache_data
def load_predictions():
    data = pd.read_csv(DATA_PATH)

    required_columns = [
        "Customer_ID",
        "Actual_Churn",
        "Churn_Probability",
        "Predicted_Churn",
        "Risk_Category",
        "Retention_Strategy"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns: {missing_columns}"
        )

    return data

try:
    predictions = load_predictions()

    st.success(
        f"Successfully loaded predictions for "
        f"{len(predictions):,} customers."
    )

except FileNotFoundError:
    st.error("Customer churn prediction file not found.")
    st.stop()

except Exception as e:
    st.error(f"Error loading predictions: {e}")
    st.stop()

# --------------------------------------------------
# 3. RISK CATEGORY SUMMARY
# --------------------------------------------------

st.divider()

st.header("📊 Customer Risk Overview")

risk_counts = predictions["Risk_Category"].value_counts()

high_risk = risk_counts.get("High Risk", 0)
medium_risk = risk_counts.get("Medium Risk", 0)
low_risk = risk_counts.get("Low Risk", 0)

total_customers = len(predictions)

high_percentage = high_risk / total_customers * 100
medium_percentage = medium_risk / total_customers * 100
low_percentage = low_risk / total_customers * 100

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Customers",
    f"{total_customers:,}"
)

col2.metric(
    "High Risk",
    f"{high_risk:,}",
    f"{high_percentage:.2f}%"
)

col3.metric(
    "Medium Risk",
    f"{medium_risk:,}",
    f"{medium_percentage:.2f}%"
)

col4.metric(
    "Low Risk",
    f"{low_risk:,}",
    f"{low_percentage:.2f}%"
)

# --------------------------------------------------
# 4. CUSTOMER DISTRIBUTION BY RISK
# --------------------------------------------------

st.divider()

st.header("📈 Risk Category Distribution")

risk_order = [
    "High Risk",
    "Medium Risk",
    "Low Risk"
]

risk_distribution = (
    predictions["Risk_Category"]
    .value_counts()
    .reindex(risk_order, fill_value=0)
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Customer Count by Risk")

    st.bar_chart(risk_distribution)

with col2:
    st.subheader("Risk Category Percentages")

    risk_percentages = (
        risk_distribution / total_customers * 100
    )

    st.bar_chart(risk_percentages)

# --------------------------------------------------
# 5. CHURN PROBABILITY DISTRIBUTION
# --------------------------------------------------

st.divider()

st.header("🎯 Churn Probability Analysis")

fig, ax = plt.subplots(figsize=(10, 4))

ax.hist(
    predictions["Churn_Probability"],
    bins=20,
    edgecolor="black"
)

ax.set_title("Distribution of Customer Churn Probabilities")
ax.set_xlabel("Churn Probability")
ax.set_ylabel("Number of Customers")

st.pyplot(fig)
plt.close(fig)

# --------------------------------------------------
# 6. ACTUAL CHURN RATE BY RISK CATEGORY
# --------------------------------------------------

st.divider()

st.header("📉 Actual Churn Rate by Risk Category")

risk_performance = (
    predictions.groupby("Risk_Category")
    .agg(
        Total_Customers=("Customer_ID", "count"),
        Actual_Churned=("Actual_Churn", "sum"),
        Average_Churn_Probability=(
            "Churn_Probability", "mean"
        )
    )
    .reindex(risk_order)
    .reset_index()
)

risk_performance["Actual_Churn_Rate"] = (
    risk_performance["Actual_Churned"]
    / risk_performance["Total_Customers"]
    * 100
)

risk_performance["Average_Churn_Probability"] *= 100

st.dataframe(
    risk_performance.round(2),
    width="stretch",
    hide_index=True
)

fig, ax = plt.subplots(figsize=(9, 4))

ax.bar(
    risk_performance["Risk_Category"],
    risk_performance["Actual_Churn_Rate"]
)

ax.set_title("Actual Churn Rate by Risk Category")
ax.set_xlabel("Risk Category")
ax.set_ylabel("Actual Churn Rate (%)")

st.pyplot(fig)
plt.close(fig)

# --------------------------------------------------
# 7. RETENTION STRATEGIES
# --------------------------------------------------

st.divider()

st.header("💡 Recommended Retention Strategies")

strategy_data = [
    {
        "Risk": "High Risk",
        "Strategy": "Win-back campaigns and personalized discounts",
        "Priority": "Immediate"
    },
    {
        "Risk": "Medium Risk",
        "Strategy": "Engagement campaigns and product recommendations",
        "Priority": "Moderate"
    },
    {
        "Risk": "Low Risk",
        "Strategy": "Loyalty rewards and referral programmes",
        "Priority": "Preventive"
    }
]

strategy_df = pd.DataFrame(strategy_data)

st.dataframe(
    strategy_df,
    width="stretch",
    hide_index=True
)

# --------------------------------------------------
# 8. CUSTOMER FILTER
# --------------------------------------------------

st.divider()

st.header("🔍 Customer Risk Details")

selected_risk = st.selectbox(
    "Select Risk Category",
    ["All"] + risk_order
)

if selected_risk == "All":
    filtered_data = predictions.copy()
else:
    filtered_data = predictions[
        predictions["Risk_Category"] == selected_risk
    ].copy()

st.write(
    f"Showing {len(filtered_data):,} customers."
)

# --------------------------------------------------
# 9. CUSTOMER TABLE
# --------------------------------------------------

display_columns = [
    "Customer_ID",
    "Churn_Probability",
    "Risk_Category",
    "Retention_Strategy",
    "Actual_Churn",
    "Predicted_Churn"
]

display_data = filtered_data[display_columns].copy()

display_data["Churn_Probability"] = (
    display_data["Churn_Probability"] * 100
).round(2)

display_data = display_data.rename(
    columns={
        "Customer_ID": "Customer ID",
        "Churn_Probability": "Churn Probability (%)",
        "Risk_Category": "Risk Category",
        "Retention_Strategy": "Retention Strategy",
        "Actual_Churn": "Actual Churn",
        "Predicted_Churn": "Predicted Churn"
    }
)

st.dataframe(
    display_data.sort_values(
        by="Churn Probability (%)",
        ascending=False
    ),
    width="stretch",
    hide_index=True
)

# --------------------------------------------------
# 10. DOWNLOAD FILTERED CUSTOMER DATA
# --------------------------------------------------

csv_data = filtered_data.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Customer Risk Report",
    data=csv_data,
    file_name="customer_risk_analysis.csv",
    mime="text/csv"
)

# --------------------------------------------------
# 11. PROJECT DISCLAIMER
# --------------------------------------------------

st.divider()

st.caption(
    "Note: Risk categories and churn probabilities are based "
    "on the held-out test dataset of 674 customers. "
    "They are model-based estimates, not confirmed future churn."
)
