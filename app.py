# app.py (formally streamlit_dashboard.py)

# 1. Import necessary libraries
import streamlit as st
import pandas as pd
import plotly.express as px

# 2. Load the dataset into a DataFrame and clean the data
df = pd.read_csv("vehicles_us.csv")

# Ensure 'price' column is numeric, replacing invalid values with 0
df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0).astype(int)

# Ensure 'odometer' column is numeric, replacing invalid values with 0
df['odometer'] = pd.to_numeric(df['odometer'], errors='coerce').fillna(0).astype(int)

# 3. Title and Introduction
st.title("Vehicle Data Exploratory Dashboard")
st.markdown("### Use this dashboard to explore vehicle data interactively.")

# 4. Sidebar Filters
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

# 5. Filter DataFrame based on sidebar input
filtered_df = df[
    (df['model_year'].between(*model_year)) &
    (df['odometer'] <= odometer_limit)
]

# 6. Add a checkbox to switch between showing all data and filtered data
show_all_data = st.checkbox("Show All Data", value=False)

# Filter the DataFrame based on user input or show all data
data_to_plot = df if show_all_data else filtered_df

# 7. Display Filtered Data
st.subheader("Filtered Data Preview")
st.write(data_to_plot.head())  # Show first few rows

# 8. Plot: Price Distribution
st.subheader("Price Distribution")
fig_price = px.histogram(data_to_plot, x='price', nbins=50, title='Distribution of Prices')
st.plotly_chart(fig_price)

# 9. Scatter Plot: Price vs Odometer
st.subheader("Scatter Plot: Price vs Odometer")
fig_scatter = px.scatter(
    data_to_plot, x='odometer', y='price',
    title='Price vs Odometer',
    labels={'odometer': 'Odometer Reading', 'price': 'Price (USD)'}
)
st.plotly_chart(fig_scatter)

# 10. Scatter Plot: Price vs Model Year
st.subheader("Scatter Plot: Price vs Model Year")
fig_year_price = px.scatter(
    data_to_plot, x='model_year', y='price',
    title='Price vs Model Year',
    labels={'model_year': 'Model Year', 'price': 'Price (USD)'}
)
st.plotly_chart(fig_year_price)

# 11. Display Summary Statistics
st.subheader("Summary Statistics")
st.write(data_to_plot.describe())

# 12. Insights Section (Markdown)
st.markdown("#### Key Insights")
st.markdown("- Use the filters to narrow down the dataset by model year and odometer readings.")
st.markdowndel years.")
e trends between vehicle prices, odometer readings, and model years.")