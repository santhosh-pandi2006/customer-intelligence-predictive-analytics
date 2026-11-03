
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="SHAP Explainability",
    page_icon="🔍",
    layout="wide"
)

# --------------------------------------------------
# PROJECT PATH
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

SHAP_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "shap_feature_importance.csv"
)

# --------------------------------------------------
# LOAD SHAP DATA
# --------------------------------------------------

@st.cache_data
def load_shap_data():
    data = pd.read_csv(SHAP_FILE)

    required_columns = [
        "Feature",
        "Mean_SHAP_Importance"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns: {missing_columns}"
        )

    data["Mean_SHAP_Importance"] = pd.to_numeric(
        data["Mean_SHAP_Importance"],
        errors="coerce"
    )

    data = data.dropna(
        subset=["Feature", "Mean_SHAP_Importance"]
    )

    return data.sort_values(
        by="Mean_SHAP_Importance",
        ascending=False
    )


# --------------------------------------------------
# MAIN PAGE
# --------------------------------------------------

st.title("🔍 SHAP Model Explainability")

st.write(
    "Understand how customer behaviour influences "
    "our machine learning churn predictions using "
    "SHAP (SHapley Additive exPlanations)."
)

st.divider()

# --------------------------------------------------
# LOAD DATA WITH ERROR HANDLING
# --------------------------------------------------

try:
    shap_df = load_shap_data()

    st.success(
        "SHAP feature importance loaded successfully!"
    )

except FileNotFoundError:
    st.error(
        "SHAP feature importance file was not found. "
        "Please check the data/processed folder."
    )
    st.stop()

except Exception as e:
    st.error(f"Unable to load SHAP data: {e}")
    st.stop()


# --------------------------------------------------
# FEATURE IMPORTANCE OVERVIEW
# --------------------------------------------------

st.header("📊 SHAP Feature Importance Overview")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Features",
    len(shap_df)
)

col2.metric(
    "Most Important Feature",
    shap_df.iloc[0]["Feature"]
)

col3.metric(
    "Highest SHAP Importance",
    f'{shap_df.iloc[0]["Mean_SHAP_Importance"]:.4f}'
)

st.divider()


# --------------------------------------------------
# SHAP FEATURE IMPORTANCE BAR CHART
# --------------------------------------------------

st.header("🏆 Feature Importance Ranking")

st.subheader("Mean Absolute SHAP Values")

shap_plot = shap_df.sort_values(
    by="Mean_SHAP_Importance",
    ascending=True
)

fig, ax = plt.subplots(figsize=(10, 6))

ax.barh(
    shap_plot["Feature"],
    shap_plot["Mean_SHAP_Importance"]
)

ax.set_xlabel("Mean Absolute SHAP Value")
ax.set_ylabel("Features")

ax.set_title(
    "SHAP Feature Importance for Churn Prediction"
)

ax.grid(
    axis="x",
    linestyle="--",
    alpha=0.4
)

plt.tight_layout()

st.pyplot(fig)

plt.close(fig)

st.caption(
    "Higher mean absolute SHAP values indicate "
    "greater average contribution to model predictions."
)

st.divider()


# --------------------------------------------------
# SHAP FEATURE IMPORTANCE TABLE
# --------------------------------------------------

st.header("📋 SHAP Feature Importance Details")

display_df = shap_df.copy()

display_df["Mean_SHAP_Importance"] = (
    display_df["Mean_SHAP_Importance"].round(4)
)

display_df.insert(
    0,
    "Rank",
    range(1, len(display_df) + 1)
)

st.dataframe(
    display_df,
    width="stretch",
    hide_index=True
)

st.divider()


# --------------------------------------------------
# INDIVIDUAL FEATURE INTERPRETATION
# --------------------------------------------------

st.header("🔎 Understanding Important Features")

feature_explanations = {
    "Active_Days": (
        "Measures the number of distinct days on which "
        "a customer made purchases. It represents "
        "customer purchasing activity."
    ),

    "Recency": (
        "Measures the number of days since the customer's "
        "most recent purchase. Higher recency generally "
        "indicates a longer period of inactivity."
    ),

    "Monetary": (
        "Represents the total amount spent by a customer. "
        "It helps identify high-value customers."
    ),

    "Unique_Products": (
        "Measures the number of distinct products purchased "
        "by a customer. It represents product variety."
    ),

    "Frequency": (
        "Measures the number of unique orders placed by "
        "a customer. It represents purchasing frequency."
    ),

    "Total_Quantity": (
        "Represents the total number of product units "
        "purchased by a customer."
    ),

    "Average_Order_Value": (
        "Represents the average monetary value of a "
        "customer's orders."
    )
}

for _, row in shap_df.iterrows():

    feature = row["Feature"]
    importance = row["Mean_SHAP_Importance"]

    explanation = feature_explanations.get(
        feature,
        "Represents a customer behaviour feature used "
        "by the churn prediction model."
    )

    with st.expander(
        f'{feature} — SHAP Importance: {importance:.4f}'
    ):

        st.write(explanation)

        st.progress(
            min(
                float(
                    importance /
                    shap_df["Mean_SHAP_Importance"].max()
                ),
                1.0
            )
        )


st.divider()


# --------------------------------------------------
# KEY BUSINESS INSIGHTS
# --------------------------------------------------

st.header("💡 Key Business Insights")

top_features = shap_df.head(3)

st.subheader("Top Three Influential Features")

for rank, (_, row) in enumerate(
    top_features.iterrows(),
    start=1
):

    st.write(
        f"**{rank}. {row['Feature']}** — "
        f"SHAP Importance: "
        f"{row['Mean_SHAP_Importance']:.4f}"
    )


st.subheader("Business Recommendations")

st.markdown("""
- **Monitor customer activity:** Track how frequently
  customers interact with the business.

- **Identify inactive customers:** Pay attention to
  customers whose last purchase was a long time ago.

- **Protect high-value customers:** Monitor customer
  spending and identify valuable customers who may need
  retention campaigns.

- **Improve customer engagement:** Encourage repeat
  purchases and increase customer interaction.

- **Personalize marketing:** Use customer purchase
  behaviour to create relevant promotional campaigns.
""")


st.divider()


# --------------------------------------------------
# HOW SHAP WORKS
# --------------------------------------------------

st.header("📘 Understanding SHAP")

st.markdown("""
**SHAP (SHapley Additive exPlanations)** is a model
explainability technique based on cooperative game theory.

It explains how individual input features contribute
to a machine learning model's prediction.

### Why SHAP is used in this project

1. Identifies influential customer behaviour features.
2. Helps understand churn prediction decisions.
3. Improves model transparency.
4. Supports data-driven customer retention strategies.
5. Helps stakeholders understand machine learning results.
""")


st.info(
    "**Important:** Mean absolute SHAP importance shows "
    "the average magnitude of feature contributions. "
    "It does not show whether a feature increases or "
    "decreases churn probability, and it does not establish "
    "a causal relationship."
)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Customer Intelligence & Predictive Analytics Platform | "
    "SHAP Model Explainability"
)
