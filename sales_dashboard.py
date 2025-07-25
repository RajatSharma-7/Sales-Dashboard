  # -*- coding: utf-8 -*-
"""Sales Dashboard.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1yLy-8yp1w1Z47kCfFhNpFEwioyKjtU0a
"""

import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt

file_path = "D:\8. Projects\Python\Sales Dashboard\Superstore_Data.csv"
df = pd.read_csv(file_path,encoding = 'latin1')
df.head()

def load_data():
  df = pd.read_csv("Superstore_Data.csv",encoding = 'latin1')
  df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
  df['Month'] = df['Order Date'].dt.to_period('M').dt.to_timestamp()
  df.dropna(subset=['Order Date','Sales','Profit','Quantity'],inplace = True)
  return df

df = load_data()

# Title
st.title("Superstore Sales Dashboard")

# Filters
region = st.selectbox("Select Region",['All']+sorted(df['Region'].dropna().unique().tolist()))
if region != 'All':
  df = df[df['Region'] == region]

# KPIs
total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()
total_orders = df['Order ID'].nunique()

st.metric("Total Sales", f"${total_sales:,.2f}")
st.metric("Total Orders", total_orders)
st.metric("Total Profit",f"${total_profit:,.2f}")

# Monthly sales
monthly_sales = df.groupby('Month')['Sales'].sum().reset_index()
fig1 = px.line(monthly_sales, x = 'Month',y='Sales',title = 'Monthly Sales Trend')
st.plotly_chart(fig1)

# Top 10 Products
top_products = df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(10).reset_index()
fig2 = px.bar(top_products, x='Product Name', y='Sales', title='Top 10 Products by Sales')
st.plotly_chart(fig2)


# Category Wise Sales
cat_sales = df.groupby('Category')['Sales'].sum().reset_index()
fig3 = px.pie(cat_sales,names = 'Category',values = 'Sales',title='Sales by category')
st.plotly_chart(fig3)


# Region-Wise Sales (IF NOT FILTERED)
if region == 'All':
  region_sales = df.groupby('Region')['Sales'].sum().reset_index()
  fig4 = px.bar(region_sales, x='Region',y='Sales',title='Sales by Region')
  st.plotly_chart(fig4)


# Optional: Show Raw Data
if st.checkbox("Show Raw Data"):
  st.dataframe(df)