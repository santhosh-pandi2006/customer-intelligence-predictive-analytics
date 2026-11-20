
import streamlit as st


def apply_app_style():

    st.markdown("""
    <style>

    /* Theme-aware application background */
    .stApp {
        background-color: var(--background-color);
        color: var(--text-color);
    }

    /* Main content spacing */
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    /* Consistent headings */
    h1, h2, h3, h4 {
        color: var(--text-color);
        font-weight: 700;
    }

    /* Consistent sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #172554,
            #312E81
        );
    }

    /* Sidebar navigation text */
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] a,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #FFFFFF !important;
    }

    /* Sidebar selected navigation item */
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] a[aria-current="page"] {
        background-color: rgba(255, 255, 255, 0.16);
        border-radius: 8px;
    }

    /* KPI cards adapt to the active theme */
    [data-testid="stMetric"] {
        background: var(--secondary-background-color);
        padding: 18px;
        border-radius: 14px;
        border-left: 4px solid #6366F1;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
    }

    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"] {
        color: var(--text-color);
    }

    [data-testid="stMetricLabel"] {
        font-weight: 600;
    }

    [data-testid="stMetricValue"] {
        font-weight: 800;
    }

    /* Consistent information boxes */
    [data-testid="stAlert"] {
        border-radius: 12px;
    }

    /* Consistent dividers */
    hr {
        border-color: var(--secondary-background-color);
    }

    /* Mobile responsiveness */
    @media screen and (max-width: 768px) {

        .block-container {
            padding: 1rem 0.85rem 1.5rem 0.85rem;
        }

        h1 {
            font-size: 1.65rem !important;
        }

        h2 {
            font-size: 1.35rem !important;
        }

        [data-testid="stMetric"] {
            padding: 12px;
        }
    }

    </style>
    """, unsafe_allow_html=True)
