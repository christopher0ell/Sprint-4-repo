import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# Title and Introduction
st.title("Vehicle Data Analysis and Visualization")
st.write("""
This Streamlit app loads vehicle data, preprocesses it by filling missing values, 
removes outliers, and provides visual insights into the relationship between 
vehicle model years and prices.
""")

# Data Loading Section
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("### First 5 Rows of the Dataset")
    st.write(df.head())

    # Preprocessing Functions
    def fill_with_median(df, group_col, target_col):
        return df[target_col].fillna(df.groupby(group_col)[target_col].transform('median'))

    # Preprocessing: Filling Missing Values
    df['model_year'] = fill_with_median(df, 'model', 'model_year')
    df['cylinders'] = fill_with_median(df, 'model', 'cylinders')
    df['odometer'] = fill_with_median(df, ['model', 'model_year'], 'odometer')

    st.write("### Data After Preprocessing")
    st.write(df.head())

    # Outlier Removal
    q_low_price = df['price'].quantile(0.01)
    q_high_price = df['price'].quantile(0.99)
    df_filtered = df[(df['price'] >= q_low_price) & (df['price'] <= q_high_price)]

    q_low_year = df['model_year'].quantile(0.01)
    q_high_year = df['model_year'].quantile(0.99)
    df_filtered = df_filtered[(df_filtered['model_year'] >= q_low_year) & (df_filtered['model_year'] <= q_high_year)]

    st.write("### Data After Outlier Removal")
    st.write(df_filtered.head())

    # Scatterplot: Price vs. Model Year
    st.write("### Scatterplot: Price vs. Model Year (Filtered Data)")
    fig, ax = plt.subplots()
    ax.scatter(df_filtered['model_year'], df_filtered['price'], alpha=0.5)
    ax.set_xlabel('Model Year')
    ax.set_ylabel('Price')
    ax.set_title('Scatterplot of Price vs. Model Year (Filtered)')
    st.pyplot(fig)

else:
    st.warning("Please upload a CSV file to proceed.")

