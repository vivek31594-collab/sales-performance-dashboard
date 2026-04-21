import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os

# =====================================================
# ⚙️ PAGE CONFIG (MUST BE FIRST STREAMLIT COMMAND)
# =====================================================
st.set_page_config(
    page_title="Executive Sales Intelligence System",
    page_icon="📊",
    layout="wide"
)

sns.set_style("whitegrid")

# =====================================================
# 📥 LOAD DATA (ONLY ONCE)
# =====================================================
@st.cache_data
def load_data():
    file_path = "1_data/processed/cleanedsales.csv"

    if not os.path.exists(file_path):
        st.error("❌ Dataset not found. Check file path.")
        st.stop()

    df = pd.read_csv(file_path, encoding="cp1252", low_memory=False)

    df["Order.Date"] = pd.to_datetime(df["Order.Date"], errors="coerce")
    df = df.dropna(subset=["Order.Date"])

    for col in ["Sales", "Profit", "Discount"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df["Year_Month"] = df["Order.Date"].dt.to_period("M").astype(str)

    return df


df = load_data()

# =====================================================
# 🧭 TITLE
# =====================================================
st.title("📊 Sales Performance Dashboard")
st.markdown("### Business Intelligence & Insights Overview")

st.markdown("---")

# =====================================================
# 📌 EXECUTIVE SUMMARY (TOP SECTION)
# =====================================================
st.markdown("## 📌 Executive Summary Insights")

total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
profit_margin = (total_profit / total_sales * 100) if total_sales else 0

c1, c2, c3 = st.columns(3)
c1.metric("💰 Total Sales", f"{total_sales:,.0f}")
c2.metric("📈 Total Profit", f"{total_profit:,.0f}")
c3.metric("📊 Profit Margin", f"{profit_margin:.2f}%")

st.markdown("""
### 🔎 Key Business Insights
- 📊 West region contributes highest revenue but lower margin stability  
- 📉 Certain categories show high sales but negative profit impact  
- ⚠️ Few products are dragging overall profitability down  
""")

st.markdown("---")

# =====================================================
# ⚠️ LOSS-MAKING PRODUCTS
# =====================================================
st.markdown("## ⚠️ Loss-Making Products Analysis")

loss_df = df[df["Profit"] < 0]

top_loss = loss_df.groupby("Product.Name")["Profit"].sum().sort_values().head(10)

st.bar_chart(top_loss)

st.markdown(f"### Total Loss Impact: {loss_df['Profit'].sum():,.0f}")

st.markdown("---")

# =====================================================
# 📈 TREND ANALYSIS
# =====================================================
st.markdown("## 📈 Sales & Profit Trend Analysis")

monthly_sales = df.groupby("Year_Month")["Sales"].sum()
monthly_profit = df.groupby("Year_Month")["Profit"].sum()

st.markdown("### 📊 Monthly Sales Trend")
st.line_chart(monthly_sales)

st.markdown("### 📊 Monthly Profit Trend")
st.line_chart(monthly_profit)

st.markdown("""
### 🔎 Trend Insights
- 📈 Sales fluctuate across months  
- 💰 Profit does not always follow sales trend  
- ⚠️ Some months show high sales but low profitability  
- 🎯 Indicates pricing/discount optimization required  
""")

st.markdown("---")

# =====================================================
# 🔍 FILTERS (MAIN ANALYTICS SECTION)
# =====================================================
st.sidebar.header("Filters")

date_range = st.sidebar.date_input(
    "Date Range",
    [df["Order.Date"].min(), df["Order.Date"].max()]
)

region = st.sidebar.multiselect(
    "Region",
    df["Region"].dropna().unique(),
    df["Region"].dropna().unique()
)

category = st.sidebar.multiselect(
    "Category",
    df["Category"].dropna().unique(),
    df["Category"].dropna().unique()
)

filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category)) &
    (df["Order.Date"] >= pd.to_datetime(date_range[0])) &
    (df["Order.Date"] <= pd.to_datetime(date_range[1]))
]

