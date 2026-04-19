import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# =====================================================
# ⚙️ PAGE CONFIG (CONSULTING STYLE UI)
# =====================================================
st.set_page_config(
    page_title="Executive Sales Intelligence System",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# 📥 DATA PIPELINE (PRODUCTION STYLE)
# =====================================================
@st.cache_data
def load_data():
    df = pd.read_csv(
        "1_data/processed/cleanedsales.csv",
        encoding="cp1252",
        low_memory=False
    )

    # CLEANING
    df.columns = df.columns.str.strip().str.replace(".", "_", regex=False)

    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
    df = df.dropna(subset=["Order_Date"])

    for col in ["Sales", "Profit", "Discount"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["Sales"] = df["Sales"].fillna(0)
    df["Profit"] = df["Profit"].fillna(0)

    # FEATURE ENGINEERING
    df["Profit_Margin"] = np.where(df["Sales"] > 0,
                                   (df["Profit"] / df["Sales"]) * 100,
                                   0)

    df["YearMonth"] = df["Order_Date"].dt.to_period("M").astype(str)

    return df


df = load_data()

# =====================================================
# 🧭 EXECUTIVE STORY FLOW (CONSULTING STANDARD)
# =====================================================
st.title("📊 Executive Sales Intelligence System")

st.info("""
📥 Data → Cleaned & Structured  
📊 Analytics → KPI + Trend + Segmentation  
🧠 Intelligence → Risk + Opportunity Detection  
📌 Decision Layer → Actionable Business Strategy
""")

st.markdown("---")

# =====================================================
# 📌 CORE METRICS
# =====================================================
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
orders = df["Order_ID"].nunique()

margin = (total_profit / total_sales * 100) if total_sales else 0

# =====================================================
# ⭐ BENCHMARK SYSTEM (NEW - 8 LPA LEVEL)
# =====================================================
benchmark_sales = df["Sales"].mean() * len(df)
performance_vs_benchmark = (total_sales / benchmark_sales) * 100 if benchmark_sales else 0

# =====================================================
# 🧪 DATA QUALITY SCORE
# =====================================================
null_ratio = df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100
duplicate_ratio = df.duplicated().sum() / len(df) * 100

data_quality = max(0, 100 - (null_ratio + duplicate_ratio))

# =====================================================
# 📊 BUSINESS HEALTH INDEX (ADVANCED)
# =====================================================
business_health = (
    (margin * 0.4) +
    (data_quality * 0.3) +
    (min(performance_vs_benchmark, 100) * 0.3)
) / 2

# =====================================================
# KPI DISPLAY
# =====================================================
col1, col2, col3 = st.columns(3)

col1.metric("💰 Revenue", f"₹{total_sales:,.0f}")
col2.metric("📈 Profit", f"₹{total_profit:,.0f}")
col3.metric("🛒 Orders", f"{orders:,}")

st.progress(int(data_quality))

st.success(f"📊 Business Health Score: {business_health:.2f}/100")

st.markdown("---")

# =====================================================
# 🔍 FILTERS
# =====================================================
st.sidebar.header("Business Filters")

date_range = st.sidebar.date_input(
    "Date Range",
    [df["Order_Date"].min(), df["Order_Date"].max()]
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
    (df["Order_Date"] >= pd.to_datetime(date_range[0])) &
    (df["Order_Date"] <= pd.to_datetime(date_range[1]))
]

if filtered_df.empty:
    st.error("No data available")
    st.stop()

# =====================================================
# 📊 KPI ENGINE
# =====================================================
sales = filtered_df["Sales"].sum()
profit = filtered_df["Profit"].sum()
orders = filtered_df["Order_ID"].nunique()

aov = sales / orders if orders else 0
margin = (profit / sales * 100) if sales else 0

monthly = filtered_df.groupby("YearMonth")["Sales"].sum().reset_index()
growth = monthly["Sales"].pct_change().iloc[-1] * 100 if len(monthly) > 1 else 0

# =====================================================
# 🚨 ANOMALY DETECTION (NEW)
# =====================================================
filtered_df["Profit_Risk"] = np.where(
    (filtered_df["Discount"] > 0.3) & (filtered_df["Profit"] < 0),
    "HIGH RISK",
    "NORMAL"
)

risk_count = len(filtered_df[filtered_df["Profit_Risk"] == "HIGH RISK"])

# =====================================================
# 📌 KPI DASHBOARD
# =====================================================
st.subheader("KPI Dashboard")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Sales", f"₹{sales:,.0f}", f"{growth:.2f}% MoM")
c2.metric("Profit", f"₹{profit:,.0f}")
c3.metric("Orders", orders)
c4.metric("AOV", f"₹{aov:,.2f}")
c5.metric("Margin", f"{margin:.2f}%")

st.markdown("---")

# =====================================================
# 🧠 ADVANCED ANALYTICS
# =====================================================
st.subheader("Advanced Intelligence Layer")

region_sales = filtered_df.groupby("Region")["Sales"].sum()
category_profit = filtered_df.groupby("Category")["Profit"].sum()

top_region = region_sales.idxmax()
risk_region = region_sales.idxmin()

best_category = category_profit.idxmax()
worst_category = category_profit.idxmin()

col1, col2, col3 = st.columns(3)

col1.success(f"Top Region: {top_region}")
col2.warning(f"Risk Region: {risk_region}")
col3.info(f"Best Category: {best_category}")

st.markdown("---")

# =====================================================
# 📈 VISUALS
# =====================================================
fig = px.line(monthly, x="YearMonth", y="Sales", markers=True)
st.plotly_chart(fig, use_container_width=True)

# =====================================================
# 🚨 LOSS ANALYSIS
# =====================================================
loss_df = filtered_df[filtered_df["Profit"] < 0]

st.subheader("Loss Analysis")
st.dataframe(loss_df[["Product_Name", "Sales", "Profit"]].head(10))

st.warning(f"{len(loss_df)} loss cases detected")

# =====================================================
# 🧠 EXECUTIVE AI SUMMARY (FINAL UPGRADE)
# =====================================================
st.subheader("Executive AI Summary")

insight_1 = f"Revenue is {'strong' if margin > 15 else 'weak'} with margin at {margin:.2f}%"
insight_2 = f"{risk_count} high-risk transactions identified"
insight_3 = f"{risk_region} region requires immediate attention"

st.write("📌 What happened:")
st.write(insight_1)

st.write("📌 Why it happened:")
st.write(insight_2)

st.write("📌 What to do:")
st.write(insight_3)

# =====================================================
# 📌 BUSINESS DECISION ENGINE
# =====================================================
st.subheader("Business Action Plan")

actions = []

if margin < 15:
    actions.append("Increase pricing or reduce discount dependency")

if growth < 0:
    actions.append("Launch sales recovery campaign")

if risk_count > 0:
    actions.append("Fix discount-driven loss transactions")

if business_health < 70:
    actions.append("Improve data + operational efficiency")

for a in actions:
    st.write("•", a)

if not actions:
    st.success("System is stable and optimized")

# =====================================================
# 📥 EXPORT
# =====================================================
st.download_button(
    "Download Data",
    filtered_df.to_csv(index=False),
    "sales_data.csv",
    mime="text/csv"
)

# =====================================================
# FOOTER
# =====================================================
st.caption("Production-Grade Executive Analytics System | Vivek Saha")