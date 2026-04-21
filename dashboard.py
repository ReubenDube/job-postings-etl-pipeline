import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Job Postings Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Job Postings ETL Dashboard")
st.markdown("### Interactive exploration of cleaned job postings data from the ETL pipeline")

# Define paths
PROJECT_ROOT = Path(__file__).parent
DB_PATH = PROJECT_ROOT / "data" / "job_postings.db"

# Load data function with caching
@st.cache_data
def load_data():
    if not DB_PATH.exists():
        st.error(f"Database not found at {DB_PATH}. Please run the ETL pipeline first.")
        return pd.DataFrame()
    
    engine = create_engine(f"sqlite:///{DB_PATH}")
    df = pd.read_sql("SELECT * FROM job_postings", engine)
    return df

df = load_data()

if df.empty:
    st.stop()

# Sidebar filters
st.sidebar.header("🔍 Filters")

# Country filter
countries = sorted(df['country'].unique())
selected_countries = st.sidebar.multiselect(
    "Select Countries",
    options=countries,
    default=countries[:5] if len(countries) > 5 else countries
)

# Salary filter
salary_option = st.sidebar.radio(
    "Salary Information",
    options=["All", "Has Salary", "No Salary"]
)

# Fraud filter
fraud_option = st.sidebar.radio(
    "Fraudulent Jobs",
    options=["All", "Real Only", "Fraud Only"]
)

# Apply filters
filtered_df = df[df['country'].isin(selected_countries)]

if salary_option == "Has Salary":
    filtered_df = filtered_df[filtered_df['has_salary'] == 1]
elif salary_option == "No Salary":
    filtered_df = filtered_df[filtered_df['has_salary'] == 0]

if fraud_option == "Real Only":
    filtered_df = filtered_df[filtered_df['fraudulent'] == 0]
elif fraud_option == "Fraud Only":
    filtered_df = filtered_df[filtered_df['fraudulent'] == 1]

# Main metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Jobs", f"{len(filtered_df):,}")
col2.metric("With Salary Info", f"{filtered_df['has_salary'].sum():,}")
col3.metric("Fraudulent Jobs", f"{filtered_df['fraudulent'].sum():,}")
col4.metric("Unique Countries", len(selected_countries))

# Data table
st.subheader("📋 Filtered Job Postings")
st.dataframe(filtered_df.head(50), use_container_width=True)

# Visualizations
st.subheader("📈 Visualizations")

col_v1, col_v2 = st.columns(2)

with col_v1:
    st.write("**Jobs by Country (Top 10)**")
    country_counts = filtered_df['country'].value_counts().head(10)
    st.bar_chart(country_counts)

with col_v2:
    st.write("**Fraudulent vs Real Jobs**")
    fraud_counts = filtered_df['fraudulent'].value_counts()
    st.bar_chart(fraud_counts)

# Industry breakdown
st.subheader("🏭 Top Industries")
industry_counts = filtered_df['industry'].value_counts().head(10)
st.bar_chart(industry_counts)

# Success message
st.success("✅ Data loaded successfully from your ETL pipeline!")

st.caption("Built as part of my Data Science / ML Engineer portfolio")