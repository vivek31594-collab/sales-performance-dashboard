import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os

# =====================================================
# ⚙️ PAGE CONFIG (MUST BE FIRST)
# =====================================================
st.set_page_config(
    page_title="Sales Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)

sns.set_style("whitegrid")

# =====================================================
# 📥 LOAD DATA
# =====================================================
@st.cache_data
def load_data():
    file_path = "1_data/processed/cleanedsales.csv"

    if not os.path.exists(file_path):
        st.error("Dataset not found. Check file path in repo.")
        st.stop()

    df = pd.read_csv(file_path, encoding="cp1252", low_memory=False)

    # Date conversion
    df["Order.Date"] = pd.to_datetime(df["Order.Date"], errors="coerce")
    df = df.dropna(subset=["Order.Date"])

    # Numeric cleaning
    for col in ["Sales", "Profit", "Discount"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df


df = load_data()

# =====================================================
# 🧭 HEADER
# =====================================================
st.title("📊 Sales Intelligence Dashboard")
st.markdown("### Business Performance + Insights + Analytics (PwC Style)")

st.markdown("---")

# =====================================================
# 📌 KPI SUMMARY
# =====================================================
st.markdown("## 📌 Business KPIs")

total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
orders = df["Order.ID"].nunique()
profit_margin = (total_profit / total_sales * 100) if total_sales else 0
aov = total_sales / orders if orders else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("💰 Sales", f"{total_sales:,.0f}")
c2.metric("📈 Profit", f"{total_profit:,.0f}")
c3.metric("🛒 Orders", orders)
c4.metric("📊 Margin", f"{profit_margin:.2f}%")

st.markdown("---")

# =====================================================
# ⚠️ LOSS ANALYSIS
# =====================================================
st.markdown("## ⚠️ Loss-Making Products Analysis")

loss_df = df[df["Profit"] < 0]

top_loss = (
    loss_df.groupby("Product.Name")["Profit"]
    .sum()
    .sort_values()
    .head(10)
)

st.bar_chart(top_loss)

st.markdown(f"### Total Loss Impact: {loss_df['Profit'].sum():,.0f}")

st.markdown("---")

# =====================================================
# 📈 TREND ANALYSIS (FIXED)
# =====================================================
st.markdown("## 📈 Sales & Profit Trend Over Time")

monthly = (
    df.groupby(pd.Grouper(key="Order.Date", freq="M"))
    .agg({"Sales": "sum", "Profit": "sum"})
    .sort_index()
)

monthly.index = monthly.index.to_period("M").astype(str)

st.line_chart(monthly["Sales"])
st.line_chart(monthly["Profit"])

st.markdown("---")

# =====================================================
# 📊 PLOT 1: SALES BY REGION
# =====================================================
st.markdown("## 📊 Sales by Region")

region_sales = df.groupby("Region")["Sales"].sum().sort_values()

fig1, ax1 = plt.subplots(figsize=(10,5))
sns.barplot(x=region_sales.values, y=region_sales.index, ax=ax1)
ax1.set_title("Sales by Region")
st.pyplot(fig1)

# =====================================================
# 📊 PLOT 2: PROFIT BY CATEGORY
# =====================================================
st.markdown("## 📊 Profit by Category")

category_profit = df.groupby("Category")["Profit"].sum().sort_values()

fig2, ax2 = plt.subplots(figsize=(8,4))
sns.barplot(x=category_profit.values, y=category_profit.index, ax=ax2)
ax2.set_title("Profit by Category")
st.pyplot(fig2)

# =====================================================
# 📊 PLOT 3: TOP PRODUCTS
# =====================================================
st.markdown("## 📦 Top Products by Sales")

top_products = df.groupby("Product.Name")["Sales"].sum().sort_values(ascending=False).head(10)

fig3, ax3 = plt.subplots(figsize=(10,5))
sns.barplot(x=top_products.values, y=top_products.index, ax=ax3)
ax3.set_title("Top Products")
st.pyplot(fig3)

# =====================================================
# 📊 PLOT 4: SALES vs PROFIT RELATIONSHIP
# =====================================================
st.markdown("## 📊 Sales vs Profit Relationship")

fig4 = px.scatter(
    df,
    x="Sales",
    y="Profit",
    color="Category",
    title="Sales vs Profit"
)

st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# =====================================================
# 🧠 BUSINESS INSIGHTS ENGINE
# =====================================================
st.markdown("## 🧠 Key Business Insights")

insights = []

if profit_margin < 10:
    insights.append("⚠️ Low profit margin indicates pricing or cost inefficiency.")
else:
    insights.append("✅ Healthy profit margin indicates stable business performance.")

if len(loss_df) > 0:
    loss_ratio = abs(loss_df["Profit"].sum()) / total_profit
    if loss_ratio > 0.3:
        insights.append("🚨 High losses impacting profitability significantly.")
    else:
        insights.append("⚠️ Limited loss-making products detected.")

growth = monthly["Sales"].pct_change().iloc[-1] * 100 if len(monthly) > 1 else 0

if growth < 0:
    insights.append("📉 Sales are declining in recent months.")
else:
    insights.append("📈 Sales show positive growth trend.")

for i, ins in enumerate(insights, 1):
    st.write(f"{i}. {ins}")

st.markdown("---")

# =====================================================
# 📌 BUSINESS RECOMMENDATIONS
# =====================================================
st.markdown("## 📌 Recommendations")

st.write("• Optimize pricing strategy for low-margin segments")
st.write("• Reduce or fix loss-making products")
st.write("• Focus marketing on high-performing categories")
st.write("• Improve regional underperforming areas")

st.markdown("---")

# =====================================================
# 📥 DOWNLOAD DATA
# =====================================================
st.download_button(
    "📥 Download Clean Data",
    df.to_csv(index=False),
    "sales_data.csv",
    mime="text/csv"
)

st.caption("🚀 Professional Sales Intelligence Dashboard (PwC-Level)")