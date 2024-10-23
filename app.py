# app.py (using Fastparquet for DataFrame management)

# 1. Import necessary libraries
import streamlit as st
import pandas as pd
import plotly.express as px

# 2. Load the dataset into a DataFrame and clean the data
df = pd.read_csv("vehicles_us.csv")

# Clean 'price' column: Ensure numeric with no problematic values
df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0).astype('float64')
df['price'] = df['price'].clip(lower=0)  # Ensure no negative prices

# Clean 'odometer' column: Ensure numeric with no problematic values
df['odometer'] = pd.to_numeric(df['odometer'], errors='coerce').fillna(0).astype('float64')
df['odometer'] = df['odometer'].clip(lower=0)  # Ensure no negative values

# 3. Save DataFrame to Parquet using Fastparquet
df.to_parquet("vehicles_us.parquet", engine='fastparquet')

# 4. Read the Parquet file back using Fastparquet
try:
    df = pd.read_parquet("vehicles_us.parquet", engine='fastparquet')
    st.write("Fastparquet conversion successful!")
except Exception as e:
    st.write(f"Fastparquet conversion failed: {e}")

# 5. Title and Introduction
st.title("Vehicle Data Exploratory Dashboard")
st.markdown("### Use this dashboard to explore vehicle data interactively.")

# 6. Sidebar Filters
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

# 7. Filter DataFrame based on sidebar input
filtered_df = df[
    (df['model_year'].between(*model_year)) &
    (df['odometer'] <= odometer_limit)
]

# 8. Add a checkbox to switch between showing all data and filtered data
show_all_data = st.checkbox("Show All Data", value=False)

# Use filtered data or full data based on the checkbox
data_to_plot = df if show_all_data else filtered_df

# 9. Display Filtered Data
st.subheader("Filtered Data Preview")
st.write(data_to_plot.head())  # Show first few rows

# 10. Plot: Price Distribution
st.subheader("Price Distribution")
fig_price = px.histogram(data_to_plot, x='price', nbins=50, title='Distribution of Prices')
st.plotly_chart(fig_price)

# 11. Scatter Plot: Price vs Odometer
st.subheader("Scatter Plot: Price vs Odometer")
fig_scatter = px.scatter(
    data_to_plot, x='odometer', y='price',
    title='Price vs Odometer',
    labels={'odometer': 'Odometer Reading', 'price': 'Price (USD)'}
)
st.plotly_chart(fig_scatter)

# 12. Scatter Plot: Price vs Model Year
st.subheader("Scatter Plot: Price vs Model Year")
fig_year_price = px.scatter(
    data_to_plot, x='model_year', y='price',
    title='Price vs Model Year',
    labels={'model_year': 'Model Year', 'price': 'Price (USD)'}
)
st.plotly_chart(fig_year_price)

# 13. Display Summary Statistics
st.subheader("Summary Statistics")
st.write(filtered_df.describe())

# 14. Insights Section (Markdown)
st.markdown("#### Key Insights")
st.markdown("- Use the filters to narrow down the dataset by model year and odometer readings.")
st.markdown("- Visualize trends between vehicle prices, odometer readings, and model years.")
