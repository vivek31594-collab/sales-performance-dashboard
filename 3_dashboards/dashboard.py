import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os

# =====================================================
# ⚙️ CONFIG
# =====================================================
st.set_page_config(
    page_title="Executive Sales Intelligence System",
    page_icon="📊",
    layout="wide"
)

sns.set_style("whitegrid")

# =====================================================
# 📥 DATA LOAD
# =====================================================
@st.cache_data
def load_data():
    file_path = "1_data/processed/cleanedsales.csv"

    if not os.path.exists(file_path):
        st.error("Dataset not found")
        st.stop()

    df = pd.read_csv(file_path, encoding="cp1252")

    df["Order.Date"] = pd.to_datetime(df["Order.Date"], errors="coerce")
    df = df.dropna(subset=["Order.Date"])

    for col in ["Sales", "Profit", "Discount"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df


df = load_data().sort_values("Order.Date")

# =====================================================
# 📊 MONTHLY TREND (FIXED + STABLE)
# =====================================================
monthly = (
    df.set_index("Order.Date")
    .resample("MS")
    .agg({"Sales": "sum", "Profit": "sum"})
    .sort_index()
)

# =====================================================
# 🧭 HEADER
# =====================================================
st.title("📊 Executive Sales Intelligence Dashboard")
st.markdown("### PwC-Style Business Intelligence System")

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
# 🧠 EXECUTIVE INSIGHT ENGINE (UPGRADED)
# =====================================================
st.markdown("## 🧠 Executive Business Health")

loss_df = df[df["Profit"] < 0]
loss_impact = abs(loss_df["Profit"].sum())
loss_ratio = loss_impact / profit if profit else 0

growth = monthly["Sales"].pct_change().iloc[-1] * 100 if len(monthly) > 1 else 0
volatility = monthly["Sales"].std() / monthly["Sales"].mean()

insights = []

# Revenue
if sales > df["Sales"].mean() * len(df):
    insights.append("Strong revenue base with consistent demand.")
else:
    insights.append("Moderate revenue performance with scaling opportunity.")

# Profitability
if margin >= 25:
    insights.append("High profitability with efficient operations.")
elif margin >= 10:
    insights.append("Moderate profitability with optimization scope.")
else:
    insights.append("Low profitability → pricing/cost issue detected.")

# Risk
if loss_ratio > 0.4:
    insights.append("High financial risk due to loss-heavy products.")
elif len(loss_df) > 0:
    insights.append("Controlled but present loss-making segments.")

# Growth
if growth > 5:
    insights.append("Strong upward sales momentum.")
elif growth > 0:
    insights.append("Stable but slow growth.")
else:
    insights.append("Sales decline detected.")

# Volatility
if volatility > 0.5:
    insights.append("High volatility → unstable demand pattern.")
else:
    insights.append("Stable demand pattern.")

for i, ins in enumerate(insights, 1):
    st.write(f"{i}. {ins}")

st.markdown("---")

# =====================================================
# 📈 TREND ANALYSIS (UPGRADED)
# =====================================================
st.markdown("## 📈 Business Trend Intelligence")

st.line_chart(monthly["Sales"])
st.line_chart(monthly["Profit"])

st.write(f"""
- 📌 Peak Sales Month: {monthly['Sales'].idxmax()}
- 📉 Lowest Sales Month: {monthly['Sales'].idxmin()}
- 📊 Average Monthly Sales: {monthly['Sales'].mean():,.0f}
""")

st.markdown("---")

# =====================================================
# ⚠️ LOSS ANALYSIS
# =====================================================
st.markdown("## ⚠️ Profit Leakage Analysis")

top_loss = loss_df.groupby("Product.Name")["Profit"].sum().sort_values().head(10)

st.bar_chart(top_loss)

st.write(f"Total Loss Impact: **{loss_impact:,.0f}**")

st.markdown("---")

# =====================================================
# 📊 BUSINESS DRIVERS
# =====================================================
st.subheader("📊 Revenue by Region")
st.bar_chart(df.groupby("Region")["Sales"].sum().sort_values())

st.subheader("📊 Profit by Category")
st.bar_chart(df.groupby("Category")["Profit"].sum().sort_values())

st.subheader("📦 Top Products")
st.bar_chart(df.groupby("Product.Name")["Sales"].sum().sort_values(ascending=False).head(10))

st.subheader("📊 Sales vs Profit")
fig = px.scatter(df, x="Sales", y="Profit", color="Category")
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# =====================================================
# 🧠 PRIORITY ENGINE (REAL BUSINESS PRIORITY)
# =====================================================
st.markdown("## 🧠 Action Priority Matrix")

priority_df = pd.DataFrame([
    {
        "Area": "Profit Margin",
        "Score": max(0, 100 - margin),
        "Impact": "Pricing / Cost Structure"
    },
    {
        "Area": "Loss Leakage",
        "Score": loss_ratio * 100,
        "Impact": "Product Portfolio Optimization"
    },
    {
        "Area": "Growth Stability",
        "Score": abs(growth),
        "Impact": "Demand / Market Strategy"
    }
]).sort_values("Score", ascending=False)

st.dataframe(priority_df)

st.markdown("---")

# =====================================================
# 📊 80/20 RULE
# =====================================================
st.markdown("## 📊 Business Concentration (80/20 Rule)")

top_region = (df.groupby("Region")["Sales"].sum().nlargest(3).sum() /
              df["Sales"].sum()) * 100

top_category = (df.groupby("Category")["Profit"].sum().nlargest(2).sum() /
                df["Profit"].sum()) * 100

st.write(f"Top 3 regions contribute **{top_region:.2f}% of revenue**")
st.write(f"Top 2 categories contribute **{top_category:.2f}% of profit**")

st.markdown("---")

# =====================================================
# 📌 RECOMMENDATIONS
# =====================================================
st.markdown("## 📌 Strategic Recommendations")

if margin < 15:
    st.write("🔴 Improve pricing & discount control")

if len(loss_df) > 0:
    st.write("🔴 Restructure loss-making products")

if growth < 0:
    st.write("🔴 Fix declining demand trend")

st.write("🟢 Focus on high-margin categories")
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

st.caption("🚀 PwC-Level Executive Analytics Dashboard")