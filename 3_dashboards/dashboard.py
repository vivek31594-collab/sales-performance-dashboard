import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Sales Performance Dashboard", layout="wide")

# ---------------- TITLE ----------------
st.markdown("""
<h1 style='text-align: center; color: #2E86C1;'>
📊 Sales Performance Analytics Dashboard
</h1>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------------- LOAD DATA ----------------
df = pd.read_csv("1_data/processed/cleaned_sales.csv")

# Convert date column
df["Order.Date"] = pd.to_datetime(df["Order.Date"])

# ---------------- SIDEBAR FILTERS ----------------
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

# Filter dataframe
df_selection = df.query(
    "Region == @region_list & Category == @category_list"
)

# ---------------- KPI METRICS ----------------
st.markdown("### 📌 Key Performance Indicators")

total_sales = int(df_selection["Sales"].sum())
total_profit = int(df_selection["Profit"].sum())
total_orders = df_selection["Order.ID"].nunique()

avg_order_value = total_sales / total_orders if total_orders > 0 else 0

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Sales", f"${total_sales:,}")

with col2:
    st.metric("Total Profit", f"${total_profit:,}")

with col3:
    st.metric("Total Orders", total_orders)

with col4:
    st.metric("Avg Order Value", f"${avg_order_value:.2f}")

st.markdown("---")

# ---------------- CHART SECTION ----------------
st.markdown("### 📈 Sales Analysis")

# Sales by Category
fig_category = px.bar(
    df_selection.groupby("Category")["Sales"].sum().reset_index(),
    x="Category",
    y="Sales",
    title="Sales by Category",
    template="plotly_white"
)

# Monthly Sales Trend
sales_trend = df_selection.resample("M", on="Order.Date")["Sales"].sum().reset_index()

fig_trend = px.line(
    sales_trend,
    x="Order.Date",
    y="Sales",
    title="Monthly Sales Trend",
    template="plotly_white"
)

# Display charts
left_chart, right_chart = st.columns(2)

left_chart.plotly_chart(fig_category, use_container_width=True)
right_chart.plotly_chart(fig_trend, use_container_width=True)

# ---------------- TOP PRODUCTS ----------------
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

# ---------------- DATA TABLE ----------------
st.markdown("### 📄 Filtered Dataset")

with st.expander("View Filtered Data Table"):
    st.dataframe(df_selection)

# ---------------- BUSINESS INSIGHTS ----------------
st.markdown("---")
st.markdown("### 📊 Key Business Insights")

st.write("""
• Technology category generates the highest revenue.

• West region contributes significantly to total sales.

• Some products generate high sales but relatively lower profit margins.

• Monthly sales trend helps identify seasonal demand patterns.
""")