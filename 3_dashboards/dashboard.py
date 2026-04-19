import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# =====================================================
# 📊 PAGE CONFIG (EXECUTIVE LEVEL UI)
# =====================================================
st.set_page_config(
    page_title="Sales Intelligence Executive Dashboard",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# 📥 DATA PIPELINE (AUTOMATION PROOF)
# =====================================================
@st.cache_data
def load_data():
    df = pd.read_csv(
        "1_data/processed/cleanedsales.csv",
        encoding="cp1252",
        low_memory=False
    )

    # Clean columns
    df.columns = df.columns.str.strip().str.replace(".", "_", regex=False)

    # Date handling
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
    df = df.dropna(subset=["Order_Date"])

    # Numeric safety
    for col in ["Sales", "Profit", "Discount"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["Sales"] = df["Sales"].fillna(0)
    df["Profit"] = df["Profit"].fillna(0)

    # Feature engineering
    df["Profit_Margin"] = np.where(df["Sales"] > 0,
                                   (df["Profit"] / df["Sales"]) * 100,
                                   0)

    df["YearMonth"] = df["Order_Date"].dt.to_period("M").astype(str)

    return df


df = load_data()

# =====================================================
# 🧭 EXECUTIVE STORY FLOW (IMPORTANT FOR INTERVIEW)
# =====================================================
st.title("📊 Sales Intelligence & Executive Decision System")

with st.expander("📌 End-to-End Data Flow (Pipeline Proof)"):
    st.markdown("""
    **1. Data Ingestion → CSV Dataset**  
    **2. Data Cleaning → Missing values, type correction**  
    **3. Feature Engineering → Margin, Time series features**  
    **4. Analytics Layer → KPIs, segmentation, trends**  
    **5. Decision Layer → Business recommendations**
    """)

st.markdown("---")

# =====================================================
# 📌 EXECUTIVE SCORECARD (NEW UPGRADE)
# =====================================================
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
orders = df["Order_ID"].nunique()

margin = (total_profit / total_sales * 100) if total_sales else 0

null_ratio = df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100
duplicate_ratio = df.duplicated().sum() / len(df) * 100

data_quality = max(0, 100 - (null_ratio + duplicate_ratio))

# Business Health Index (NEW)
business_score = (
    (margin * 0.4) +
    (data_quality * 0.3) +
    (min(100, orders / 100) * 0.3)
)

col1, col2, col3 = st.columns(3)

col1.metric("💰 Revenue", f"₹{total_sales:,.0f}")
col2.metric("📈 Profit", f"₹{total_profit:,.0f}")
col3.metric("🛒 Orders", f"{orders:,}")

st.progress(int(data_quality))

st.success(f"📊 Business Health Score: {business_score:.2f}/100")

st.markdown("---")

# =====================================================
# 🔍 FILTERS
# =====================================================
st.sidebar.header("🔍 Business Filters")

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
    st.error("No data for selected filters")
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

st.subheader("📌 KPI Dashboard")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Sales", f"₹{sales:,.0f}", f"{growth:.2f}% MoM")
c2.metric("Profit", f"₹{profit:,.0f}")
c3.metric("Orders", orders)
c4.metric("AOV", f"₹{aov:,.2f}")
c5.metric("Margin", f"{margin:.2f}%")

st.markdown("---")

# =====================================================
# 🧠 ADVANCED ANALYTICS LAYER (REAL INTERVIEW LEVEL)
# =====================================================

st.subheader("🧠 Advanced Analytics Layer")

# Pareto Analysis (80/20 Rule)
top_products = filtered_df.groupby("Product_Name")["Sales"].sum().sort_values(ascending=False)
pareto_impact = top_products.cumsum() / top_products.sum() * 100

high_impact_products = pareto_impact[pareto_impact <= 80]

# Segmentation
region_sales = filtered_df.groupby("Region")["Sales"].sum()
category_profit = filtered_df.groupby("Category")["Profit"].sum()

top_region = region_sales.idxmax()
risk_region = region_sales.idxmin()

best_category = category_profit.idxmax()
worst_category = category_profit.idxmin()

col1, col2, col3 = st.columns(3)

col1.success(f"🏆 Top Region: {top_region}")
col2.warning(f"⚠️ Risk Region: {risk_region}")
col3.info(f"💡 Best Category: {best_category}")

st.markdown("---")

# =====================================================
# 📈 VISUALIZATION
# =====================================================
st.subheader("📈 Sales Trend")

fig = px.line(monthly, x="YearMonth", y="Sales", markers=True)
st.plotly_chart(fig, use_container_width=True)

st.subheader("📦 Category Performance")

cat = filtered_df.groupby("Category")[["Sales", "Profit"]].sum().reset_index()
fig = px.bar(cat, x="Category", y="Profit", color="Profit")
st.plotly_chart(fig, use_container_width=True)

st.subheader("📊 Profit vs Sales")

fig = px.scatter(
    filtered_df,
    x="Sales",
    y="Profit",
    color="Category",
    hover_data=["Product_Name"]
)
st.plotly_chart(fig, use_container_width=True)

# =====================================================
# 🚨 LOSS ANALYSIS
# =====================================================
st.subheader("🚨 Loss-Making Products")

loss_df = filtered_df[filtered_df["Profit"] < 0]
st.dataframe(loss_df[["Product_Name", "Sales", "Profit"]].head(10))

# =====================================================
# 📉 DISCOUNT IMPACT
# =====================================================
st.subheader("📉 Discount Impact")

fig = px.scatter(filtered_df, x="Discount", y="Profit", color="Category")
st.plotly_chart(fig, use_container_width=True)

# =====================================================
# 📌 BUSINESS RECOMMENDATION ENGINE (IMPORTANT)
# =====================================================
st.subheader("📌 Business Recommendations")

recommendations = []

if margin < 15:
    recommendations.append("Increase pricing efficiency to improve margin")

if growth < 0:
    recommendations.append("Launch sales recovery strategy")

if len(loss_df) > 0:
    recommendations.append("Stop or redesign loss-making products")

if data_quality < 80:
    recommendations.append("Improve data pipeline quality")

if len(high_impact_products) < len(top_products) * 0.2:
    recommendations.append("Focus on high-value product segmentation")

for r in recommendations:
    st.write("•", r)

if not recommendations:
    st.success("Business performance is stable and optimized 🚀")

# =====================================================
# 📥 EXPORT
# =====================================================
st.download_button(
    "📥 Download Data",
    filtered_df.to_csv(index=False),
    "sales_data.csv",
    mime="text/csv"
)

# =====================================================
# FOOTER
# =====================================================
st.markdown("---")
st.caption("🚀 Production-Level Analytics System | Vivek Saha")