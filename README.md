# Customer Intelligence & Predictive Analytics Platform

An end-to-end Data Science and Machine Learning project that analyzes retail customer behaviour, segments customers using RFM analysis, predicts customer churn, and provides actionable business insights through an interactive Streamlit dashboard.

## Project Overview

The Customer Intelligence & Predictive Analytics Platform helps businesses understand customer purchasing behaviour, identify valuable customer segments, detect customers at risk of churn, and develop targeted retention strategies.

The platform combines data analytics, SQL, machine learning and explainable AI to transform retail transaction data into meaningful business insights.

## Project Objectives

- Analyze retail sales and customer purchasing patterns.
- Identify high-value products, countries and revenue trends.
- Segment customers using Recency, Frequency and Monetary (RFM) analysis.
- Predict customer churn using machine learning.
- Identify important churn-related features using SHAP.
- Classify customers into risk categories.
- Recommend customer retention strategies.
- Present insights through an interactive dashboard.

## Technologies Used

| Category | Technologies |
|---|---|
| Programming | Python |
| Data Analysis | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |
| Database | MySQL |
| Machine Learning | Scikit-learn, XGBoost |
| Explainable AI | SHAP |
| Dashboard | Streamlit |
| Development | Jupyter Notebook, VS Code |
| Model Storage | Joblib / Pickle |
| Version Control | Git, GitHub |

## Dataset Information

**Dataset:** Online Retail II

**Source:** UCI Machine Learning Repository

https://archive.ics.uci.edu/dataset/502/online+retail+ii

The project uses the downloaded transaction data containing the following fields:

- Invoice
- StockCode
- Description
- Quantity
- InvoiceDate
- Price
- Customer ID
- Country

**Dataset overview:**

| Metric | Value |
|---|---:|
| Original records | 541,910 |
| Original columns | 8 |
| Cleaned sales records | 524,879 |
| Cleaned sales revenue | £10,642,128.80 |
| Identified customers in sales analysis | 4,338 |
| Unique orders | 19,960 |

*Note: The downloaded file used in this project contains data from December 2010 to December 9, 2011. Revenue represents the project's cleaned positive-quantity, positive-price sales definition.*

## Project Workflow

### 1. Data Understanding and Cleaning
- Inspected dataset structure and data types.
- Identified missing values and duplicate records.
- Investigated cancelled invoices and negative quantities.
- Handled invalid and non-sales records.
- Created a cleaned sales dataset.

### 2. Exploratory Data Analysis
- Monthly revenue analysis.
- Country-wise sales analysis.
- Product performance analysis.
- Revenue distribution and outlier analysis.
- Customer purchasing behaviour analysis.

### 3. SQL Database Integration
- Created a MySQL database.
- Imported cleaned retail transaction data.
- Performed SQL-based sales and customer analysis.
- Created a monthly sales summary view.

### 4. RFM Customer Segmentation

Customers were analyzed using:

- **Recency:** How recently a customer purchased.
- **Frequency:** How often a customer purchased.
- **Monetary:** How much a customer spent.

Seven customer segments were identified:

1. Best Customers
2. Loyal Customers
3. Recent Customers
4. At Risk Customers
5. Lost Customers
6. Big Spenders
7. Regular Customers

The RFM analysis identified 4,335 customers.

### 5. Customer Churn Prediction

Built a supervised machine learning dataset using historical customer behaviour.

Machine learning models evaluated:

- Logistic Regression
- Random Forest
- XGBoost
- Optimized Random Forest

The optimized Random Forest model was selected based on its recall and F1-score performance.

### 6. Model Explainability Using SHAP

SHAP (SHapley Additive exPlanations) was used to interpret model predictions and understand the contribution of customer features.

The analysis included:
- SHAP summary plot.
- Feature importance analysis.
- Feature dependence plots.
- Business interpretation of important features.

### 7. Customer Risk Analysis

Customers were classified into three risk categories:

- High Risk
- Medium Risk
- Low Risk

Retention strategies were developed for each risk category.

## Machine Learning Performance

**Selected Model: Optimized Random Forest**

| Evaluation Metric | Score |
|---|---:|
| Accuracy | 67.06% |
| Precision | 59.14% |
| Recall | 75.86% |
| F1-Score | 66.47% |
| ROC-AUC | 0.7341 |

The model achieved 75.86% recall, making it useful for identifying a substantial proportion of customers labelled as churned in the prediction period.

## SHAP Feature Importance

The SHAP analysis identified the following feature ranking:

1. Active_Days
2. Recency
3. Monetary
4. Unique_Products
5. Frequency
6. Total_Quantity
7. Average_Order_Value

These features help explain how historical customer behaviour contributes to the model's churn predictions.

## Customer Risk Analysis

The model's held-out test dataset contained 674 customers.

| Risk Category | Customers |
|---|---:|
| High Risk | 257 |
| Medium Risk | 226 |
| Low Risk | 191 |
| **Total** | **674** |

Suggested retention strategies:

- **High Risk:** Personalized win-back campaigns and targeted offers.
- **Medium Risk:** Customer engagement and product recommendations.
- **Low Risk:** Loyalty rewards and referral campaigns.

## Interactive Streamlit Dashboard

The project includes six dashboard pages:

| Page | Description |
|---|---|
| Home | Project overview, KPIs and key business insights |
| Sales Analytics | Revenue trends, country performance and product analysis |
| Customer Segmentation | RFM segments and customer revenue contribution |
| Churn Prediction | Model performance and churn dataset overview |
| Risk Analysis | Customer risk distribution and retention strategies |
| SHAP Explainability | Feature importance and model interpretation |

## Project Structure

```text
customer-intelligence-platform/
│
├── app/
│   ├── Home.py
│   ├── test_app.py
│   └── pages/
│       ├── 1_Sales_Analytics.py
│       ├── 2_Customer_Segmentation.py
│       ├── 3_Churn_Prediction.py
│       ├── 4_Risk_Analysis.py
│       └── 5_SHAP_Explainability.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── features/
│
├── notebooks/
│
├── src/
│   ├── analytics/
│   ├── data/
│   ├── database/
│   ├── features/
│   └── models/
│
├── models/
│
├── reports/
│
├── tests/
│
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation and Execution

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd customer-intelligence-platform
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Run the Streamlit dashboard

```bash
python -m streamlit run app/Home.py
```

Open the local URL displayed in the terminal to access the dashboard.

## Project Limitations

- The downloaded dataset used in this implementation covers December 2010 to December 9, 2011.
- The churn target represents inactivity during a defined prediction period; it does not establish permanent customer churn.
- Model evaluation metrics are based on a held-out test dataset.
- Customer risk predictions shown in the dashboard represent 674 test customers, not the complete customer database.
- SHAP feature importance describes model behaviour, not causal relationships.
- Predicted churn probabilities are not perfectly calibrated against observed churn rates.

## Future Enhancements

- Deploy the dashboard to a cloud platform.
- Add real-time customer transaction processing.
- Improve churn prediction through additional feature engineering and model calibration.
- Generate customer-specific retention recommendations.
- Integrate automated customer alerts.
- Add interactive customer-level filtering and reporting.

## Author

**Santhosh Pandi M.**

B.Tech – Artificial Intelligence and Data Science

Rajalakshmi Institute of Technology