if filtered_df.empty:
    st.warning("No data available for selected filters")
    st.stop()

# =====================================================
# 📊 KPI DASHBOARD (FILTERED)
# =====================================================
sales = filtered_df["Sales"].sum()
profit = filtered_df["Profit"].sum()
orders = filtered_df["Order.ID"].nunique()

aov = sales / orders if orders else 0
margin = (profit / sales * 100) if sales else 0

monthly = filtered_df.groupby("Year_Month")["Sales"].sum().reset_index()
growth = monthly["Sales"].pct_change().iloc[-1] * 100 if len(monthly) > 1 else 0

st.subheader("📊 Live KPI Dashboard")

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Sales", f"₹{sales:,.0f}", f"{growth:.2f}% MoM")
c2.metric("Profit", f"₹{profit:,.0f}")
c3.metric("Orders", orders)
c4.metric("AOV", f"₹{aov:,.2f}")
c5.metric("Margin", f"{margin:.2f}%")

st.markdown("---")

# =====================================================
# 📈 VISUALS
# =====================================================
fig1 = px.line(monthly, x="Year_Month", y="Sales", markers=True, title="Monthly Sales Trend")
st.plotly_chart(fig1, use_container_width=True)

# =====================================================
# 📊 REGION ANALYSIS
# =====================================================
st.subheader("📊 Sales by Region")

region_sales = filtered_df.groupby("Region")["Sales"].sum().sort_values()

fig2, ax2 = plt.subplots(figsize=(10,5))
sns.barplot(x=region_sales.values, y=region_sales.index, ax=ax2)
st.pyplot(fig2)

# =====================================================
# 📊 SUB-CATEGORY PROFIT
# =====================================================
st.subheader("📊 Profit by Sub-Category")

subcat_profit = filtered_df.groupby("Sub.Category")["Profit"].sum().sort_values()

fig3, ax3 = plt.subplots(figsize=(12,6))
sns.barplot(x=subcat_profit.values, y=subcat_profit.index, ax=ax3)

st.pyplot(fig3)

# =====================================================
# 📦 TOP PRODUCTS
# =====================================================
st.subheader("📦 Top Products")

top_products = filtered_df.groupby("Product.Name")["Sales"].sum().sort_values(ascending=False).head(10)

fig4, ax4 = plt.subplots(figsize=(10,5))
sns.barplot(x=top_products.values, y=top_products.index, ax=ax4)

st.pyplot(fig4)

# =====================================================
# 🚨 LOSS TRANSACTIONS
# =====================================================
st.subheader("🚨 Loss Transactions")

st.dataframe(filtered_df[filtered_df["Profit"] < 0][["Product.Name", "Sales", "Profit"]].head(10))

# =====================================================
# 📌 ACTIONS
# =====================================================
st.subheader("📌 Business Actions")

if margin < 15:
    st.write("• Improve pricing strategy")

if len(loss_df) > 0:
    st.write("• Fix loss-making products")

if growth < 0:
    st.write("• Improve sales growth strategy")

# =====================================================
# 📌 RECOMMENDATIONS
# =====================================================
st.markdown("## 📌 Business Recommendations")

low_margin = df[df["Profit"] / df["Sales"] < 0.1]

st.write("🔴 Reduce focus on loss-making products immediately.")
st.write("📊 Optimize pricing and discount strategy.")
st.write("🚚 Improve logistics cost efficiency.")
st.write("🎯 Focus on high-profit categories.")

# =====================================================
# 📥 DOWNLOAD
# =====================================================
st.download_button(
    "📥 Download Data",
    filtered_df.to_csv(index=False),
    "sales_data.csv",
    mime="text/csv"
)

st.caption("🚀 PwC-Level Executive Sales Intelligence Dashboard")