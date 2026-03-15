import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="Sales Dashboard", layout="wide")

st.title("📊 Sales Performance Dashboard")

# 1. Load data
df = pd.read_csv("1_data/processed/cleaned_sales.csv")

# 2. Convert date
df["Order.Date"] = pd.to_datetime(df["Order.Date"])

# 3. Sidebar filters
st.sidebar.header("Filters")

region_list = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

category_list = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

# 4. Filter dataframe
df_selection = df.query(
    "Region == @region_list & Category == @category_list"
)

# 5. KPI Metrics
total_sales = int(df_selection["Sales"].sum())
total_profit = int(df_selection["Profit"].sum())
total_orders = df_selection["Order.ID"].nunique()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Sales", f"${total_sales:,}")

with col2:
    st.metric("Total Profit", f"${total_profit:,}")

with col3:
    st.metric("Total Orders", total_orders)

# 6. Visualisations
st.markdown("---")

# Sales by Category (Bar Chart)
fig_category = px.bar(
    df_selection.groupby("Category")["Sales"].sum().reset_index(),
    x="Category",
    y="Sales",
    title="Sales by Category",
    template="plotly_white"
)

# Sales Trend (Line Chart)
sales_trend = df_selection.resample('M', on='Order.Date')['Sales'].sum().reset_index()

fig_trend = px.line(
    sales_trend,
    x="Order.Date",
    y="Sales",
    title="Monthly Sales Trend",
    template="plotly_white"
)

# Display Charts
left_chart, right_chart = st.columns(2)

left_chart.plotly_chart(fig_category, use_container_width=True)
right_chart.plotly_chart(fig_trend, use_container_width=True)

# 7. Top Products Chart
st.markdown("### 🏆 Top 10 Products by Sales")

top_products = (
    df_selection.groupby("Product.Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_products = px.bar(
    top_products,
    x="Sales",
    y="Product.Name",
    orientation="h",
    title="Top 10 Products",
    template="plotly_white"
)

st.plotly_chart(fig_products, use_container_width=True)

# 8. View Filtered Data
with st.expander("View Filtered Data Table"):
    st.dataframe(df_selection)

