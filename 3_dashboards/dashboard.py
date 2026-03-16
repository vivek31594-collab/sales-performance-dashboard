import streamlit as st
import pandas as pd
import plotly.express as px
from prophet import Prophet

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Sales Performance Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("1_data/processed/cleaned_sales.csv")
    df["Order.Date"] = pd.to_datetime(df["Order.Date"])
    return df

df = load_data()

# ---------------- TITLE ----------------
st.markdown("""
<h1 style='text-align: center; color: #2E86C1;'>
📊 Sales Performance Analytics Dashboard
</h1>
""", unsafe_allow_html=True)
st.markdown("---")

# ---------------- SIDEBAR ----------------
st.sidebar.title("🔎 Dashboard Filters")

# Date filter
min_date = df["Order.Date"].min()
max_date = df["Order.Date"].max()
date_range = st.sidebar.date_input(
    "Select Date Range",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Region filter
region_list = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

# Category filter
category_list = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

# Top N Products selection
top_n = st.sidebar.slider("Select Top N Products", min_value=5, max_value=20, value=10)

# ---------------- FILTER DATA ----------------
df_selection = df[
    (df["Region"].isin(region_list)) &
    (df["Category"].isin(category_list)) &
    (df["Order.Date"] >= pd.to_datetime(date_range[0])) &
    (df["Order.Date"] <= pd.to_datetime(date_range[1]))
]

if df_selection.empty:
    st.warning("No data available for selected filters.")
    st.stop()

# ---------------- KPI METRICS ----------------
st.markdown("## 📌 Key Performance Indicators")

total_sales = df_selection["Sales"].sum()
total_profit = df_selection["Profit"].sum()
total_orders = df_selection["Order.ID"].nunique()
avg_order_value = total_sales / total_orders
profit_margin = (total_profit / total_sales) * 100

# YoY Growth (if data spans multiple years)
df_selection['Year'] = df_selection['Order.Date'].dt.year
sales_by_year = df_selection.groupby('Year')['Sales'].sum()
yoy_growth = sales_by_year.pct_change().iloc[-1] if len(sales_by_year) > 1 else 0

# Category profit %
category_profit = (df_selection.groupby('Category')['Profit'].sum() /
                   df_selection.groupby('Category')['Sales'].sum() * 100).reset_index()
category_profit.columns = ['Category', 'Profit_Percent']

# Region contribution %
region_contribution = (df_selection.groupby('Region')['Sales'].sum() / total_sales * 100).reset_index()
region_contribution.columns = ['Region', 'Contribution_Percent']

col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("💰 Total Sales", f"${total_sales:,.0f}")
col2.metric("📈 Total Profit", f"${total_profit:,.0f}")
col3.metric("🛒 Total Orders", total_orders)
col4.metric("💳 Avg Order Value", f"${avg_order_value:,.2f}")
col5.metric("📊 Profit Margin", f"{profit_margin:.2f}%")
col6.metric("📈 YoY Growth", f"{yoy_growth:.2%}")

st.markdown("---")

# ---------------- EXECUTIVE SUMMARY ----------------
st.markdown("## 📄 Executive Summary")
st.markdown("""
- Technology category generates the highest revenue.
- West region contributes significantly to total sales.
- Some products generate high sales but relatively lower profit margins.
- Monthly trends show seasonal demand fluctuations.
- Corporate segment contributes strongly to revenue.
""")

# ---------------- CHARTS ----------------
st.markdown("## 📈 Sales Analysis")

# Sales by Category
sales_category = df_selection.groupby("Category")["Sales"].sum().sort_values(ascending=False).reset_index()
fig_category = px.bar(
    sales_category,
    x="Category",
    y="Sales",
    color="Category",
    title="Sales by Category",
    template="plotly_white"
)

# Monthly Sales Trend
sales_trend = df_selection.resample("M", on="Order.Date")["Sales"].sum().reset_index()
fig_trend = px.line(
    sales_trend,
    x="Order.Date",
    y="Sales",
    markers=True,
    title="Monthly Sales Trend",
    template="plotly_white"
)

# Layout: side by side
left_chart, right_chart = st.columns(2)
left_chart.plotly_chart(fig_category, use_container_width=True)
right_chart.plotly_chart(fig_trend, use_container_width=True)

# ---------------- SALES FORECAST ----------------
st.markdown("## 🔮 6-Month Sales Forecast")
forecast_df = df_selection.groupby("Order.Date")["Sales"].sum().reset_index()
forecast_df.rename(columns={"Order.Date": "ds", "Sales": "y"}, inplace=True)

if len(forecast_df) < 2:
    st.warning("Not enough data to generate a 6-month sales forecast. Try adjusting the filters.")
else:
    model = Prophet(yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False)
    model.fit(forecast_df)

    future = model.make_future_dataframe(periods=6, freq='M')
    forecast = model.predict(future)

    fig_forecast = px.line(
        forecast,
        x="ds",
        y="yhat",
        title="Sales Forecast (Next 6 Months)",
        template="plotly_white"
    )
    fig_forecast.add_traces([
        px.line(forecast, x='ds', y='yhat_upper', line=dict(color='lightgreen', dash='dash')).data[0],
        px.line(forecast, x='ds', y='yhat_lower', line=dict(color='lightcoral', dash='dash')).data[0]
    ])
    st.plotly_chart(fig_forecast, use_container_width=True)

    with st.expander("View Forecast Data"):
        st.dataframe(forecast[['ds','yhat','yhat_lower','yhat_upper']].tail(12))

# ---------------- REGION SALES ----------------
st.markdown("## 🌍 Sales by Region")
fig_region = px.bar(
    region_contribution,
    x="Region",
    y="Contribution_Percent",
    color="Region",
    title="Region Contribution % to Total Sales",
    template="plotly_white"
)
st.plotly_chart(fig_region, use_container_width=True)

# ---------------- PROFIT TREND ----------------
st.markdown("## 💹 Monthly Profit Trend")
profit_trend = df_selection.resample("M", on="Order.Date")["Profit"].sum().reset_index()
fig_profit = px.line(
    profit_trend,
    x="Order.Date",
    y="Profit",
    markers=True,
    title="Monthly Profit Trend",
    template="plotly_white"
)
st.plotly_chart(fig_profit, use_container_width=True)

# ---------------- TOP PRODUCTS ----------------
st.markdown(f"## 🏆 Top {top_n} Products by Sales")
top_products = df_selection.groupby("Product.Name")["Sales"].sum().sort_values(ascending=False).head(top_n).reset_index()
fig_products = px.bar(
    top_products,
    x="Sales",
    y="Product.Name",
    orientation="h",
    color="Sales",
    title=f"Top {top_n} Products",
    template="plotly_white"
)
st.plotly_chart(fig_products, use_container_width=True)

# ---------------- SUB-CATEGORY PIE CHART ----------------
st.markdown("## 👥 Sales Distribution by Sub-Category")
sales_subcat_pie = df_selection.groupby("Sub.Category")["Sales"].sum().reset_index()
fig_subcat_pie = px.pie(
    sales_subcat_pie,
    names="Sub.Category",
    values="Sales",
    title="Sales % by Sub-Category",
    hole=0.4
)
st.plotly_chart(fig_subcat_pie, use_container_width=True)

# ---------------- DOWNLOAD BUTTON ----------------
st.download_button(
    label="📥 Download Filtered Data",
    data=df_selection.to_csv(index=False),
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)

# ---------------- DATA TABLE ----------------
st.markdown("## 📄 Filtered Dataset")
with st.expander("View Data"):
    st.dataframe(df_selection)

# ---------------- FOOTER ----------------
st.markdown("""
---
📊 **Sales Performance Dashboard**  
Created by **Vivek Saha**  
Data Analyst Portfolio Project
""")