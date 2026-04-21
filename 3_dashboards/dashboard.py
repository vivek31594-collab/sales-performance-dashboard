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
        st.error("❌ Data file not found in repo structure.")
        st.stop()

    df = pd.read_csv(file_path, encoding="cp1252", low_memory=False)

    df.columns = df.columns.str.strip().str.replace(".", "_", regex=False)

    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
    df = df.dropna(subset=["Order_Date"])

    for col in ["Sales", "Profit", "Discount"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["Sales"] = df["Sales"].fillna(0)
    df["Profit"] = df["Profit"].fillna(0)

    df["Profit_Margin"] = np.where(df["Sales"] > 0,
                                   (df["Profit"] / df["Sales"]) * 100,
                                   0)

    df["YearMonth"] = df["Order_Date"].dt.to_period("M").astype(str)

    return df


df = load_data()

sns.set_style("whitegrid")

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
    st.warning("⚠️ No data for selected filters")
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
# 📈 SALES TREND
# =====================================================
fig = px.line(monthly, x="YearMonth", y="Sales", markers=True)
st.plotly_chart(fig, use_container_width=True)

# =====================================================
# 📊 SALES BY REGION
# =====================================================
st.subheader("📊 Sales by Region")

region_sales = filtered_df.groupby("Region")["Sales"].sum().sort_values()

fig1, ax1 = plt.subplots(figsize=(10,5))

sns.barplot(
    x=region_sales.values,
    y=region_sales.index,
    hue=region_sales.index,
    palette="viridis",
    legend=False,
    ax=ax1
)

ax1.set_title("Sales by Region")
ax1.set_xlabel("Sales")
ax1.set_ylabel("")
sns.despine()
st.pyplot(fig1)

# =====================================================
# 📊 PROFIT BY SUB-CATEGORY
# =====================================================
st.subheader("📊 Profit by Sub-Category")

subcat_profit = filtered_df.groupby("Sub.Category")["Profit"].sum().sort_values()

fig2, ax2 = plt.subplots(figsize=(12,6))

sns.barplot(
    x=subcat_profit.values,
    y=subcat_profit.index,
    hue=subcat_profit.index,
    palette="coolwarm",
    legend=False,
    ax=ax2
)

for i, v in enumerate(subcat_profit.values):
    ax2.text(v + (max(subcat_profit.values)*0.01), i, f"{v:,.0f}", va='center', fontsize=9)

ax2.set_title("Profit by Sub-Category")
ax2.set_xlabel("Profit")
ax2.set_ylabel("")
sns.despine()
st.pyplot(fig2)

# =====================================================
# 📊 SALES vs PROFIT
# =====================================================
st.subheader("📊 Sales vs Profit Relationship")

fig3, ax3 = plt.subplots(figsize=(10,6))

sns.scatterplot(data=filtered_df, x="Sales", y="Profit", alpha=0.6, ax=ax3)

sns.regplot(data=filtered_df, x="Sales", y="Profit", scatter=False, ax=ax3)

high_sales = filtered_df[filtered_df["Sales"] > 8000]

sns.scatterplot(data=high_sales, x="Sales", y="Profit", color="red", s=80, label="High-value", ax=ax3)

ax3.set_title("Sales vs Profit Relationship")
ax3.legend()
sns.despine()
st.pyplot(fig3)

# =====================================================
# 📦 TOP PRODUCTS
# =====================================================
st.subheader("📦 Top 10 Products by Sales")

top_products = filtered_df.groupby("Product_Name")["Sales"].sum().sort_values(ascending=False).head(10)

fig4, ax4 = plt.subplots(figsize=(10,6))

sns.barplot(
    x=top_products.values,
    y=top_products.index,
    hue=top_products.index,
    palette="Blues_r",
    legend=False,
    ax=ax4
)

ax4.set_title("Top 10 Products")
sns.despine()
st.pyplot(fig4)

# =====================================================
# 📉 PROFIT TREND
# =====================================================
st.subheader("📉 Monthly Profit Trend")

profit_trend = filtered_df.groupby("YearMonth")["Profit"].sum().reset_index()

fig5, ax5 = plt.subplots(figsize=(10,5))

sns.lineplot(data=profit_trend, x="YearMonth", y="Profit", marker="o", ax=ax5)

ax5.set_title("Profit Trend")
plt.xticks(rotation=45)

sns.despine()
st.pyplot(fig5)

# =====================================================
# 🚨 DISCOUNT vs PROFIT
# =====================================================
st.subheader("🚨 Discount vs Profit Impact")

fig6, ax6 = plt.subplots(figsize=(10,6))

sns.scatterplot(data=filtered_df, x="Discount", y="Profit", alpha=0.6, ax=ax6)

sns.regplot(data=filtered_df, x="Discount", y="Profit", scatter=False, ax=ax6)

ax6.set_title("Discount vs Profit Relationship")

sns.despine()
st.pyplot(fig6)

# =====================================================
# 🚨 LOSS ANALYSIS
# =====================================================
st.subheader("🚨 Loss Making Transactions")

loss_df = filtered_df[filtered_df["Profit"] < 0]

st.dataframe(loss_df[["Product_Name", "Sales", "Profit"]].head(10))

st.warning(f"{len(loss_df)} loss cases detected")

# =====================================================
# 📌 ACTIONS
# =====================================================
st.subheader("📌 Business Actions")

if margin < 15:
    st.write("• Improve pricing strategy")

if len(loss_df) > 0:
    st.write("• Fix loss-making products")

if growth < 0:
    st.write("• Sales recovery plan needed")

# =====================================================
# FOOTER
# =====================================================
st.caption("🚀 Executive Analytics Dashboard | Vivek Saha")