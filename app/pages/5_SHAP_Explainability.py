
import sys
from pathlib import Path

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="SHAP Explainability",
    layout="wide"
)

APP_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP_DIR))

from common_style import apply_app_style

apply_app_style()

# --------------------------------------------------
# 2. PROJECT PATH
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

SHAP_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "shap_feature_importance.csv"
)

# --------------------------------------------------
# 3. THEME-AWARE CHART STYLING
# --------------------------------------------------

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
        axis="x",
        color=grid_color,
        linestyle="--",
        alpha=0.4
    )


# --------------------------------------------------
# 4. LOAD SHAP DATA
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
# 5. MAIN PAGE
# --------------------------------------------------

st.title("SHAP Model Explainability")

st.write(
    "Understand how customer behaviour influences "
    "our machine learning churn predictions using "
    "SHAP (SHapley Additive exPlanations)."
)

st.divider()

# --------------------------------------------------
# 6. LOAD DATA WITH ERROR HANDLING
# --------------------------------------------------

try:
    shap_df = load_shap_data()

    if shap_df.empty:
        st.error("No valid SHAP feature importance data found.")
        st.stop()

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
# 7. FEATURE IMPORTANCE OVERVIEW
# --------------------------------------------------

st.header("SHAP Feature Importance Overview")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Features",
    len(shap_df)
)

col2.metric(
    "Most Important Feature",
    str(shap_df.iloc[0]["Feature"])
)

col3.metric(
    "Highest SHAP Importance",
    f'{shap_df.iloc[0]["Mean_SHAP_Importance"]:.4f}'
)

st.divider()


# --------------------------------------------------
# 8. SHAP FEATURE IMPORTANCE BAR CHART
# --------------------------------------------------

st.header("Feature Importance Ranking")

st.subheader("Mean Absolute SHAP Values")

shap_plot = shap_df.sort_values(
    by="Mean_SHAP_Importance",
    ascending=True
)

fig, ax = plt.subplots(
    figsize=(10, max(5, len(shap_plot) * 0.4))
)

ax.barh(
    shap_plot["Feature"],
    shap_plot["Mean_SHAP_Importance"]
)

ax.set_xlabel("Mean Absolute SHAP Value")
ax.set_ylabel("Features")

ax.set_title(
    "SHAP Feature Importance for Churn Prediction"
)

style_chart(fig, ax)

plt.tight_layout()

st.pyplot(
    fig,
    use_container_width=True
)

plt.close(fig)

st.caption(
    "Higher mean absolute SHAP values indicate "
    "greater average contribution to model predictions."
)

st.divider()


# --------------------------------------------------
# 9. SHAP FEATURE IMPORTANCE TABLE
# --------------------------------------------------

st.header("SHAP Feature Importance Details")

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
# 10. INDIVIDUAL FEATURE INTERPRETATION
# --------------------------------------------------

st.header("Understanding Important Features")

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

max_importance = shap_df["Mean_SHAP_Importance"].max()

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

        progress_value = (
            float(importance / max_importance)
            if max_importance > 0
            else 0.0
        )

        st.progress(
            min(max(progress_value, 0.0), 1.0)
        )


st.divider()


# --------------------------------------------------
# 11. KEY BUSINESS INSIGHTS
# --------------------------------------------------

st.header("Key Business Insights")

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
# 12. HOW SHAP WORKS
# --------------------------------------------------

st.header("Understanding SHAP")

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
# 13. FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Customer Intelligence & Predictive Analytics Platform | "
    "SHAP Model Explainability"
)
