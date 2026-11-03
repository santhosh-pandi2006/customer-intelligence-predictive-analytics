import streamlit as st

st.set_page_config(
    page_title="Customer Intelligence",
    page_icon="📊",
    layout="wide"
)

st.title("Customer Intelligence Dashboard")

st.subheader("Welcome to our Data Science Project")

st.write(
    "This application analyzes customer behaviour "
    "and predicts customer churn."
)

st.success("Streamlit is working successfully!")

# Display sample metrics
col1, col2, col3 = st.columns(3)

col1.metric("Total Customers", "4,335")
col2.metric("Repeat Customers", "2,830")
col3.metric("Churn Rate", "33.43%")