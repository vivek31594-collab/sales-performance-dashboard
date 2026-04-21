import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os

# =====================================================
# ⚙️ CONFIG (MUST BE FIRST)
# =====================================================
st.set_page_config(
    page_title="Executive Sales Intelligence System",
    page_icon="📊",
    layout="wide"
)

sns.set_style("whitegrid")

# =====================================================
# 📥 DATA LOAD (STABLE + DEPLOYMENT SAFE)
# =====================================================
@st.cache_data
def load_data():
    file_path = "1_data/processed/cleanedsales.csv"

    if not os.path.exists(file_path):
        st.error("Dataset not found. Check repository structure.")
        st.stop()

    df = pd.read_csv(file_path, encoding="cp1252")

    df["Order.Date"] = pd.to_datetime(df["Order.Date"], errors="coerce")
    df = df.dropna(subset=["Order.Date"])

    for col in ["Sales", "Profit", "Discount"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df


df = load_data().sort_values("Order.Date")

# =====================================================
# 📊 MONTHLY TREND (FIXED + CLEAN)
# =====================================================

# =====================================================
# 📈 FIXED MONTHLY TREND (STREAMLIT CLOUD SAFE)
# =====================================================

df["Order.Date"] = pd.to_datetime(df["Order.Date"], errors="coerce")
df = df.dropna(subset=["Order.Date"])

monthly = (
    df.set_index("Order.Date")
    .resample("MS")   # Month Start (MOST STABLE FIX)
    .agg({
        "Sales": "sum",
        "Profit": "sum"
    })
)

monthly = monthly.sort_index()

# =====================================================
# 🧭 HEADER
# =====================================================
st.title("📊 Executive Sales Intelligence Dashboard")
st.markdown("### Business Performance | Risk | Growth | Strategy")

st.markdown("---")

# =====================================================
# 📌 CORE KPIs
# =====================================================
sales = df["Sales"].sum()
profit = df["Profit"].sum()
orders = df["Order.ID"].nunique()

margin = (profit / sales * 100) if sales else 0
aov = sales / orders if orders else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Revenue", f"{sales:,.0f}")
c2.metric("Profit", f"{profit:,.0f}")
c3.metric("Orders", orders)
c4.metric("Margin %", f"{margin:.2f}%")

st.markdown("---")

# =====================================================
# 🧠 EXECUTIVE SUMMARY (BUSINESS STORY)
# =====================================================
st.markdown("## 🧠 Executive Summary")

loss_df = df[df["Profit"] < 0]

loss_impact = abs(loss_df["Profit"].sum())
loss_ratio = loss_impact / profit if profit else 0

growth = monthly["Sales"].pct_change().iloc[-1] * 100 if len(monthly) > 1 else 0

summary_points = []

# Revenue
if sales > df["Sales"].median() * len(df):
    summary_points.append("Revenue base is strong with consistent transaction volume.")
else:
    summary_points.append("Revenue base is moderate with room for scaling.")

# Profitability
if margin >= 25:
    summary_points.append("High profitability indicates efficient cost structure.")
elif margin >= 10:
    summary_points.append("Moderate profitability with optimization opportunities.")
else:
    summary_points.append("Low profitability driven by pricing/cost inefficiencies.")

# Risk
if loss_ratio > 0.4:
    summary_points.append("High financial risk due to significant loss-making products.")
elif len(loss_df) > 0:
    summary_points.append("Moderate risk from limited loss-making segments.")
else:
    summary_points.append("Low risk across product portfolio.")

for i, s in enumerate(summary_points, 1):
    st.write(f"{i}. {s}")

st.markdown("---")

# =====================================================
# 📈 TREND ANALYSIS
# =====================================================
st.markdown("## 📈 Business Trend Analysis")

st.line_chart(monthly["Sales"])
st.line_chart(monthly["Profit"])

st.markdown("---")

# =====================================================
# ⚠️ LOSS ANALYSIS
# =====================================================
st.markdown("## ⚠️ Profit Leakage Analysis")

top_loss = loss_df.groupby("Product.Name")["Profit"].sum().sort_values().head(10)

st.bar_chart(top_loss)

st.write(f"Total loss impact: **{loss_impact:,.0f}**")

st.markdown("---")

# =====================================================
# 📊 BUSINESS DRIVERS (4 CORE PLOTS)
# =====================================================

st.subheader("📊 Revenue by Region")
region = df.groupby("Region")["Sales"].sum().sort_values()
st.bar_chart(region)

st.subheader("📊 Profit by Category")
category = df.groupby("Category")["Profit"].sum().sort_values()
st.bar_chart(category)

st.subheader("📦 Top Products (Revenue Drivers)")
top_products = df.groupby("Product.Name")["Sales"].sum().sort_values(ascending=False).head(10)
st.bar_chart(top_products)

st.subheader("📊 Sales vs Profit Relationship")

fig = px.scatter(
    df,
    x="Sales",
    y="Profit",
    color="Category",
    title="Profitability Distribution"
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# =====================================================
# 🧠 PRIORITY ENGINE (MOST IMPORTANT UPGRADE)
# =====================================================
st.markdown("## 🧠 Executive Priority Dashboard")

priority = []

priority.append({
    "Area": "Profit Margin",
    "Score": max(0, 100 - margin),
    "Insight": "Lower margin = urgent pricing/cost optimization"
})

priority.append({
    "Area": "Loss Leakage",
    "Score": loss_ratio * 100,
    "Insight": "Direct profit erosion from negative products"
})

priority.append({
    "Area": "Growth Stability",
    "Score": abs(growth),
    "Insight": "Revenue momentum risk"
})

priority_df = pd.DataFrame(priority).sort_values("Score", ascending=False)

st.dataframe(priority_df)

st.markdown("---")

# =====================================================
# 📊 80/20 BUSINESS RULE
# =====================================================
st.markdown("## 📊 Business Concentration (80/20 Analysis)")

region_share = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
top_region_share = (region_share.head(3).sum() / region_share.sum()) * 100

category_share = df.groupby("Category")["Profit"].sum().sort_values(ascending=False)
top_category_share = (category_share.head(2).sum() / category_share.sum()) * 100

st.write(f"Top 3 regions contribute **{top_region_share:.2f}% of sales**")
st.write(f"Top 2 categories contribute **{top_category_share:.2f}% of profit**")

st.markdown("---")

# =====================================================
# 📌 STRATEGIC RECOMMENDATIONS
# =====================================================
st.markdown("## 📌 Strategic Recommendations")

if margin < 15:
    st.write("🔴 Improve pricing and discount strategy")

if len(loss_df) > 0:
    st.write("🔴 Reduce or redesign loss-making products")

if growth < 0:
    st.write("🔴 Address declining sales trend")

st.write("🟢 Focus on high-margin categories for expansion")
st.write("🟢 Strengthen strong-performing regions")

st.markdown("---")

# =====================================================
# 📥 EXPORT
# =====================================================
st.download_button(
    "📥 Download Data",
    df.to_csv(index=False),
    "sales_data.csv",
    mime="text/csv"
)

st.caption("🚀 Executive Sales Intelligence System | PwC-Level Analytics Dashboard")