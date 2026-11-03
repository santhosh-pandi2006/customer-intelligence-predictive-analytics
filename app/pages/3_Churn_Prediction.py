import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "processed"
MODEL_DIR = BASE_DIR / "models"

# Load churn model dataset
model_data = pd.read_csv(
    DATA_DIR / "churn_feature_engineered.csv"
)

# Load optimized Random Forest model
model = joblib.load(
    MODEL_DIR / "optimized_random_forest_model.pkl"
)

st.set_page_config(
    page_title="Churn Prediction",
    page_icon="📉",
    layout="wide"
)

st.title("📉 Customer Churn Prediction")
st.write(
    "Analyze customer churn patterns and evaluate "
    "the performance of our machine learning model."
)

st.success("Churn dataset and optimized model loaded successfully!")
st.divider()
st.header("📊 Model Performance")

# Model evaluation metrics from our Day 20 results
col1, col2, col3, col4 = st.columns(4)

col1.metric("Accuracy", "67.06%")
col2.metric("Precision", "59.14%")
col3.metric("Recall", "75.86%")
col4.metric("F1 Score", "66.47%")

st.caption(
    "Metrics are based on the held-out test dataset. "
    "The optimized Random Forest achieved 75.86% churn recall."
)

st.divider()
st.header("🎯 Churn Prediction Dataset Overview")

total_customers = len(model_data)
churned_customers = int(model_data["Churn"].sum())
active_customers = total_customers - churned_customers
churn_rate = churned_customers / total_customers * 100

col1, col2, col3 = st.columns(3)

col1.metric("Total Customers", f"{total_customers:,}")
col2.metric("Active Customers", f"{active_customers:,}")
col3.metric("Churned Customers", f"{churned_customers:,}")

st.metric("Historical Churn Rate", f"{churn_rate:.2f}%")