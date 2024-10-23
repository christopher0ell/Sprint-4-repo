# app.py (formally streamlit_dashboard.py)

# 1. Import necessary libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import pyarrow as pa  # Import PyArrow for conversion testing

# 2. Load the dataset into a DataFrame and clean the data
df = pd.read_csv("vehicles_us.csv")

# Clean 'price' column: Ensure numeric with no problematic values
df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0).astype('int64')
df['price'] = df['price'].clip(lower=0)  # Ensure no negative prices

# Debug: Display data types and the first few rows to verify data integrity
st.write("Data Types:")
st.write(df.dtypes)
st.write("Sample Data:")
st.write(df.head())

# Test PyArrow conversion to ensure compatibility before passing to Streamlit
try:
    table = pa.Table.from_pandas(df)
    st.write("PyArrow conversion successful!")
except Exception as e:
    st.write(f"PyArrow conversion failed: {e}")

# 3. Plot a simple chart using Plotly Express
fig = px.histogram(df, x='price', nbins=50, title='Distribution of Vehicle Prices')

# 4. Display the chart and the data in Streamlit
st.write("Vehicle Price Distribution")
st.plotly_chart(fig)

st.write("DataFrame:")
st.dataframe(df)  # Show the DataFrame in the Streamlit app
