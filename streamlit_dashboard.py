# streamlit_dashboard.py

# 1. Import necessary libraries
import streamlit as st
import pandas as pd
import plotly.express as px

# 2. Load the dataset into a DataFrame
df = pd.read_csv("vehicles_us.csv")

# 3. Add a header
st.header("Interactive Vehicle Data Dashboard")

# 4. Sidebar Filters
st.sidebar.header("Filter Options")

# Slider to filter by model year
model_year = st.sidebar.slider(
    "Select Model Year Range", 
    int(df['model_year'].min()), 
    int(df['model_year'].max()), 
    (2000, 2019)
)

# Slider to limit odometer readings
odometer_limit = st.sidebar.slider(
    "Odometer Limit (Max)", 
    0, 
    int(df['odometer'].max()), 
    100000
)

# 5. Add a checkbox to switch between showing all data and filtered data
show_all_data = st.checkbox("Show All Data", value=False)

# Filter the DataFrame based on user input or show all data
if show_all_data:
    data_to_plot = df
else:
    data_to_plot = df[(df['model_year'].between(*model_year)) & (df['odometer'] <= odometer_limit)]

# 6. Display Data Preview
st.subheader("Data Preview")
st.write(data_to_plot.head())  # Show first few rows

# 7. Plot: Price Distribution Histogram
st.subheader("Price Distribution")
fig_price = px.histogram(data_to_plot, x='price', nbins=50, title='Distribution of Vehicle Prices')
st.plotly_chart(fig_price)

# 8. Scatter Plot: Price vs Odometer
st.subheader("Price vs Odometer Scatter Plot")
fig_scatter = px.scatter(
    data_to_plot, 
    x='odometer', 
    y='price', 
    title='Price vs Odometer', 
    labels={'odometer': 'Odometer Reading', 'price': 'Price (USD)'}
)
st.plotly_chart(fig_scatter)

# 9. Scatter Plot: Price vs Model Year
st.subheader("Price vs Model Year Scatter Plot")
fig_year_price = px.scatter(
    data_to_plot, 
    x='model_year', 
    y='price', 
    title='Price vs Model Year', 
    labels={'model_year': 'Model Year', 'price': 'Price (USD)'}
)
st.plotly_chart(fig_year_price)
