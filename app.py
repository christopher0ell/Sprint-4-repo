# app.py (formally streamlit_dashboard.py)

import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset (Ensure vehicles_us.csv is in the same directory or provide the correct path)
df = pd.read_csv('vehicles_us.csv')

# Clean and preprocess the 'price' column
df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0).astype('int64')

# Header
st.header("Vehicle Data Analysis App")

# Display the first few rows of the DataFrame
st.write("Here are the first 5 rows of the dataset:")
st.write(df.head())

# Histogram of vehicle prices
st.subheader("Histogram: Distribution of Vehicle Prices")
fig_price = px.histogram(df, x='price', nbins=50, title='Distribution of Vehicle Prices')
st.plotly_chart(fig_price)

# Scatter plot: Vehicle Price vs. Model Year
st.subheader("Scatter Plot: Vehicle Price vs Model Year")
fig_price_year = px.scatter(
    df, x='model_year', y='price',
    title='Vehicle Price vs Model Year',
    labels={'model_year': 'Model Year', 'price': 'Price (USD)'}
)
st.plotly_chart(fig_price_year)

# Checkbox to show/hide additional scatter plot
if st.checkbox("Show Scatter Plot: Vehicle Price vs Odometer Reading"):
    st.subheader("Scatter Plot: Vehicle Price vs Odometer Reading")
    fig_price_odometer = px.scatter(
        df, x='odometer', y='price',
        title='Vehicle Price vs Odometer Reading',
        labels={'odometer': 'Odometer Reading', 'price': 'Price (USD)'}
    )
    st.plotly_chart(fig_price_odometer)

# Footer text
st.write("This is a simple vehicle data exploration app built with Streamlit.")
