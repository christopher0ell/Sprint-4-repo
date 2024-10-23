# app.py using Fastparquet and Data Validation

import os
import streamlit as st
import pandas as pd
import plotly.express as px

# Disable PyArrow for Pandas if causing issues
os.environ["PYARROW_IGNORE_IMPORT"] = "1"

# Load dataset and clean data
df = pd.read_csv("vehicles_us.csv")
df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0).clip(lower=0).astype('float64')
df['odometer'] = pd.to_numeric(df['odometer'], errors='coerce').fillna(0).clip(lower=0).astype('float64')

# Save and load with Fastparquet to avoid PyArrow
df.to_parquet("vehicles_us.parquet", engine='fastparquet')
df = pd.read_parquet("vehicles_us.parquet", engine='fastparquet')

# Data validation for 'price' column
invalid_price = df[~df['price'].apply(lambda x: isinstance(x, float))]
if not invalid_price.empty:
    st.write("Invalid entries in 'price' column:")
    st.write(invalid_price)

# Sidebar filters
model_year = st.sidebar.slider("Select Model Year Range", int(df['model_year'].min()), int(df['model_year'].max()), (2000, 2019))
odometer_limit = st.sidebar.slider("Odometer Limit (Max)", 0, int(df['odometer'].max()), 100000)

# Filter data
filtered_df = df[(df['model_year'].between(*model_year)) & (df['odometer'] <= odometer_limit)]
data_to_plot = df if st.checkbox("Show All Data", value=False) else filtered_df

# Display data safely using NumPy or Pandas fallback
st.subheader("Filtered Data Preview")
st.write(data_to_plot.to_numpy())  # Avoid PyArrow by using NumPy

# Plot graphs
fig_price = px.histogram(data_to_plot, x='price', nbins=50, title='Distribution of Prices')
st.plotly_chart(fig_price)

fig_scatter = px.scatter(data_to_plot, x='odometer', y='price', title='Price vs Odometer', labels={'odometer': 'Odometer Reading', 'price': 'Price (USD)'})
st.plotly_chart(fig_scatter)

fig_year_price = px.scatter(data_to_plot, x='model_year', y='price', title='Price vs Model Year', labels={'model_year': 'Model Year', 'price': 'Price (USD)'})
st.plotly_chart(fig_year_price)

st.subheader("Summary Statistics")
st.write(filtered_df.describe())

st.markdown("#### Key Insights")
st.markdown("- Use the filters to narrow down the dataset by model year and odometer readings.")
st.markdown("- Visualize trends between vehicle prices, odometer readings, and model years.")
