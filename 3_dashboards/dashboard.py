import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os

# =====================================================
# ⚙️ PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Executive Sales Intelligence System",
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
        st.error("❌ Dataset not found. Check path.")
        st.stop()

    df = pd.read_csv(file_path, encoding="cp1252", low_memory=False)

    # Clean columns lightly (DO NOT rename dots)
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
st.title("📊 Executive Sales Intelligence System")

st.markdown("---")

# =====================================================
# 📌 GLOBAL KPIs
# =====================================================
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
orders = df["Order.ID"].nunique()

margin = (total_profit / total_sales * 100) if total_sales else 0

c1, c2, c3 = st.columns(3)
c1.metric("💰 Revenue", f"₹{total_sales:,.0f}")
c2.metric("📈 Profit", f"₹{total_profit:,.0f}")
c3.metric("🛒 Orders", f"{orders:,}")

st.markdown("---")

# =====================================================
# 🔍 FILTERS
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
# 📊 KPI DASHBOARD
# =====================================================
sales = filtered_df["Sales"].sum()
profit = filtered_df["Profit"].sum()
orders = filtered_df["Order.ID"].nunique()

aov = sales / orders if orders else 0
margin = (profit / sales * 100) if sales else 0

monthly = filtered_df.groupby("Year_Month")["Sales"].sum().reset_index()
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
fig1 = px.line(
    monthly,
    x="Year_Month",
    y="Sales",
    markers=True,
    title="📈 Monthly Sales Trend"
)

st.plotly_chart(fig1, use_container_width=True)

# =====================================================
# 📊 SALES BY REGION
# =====================================================
st.subheader("📊 Sales by Region")

region_sales = filtered_df.groupby("Region")["Sales"].sum().sort_values()

fig2, ax2 = plt.subplots(figsize=(10,5))

sns.barplot(
    x=region_sales.values,
    y=region_sales.index,
    hue=region_sales.index,
    palette="viridis",
    legend=False,
    ax=ax2
)

ax2.set_title("Sales by Region")
ax2.set_xlabel("Sales")
ax2.set_ylabel("")

st.pyplot(fig2)

# =====================================================
# 📊 PROFIT BY SUB-CATEGORY
# =====================================================
st.subheader("📊 Profit by Sub-Category")

subcat_profit = filtered_df.groupby("Sub.Category")["Profit"].sum().sort_values()

fig3, ax3 = plt.subplots(figsize=(12,6))

sns.barplot(
    x=subcat_profit.values,
    y=subcat_profit.index,
    hue=subcat_profit.index,
    palette="coolwarm",
    legend=False,
    ax=ax3
)

for i, v in enumerate(subcat_profit.values):
    ax3.text(v + (max(subcat_profit.values)*0.01), i, f"{v:,.0f}")

ax3.set_title("Profit by Sub-Category")
ax3.set_xlabel("Profit")
ax3.set_ylabel("")

st.pyplot(fig3)

# =====================================================
# 📊 SALES vs PROFIT
# =====================================================
st.subheader("📊 Sales vs Profit Relationship")

fig4, ax4 = plt.subplots(figsize=(10,6))

sns.scatterplot(
    data=filtered_df,
    x="Sales",
    y="Profit",
    alpha=0.6,
    ax=ax4
)

sns.regplot(
    data=filtered_df,
    x="Sales",
    y="Profit",
    scatter=False,
    ax=ax4
)

high_sales = filtered_df[filtered_df["Sales"] > 8000]

sns.scatterplot(
    data=high_sales,
    x="Sales",
    y="Profit",
    color="red",
    s=80,
    label="High Value",
    ax=ax4
)

ax4.set_title("Sales vs Profit")
ax4.legend()

st.pyplot(fig4)

# =====================================================
# 📦 TOP PRODUCTS
# =====================================================
st.subheader("📦 Top Products")

top_products = filtered_df.groupby("Product.Name")["Sales"].sum().sort_values(ascending=False).head(10)

fig5, ax5 = plt.subplots(figsize=(10,5))

sns.barplot(
    x=top_products.values,
    y=top_products.index,
    hue=top_products.index,
    palette="Blues_r",
    legend=False,
    ax=ax5
)

ax5.set_title("Top Products by Sales")

st.pyplot(fig5)

# =====================================================
# 🚨 LOSS ANALYSIS
# =====================================================
st.subheader("🚨 Loss Making Transactions")

loss_df = filtered_df[filtered_df["Profit"] < 0]

st.dataframe(loss_df[["Product.Name", "Sales", "Profit"]].head(10))

st.warning(f"{len(loss_df)} loss transactions detected")

# =====================================================
# 📌 INSIGHTS
# =====================================================
st.subheader("🧠 Key Insights")

st.write("• Sales and profit relationship is not linear")
st.write("• Certain sub-categories drive most profit")
st.write("• Region performance varies significantly")

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
st.caption("🚀 Executive Sales Intelligence Dashboard")