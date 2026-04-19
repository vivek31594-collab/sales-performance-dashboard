import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# 📊 PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Sales Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# 📥 LOAD DATA
# =====================================================
@st.cache_data
def load_data():
    df = pd.read_csv(
        "1_data/processed/cleanedsales.csv",
        encoding="cp1252",
        low_memory=False
    )

    # Clean column names
    df.columns = df.columns.str.strip().str.replace(".", "_", regex=False)

    # Date conversion
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
    df = df.dropna(subset=["Order_Date"])

    # Numeric conversion
    for col in ["Sales", "Profit", "Discount"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df["Sales"] = df["Sales"].fillna(0)
    df["Profit"] = df["Profit"].fillna(0)

    # Profit Margin
    df["Profit_Margin"] = df["Profit"] / df["Sales"].replace(0, pd.NA) * 100

    # Time feature
    df["YearMonth"] = df["Order_Date"].dt.to_period("M").astype(str)

    return df


df = load_data()

# =====================================================
# 🧭 BUSINESS STORY FLOW (NEW)
# =====================================================
st.subheader("🧭 Business Story Flow")

st.info("""
📥 Data Ingestion → Raw CSV Sales Dataset  
🔧 Data Cleaning → Missing values, formatting, type correction  
📊 Analytics Layer → KPIs, trends, category analysis  
🧠 Insights Layer → Profitability, risk detection  
📌 Decision Layer → Business recommendations for optimization
""")

st.markdown("---")

# =====================================================
# 📌 EXECUTIVE SUMMARY
# =====================================================
st.subheader("📌 Executive Business Summary")

total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_orders = df["Order_ID"].nunique()

profit_margin = (total_profit / total_sales * 100) if total_sales else 0

# =====================================================
# 🧪 DATA QUALITY SCORE
# =====================================================
total_rows = len(df)
null_ratio = df.isnull().sum().sum() / (total_rows * len(df.columns)) * 100
duplicate_ratio = df.duplicated().sum() / total_rows * 100

quality_score = 100 - (null_ratio + duplicate_ratio)
quality_score = max(0, min(100, quality_score))

c1, c2, c3 = st.columns(3)

c1.metric("💰 Total Revenue", f"₹{total_sales:,.0f}")
c2.metric("📈 Total Profit", f"₹{total_profit:,.0f}")
c3.metric("🛒 Total Orders", f"{total_orders:,}")

# Profit Health
if profit_margin >= 20:
    st.success(f"🟢 Strong Business Health | Margin: {profit_margin:.2f}%")
elif profit_margin >= 10:
    st.warning(f"🟡 Moderate Performance | Margin: {profit_margin:.2f}%")
else:
    st.error(f"🔴 Profitability Risk | Margin: {profit_margin:.2f}%")

# Data Quality
st.subheader("🧪 Data Quality Score")

if quality_score >= 85:
    st.success(f"🟢 High Quality Data: {quality_score:.2f}/100")
elif quality_score >= 70:
    st.warning(f"🟡 Moderate Quality Data: {quality_score:.2f}/100")
else:
    st.error(f"🔴 Poor Quality Data: {quality_score:.2f}/100")

st.markdown("---")

# =====================================================
# 🔍 FILTERS
# =====================================================
st.sidebar.header("🔍 Filters")

min_date = df["Order_Date"].min()
max_date = df["Order_Date"].max()

date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date])

region_list = df["Region"].dropna().unique().tolist()
category_list = df["Category"].dropna().unique().tolist()

region = st.sidebar.multiselect("Region", region_list, default=region_list)
category = st.sidebar.multiselect("Category", category_list, default=category_list)

# =====================================================
# FILTERED DATA
# =====================================================
filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category)) &
    (df["Order_Date"] >= pd.to_datetime(date_range[0])) &
    (df["Order_Date"] <= pd.to_datetime(date_range[1]))
]

if filtered_df.empty:
    st.error("No data available for selected filters")
    st.stop()

# =====================================================
# 📊 KPIs
# =====================================================
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
orders = filtered_df["Order_ID"].nunique()

aov = total_sales / orders if orders else 0
margin = (total_profit / total_sales * 100) if total_sales else 0

monthly_sales = (
    filtered_df.groupby("YearMonth")["Sales"]
    .sum()
    .reset_index()
    .sort_values("YearMonth")
)

growth = 0
if len(monthly_sales) > 1:
    growth = (
        (monthly_sales["Sales"].iloc[-1] - monthly_sales["Sales"].iloc[-2])
        / monthly_sales["Sales"].iloc[-2]
    ) * 100

st.subheader("📌 Key Metrics")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("💰 Sales", f"₹{total_sales:,.0f}", f"{growth:.2f}% MoM")
c2.metric("📈 Profit", f"₹{total_profit:,.0f}")
c3.metric("🛒 Orders", orders)
c4.metric("💳 AOV", f"₹{aov:,.2f}")
c5.metric("📊 Margin", f"{margin:.2f}%")

st.markdown("---")

# =====================================================
# 🧠 INSIGHTS
# =====================================================
st.subheader("🧠 Business Insights")

region_sales = filtered_df.groupby("Region")["Sales"].sum()
top_region = region_sales.idxmax()

category_profit = filtered_df.groupby("Category")["Profit"].sum()
best_category = category_profit.idxmax()
worst_category = category_profit.idxmin()

col1, col2, col3 = st.columns(3)

col1.success(f"🏆 Top Region: {top_region}")
col2.warning(f"⚠️ Low Profit Category: {worst_category}")
col3.info(f"💡 Best Category: {best_category}")

st.markdown("---")

# =====================================================
# 📈 VISUALS
# =====================================================
st.subheader("📈 Sales Trend")

fig = px.line(monthly_sales, x="YearMonth", y="Sales", markers=True)
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
st.warning(f"⚠️ {len(loss_df)} loss-making transactions detected")

# =====================================================
# 📉 DISCOUNT ANALYSIS
# =====================================================
st.subheader("📉 Discount Impact")

fig = px.scatter(filtered_df, x="Discount", y="Profit", color="Category")
st.plotly_chart(fig, use_container_width=True)

# =====================================================
# 🚨 RISK INDICATORS
# =====================================================
st.subheader("🚨 Risk Indicators")

if margin < 15:
    st.error("Low profit margin detected")

if growth < 0:
    st.error("Negative growth trend detected")

if len(loss_df) > 0:
    st.warning("Loss-making products exist")

st.markdown("---")

# =====================================================
# 📥 DOWNLOAD
# =====================================================
st.download_button(
    "📥 Download Filtered Data",
    filtered_df.to_csv(index=False),
    "filtered_sales_data.csv",
    mime="text/csv"
)

# =====================================================
# FOOTER
# =====================================================
st.markdown("---")
st.caption("🚀 Built by Vivek Saha | Sales Analytics Dashboard")