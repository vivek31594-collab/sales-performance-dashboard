import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# =====================================================
# ⚙️ PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Executive Sales Intelligence System",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# 📥 LOAD DATA (DEPLOYMENT SAFE)
# =====================================================
@st.cache_data
def load_data():
    file_path = "1_data/processed/cleanedsales.csv"

    if not os.path.exists(file_path):
        st.error("❌ Data file not found. Check GitHub repo structure.")
        st.stop()

    df = pd.read_csv(file_path, encoding="cp1252", low_memory=False)

    # CLEANING
    df.columns = df.columns.str.strip().str.replace(".", "_", regex=False)

    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
    df = df.dropna(subset=["Order_Date"])

    for col in ["Sales", "Profit", "Discount"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["Sales"] = df["Sales"].fillna(0)
    df["Profit"] = df["Profit"].fillna(0)

    # FEATURE ENGINEERING
    df["Profit_Margin"] = np.where(
        df["Sales"] > 0,
        (df["Profit"] / df["Sales"]) * 100,
        0
    )

    df["YearMonth"] = df["Order_Date"].dt.to_period("M").astype(str)

    return df


df = load_data()

# =====================================================
# 🧭 TITLE
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
# 📌 GLOBAL KPIs
# =====================================================
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
orders = df["Order_ID"].nunique()

margin = (total_profit / total_sales * 100) if total_sales else 0

col1, col2, col3 = st.columns(3)
col1.metric("💰 Revenue", f"₹{total_sales:,.0f}")
col2.metric("📈 Profit", f"₹{total_profit:,.0f}")
col3.metric("🛒 Orders", f"{orders:,}")

st.markdown("---")

# =====================================================
# 🔍 FILTERS
# =====================================================
st.sidebar.header("Filters")

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
    st.warning("⚠️ No data available for selected filters")
    st.stop()

# =====================================================
# 📊 KPI DASHBOARD
# =====================================================
sales = filtered_df["Sales"].sum()
profit = filtered_df["Profit"].sum()
orders = filtered_df["Order_ID"].nunique()

aov = sales / orders if orders else 0
margin = (profit / sales * 100) if sales else 0

monthly = filtered_df.groupby("YearMonth")["Sales"].sum().reset_index()
growth = monthly["Sales"].pct_change().iloc[-1] * 100 if len(monthly) > 1 else 0

st.subheader("📊 KPI Dashboard")

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Sales", f"₹{sales:,.0f}", f"{growth:.2f}% MoM")
c2.metric("Profit", f"₹{profit:,.0f}")
c3.metric("Orders", orders)
c4.metric("AOV", f"₹{aov:,.2f}")
c5.metric("Margin", f"{margin:.2f}%")

st.markdown("---")

# =====================================================
# 📈 PLOTLY TREND
# =====================================================
fig = px.line(
    monthly,
    x="YearMonth",
    y="Sales",
    title="📈 Monthly Sales Trend",
    markers=True
)

st.plotly_chart(fig, width="stretch")

# =====================================================
# 📉 SEABORN ANALYSIS
# =====================================================
st.subheader("📉 Sales vs Profit Analysis")

sns.set_style("whitegrid")

fig2, ax = plt.subplots(figsize=(8, 5))

sns.scatterplot(
    data=filtered_df,
    x="Sales",
    y="Profit",
    alpha=0.6,
    ax=ax
)

sns.regplot(
    data=filtered_df,
    x="Sales",
    y="Profit",
    scatter=False,
    ax=ax
)

ax.set_title("Sales vs Profit Relationship")

st.pyplot(fig2)

# =====================================================
# 📊 REGION ANALYSIS
# =====================================================
st.subheader("📊 Sales by Region")

region_sales = filtered_df.groupby("Region")["Sales"].sum().reset_index()
st.dataframe(region_sales)

# =====================================================
# 🚨 LOSS ANALYSIS
# =====================================================
st.subheader("🚨 Loss Making Transactions")

loss_df = filtered_df[filtered_df["Profit"] < 0]
st.dataframe(loss_df[["Product_Name", "Sales", "Profit"]].head(10))

st.warning(f"{len(loss_df)} loss transactions detected")

# =====================================================
# 🧠 INSIGHTS
# =====================================================
st.subheader("🧠 Key Insights")

st.write("• High sales do not always result in high profit")
st.write("• Regional performance varies significantly")
st.write("• Loss-making transactions require attention")

# =====================================================
# 📌 ACTIONS
# =====================================================
st.subheader("📌 Business Actions")

if margin < 15:
    st.write("• Improve pricing or reduce discount dependency")

if len(loss_df) > 0:
    st.write("• Investigate loss-making products")

if growth < 0:
    st.write("• Implement sales recovery strategy")

if margin >= 15 and len(loss_df) == 0:
    st.success("✔ Business performance is stable")

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
st.caption("🚀 Production-Ready Executive Dashboard | Vivek Saha")