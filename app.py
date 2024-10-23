# app.py (using Fastparquet for DataFrame management)

import os
import streamlit as st
import pandas as pd
import plotly.express as px

# Disable PyArrow usage to prevent conflicts
os.environ["PYARROW_IGNORE_IMPORT"] = "1"

# 1. Load the dataset into a DataFrame and clean the data
df = pd.read_csv("vehicles_us.csv")

# 2. Clean 'price' column: Ensure numeric with no problematic values
df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0).clip(lower=0).astype('float64')

# 3. Clean 'odometer' column: Ensure numeric with no problematic values
df['odometer'] = pd.to_numeric(df['odometer'], errors='coerce').fillna(0).clip(lower=0).astype('float64')

# 4. Reset index to avoid index-related errors during conversion
df = df.reset_index(drop=True)

# 5. Save DataFrame to Parquet using Fastparquet
df.to_parquet("vehicles_us.parquet", engine='fastparquet')

# 6. Read the Parquet file back using Fastparquet with error handling
try:
    df = pd.read_parquet("vehicles_us.parquet", engine='fastparquet')
    st.write("Fastparquet conversion successful!")
except Exception as e:
    st.write(f"Fastparquet conversion failed: {e}")

# 7. Title and Introduction
st.title("Vehicle Data Exploratory Dashboard")
st.markdown("### Use this dashboard to explore vehicle data interactively.")

# 8. Sidebar Filters
st.sidebar.header("Filter Options")

# Slider to filter by model year
model_year = st.sidebar.slider(
    "Select Model Year Range",
    int(df['model_year'].min()),
    int(df['model_year'].max()),
    (2000, 2019)
)

# Slider to limit the odometer readings
odometer_limit = st.sidebar.slider(
    "Odometer Limit (Max)",
    0,
    int(df['odometer'].max()),
    100000
)

# 9. Filter DataFrame based on sidebar input
filtered_df = df[
    (df['model_year'].between(*model_year)) &
    (df['odometer'] <= odometer_limit)
]

# 10. Add a checkbox to switch between showing all data and filtered data
show_all_data = st.checkbox("Show All Data", value=False)

# Use filtered data or full data based on the checkbox
data_to_plot = df if show_all_data else filtered_df

# 11. Validate 'price' column for any invalid or infinite values
invalid_price = data_to_plot[~data_to_plot['price'].apply(lambda x: isinstance(x, (int, float)))]
if not invalid_price.empty:
    st.write("Invalid 'price' entries found:")
    st.write(invalid_price)

# Replace infinity values with NaN, and fill NaNs with 0
data_to_plot.replace([float('inf'), -float('inf')], pd.NA, inplace=True)
data_to_plot.fillna(0, inplace=True)

# 12. Display Filtered Data
st.subheader("Filtered Data Preview")
st.dataframe(data_to_plot.astype('object'))  # Use object dtype to prevent PyArrow conversion issues

# 13. Plot: Price Distribution
st.subheader("Price Distribution")
fig_price = px.histogram(data_to_plot, x='price', nbins=50, title='Distribution of Prices')
st.plotly_chart(fig_price)

# 14. Scatter Plot: Price vs Odometer
st.subheader("Scatter Plot: Price vs Odometer")
fig_scatter = px.scatter(
    data_to_plot, x='odometer', y='price',
    title='Price vs Odometer',
    labels={'odometer': 'Odometer Reading', 'price': 'Price (USD)'}
)
st.plotly_chart(fig_scatter)

# 15. Scatter Plot: Price vs Model Year
st.subheader("Scatter Plot: Price vs Model Year")
fig_year_price = px.scatter(
    data_to_plot, x='model_year', y='price',
    title='Price vs Model Year',
    labels={'model_year': 'Model Year', 'price': 'Price (USD)'}
)
st.plotly_chart(fig_year_price)

# 16. Display Summary Statistics
st.subheader("Summary Statistics")
st.write(filtered_df.describe())

# 17. Insights Section (Markdown)
st.markdown("#### Key Insights")
st.markdown("- Use the filters to narrow down the dataset by model year and odometer readings.")
st.markdown("- Visualize trends between vehicle prices, odometer readings, and model years.")
