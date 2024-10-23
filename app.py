# app.py (formally streamlit_dashboard.py)

# 1. Import necessary libraries
import streamlit as st
import pandas as pd
import plotly.express as px

# Disable PyArrow engine
pd.options.mode.data_manager = "legacy"

# 2. Load the dataset and perform basic cleaning
df = pd.read_csv("vehicles_us.csv")

# Convert all columns to strings to prevent conversion issues
df = df.applymap(str)

# 3. Title and Introduction
st.title("Vehicle Data Exploratory Dashboard")
st.markdown("### Use this dashboard to explore vehicle data interactively.")

# Sidebar Filters
st.sidebar.header("Filter Options")

# Slider to filter by model year
model_year = st.sidebar.slider(
    "Select Model Year Range",
    int(df['model_year'].min()),
    int(df['model_year'].max()),
    (2000, 2019)
)

# Filter DataFrame
filtered_df = df[(df['model_year'].astype(int).between(*model_year))]

# Show the first few rows as a dictionary (fallback)
st.subheader("Filtered Data Preview")
st.write(filtered_df.head().to_dict())

# Plot: Price Distribution
st.subheader("Price Distribution")
fig_price = px.histogram(filtered_df, x='price', nbins=50, title='Distribution of Prices')
st.plotly_chart(fig_price)

