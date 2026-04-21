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
# 📊 MONTHLY TREND (SINGLE SOURCE)
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

c1, c2, c3, c4 = st.columns(4)
c1.metric("Revenue", f"{sales:,.0f}")
c2.metric("Profit", f"{profit:,.0f}")
c3.metric("Orders", orders)
c4.metric("Margin %", f"{margin:.2f}%")

st.markdown("---")

# =====================================================
# 🧠 EXECUTIVE INSIGHTS
# =====================================================
st.markdown("## 🧠 Executive Business Health")

loss_df = df[df["Profit"] < 0]
loss_impact = abs(loss_df["Profit"].sum())
loss_ratio = loss_impact / profit if profit else 0

growth = monthly["Sales"].pct_change().iloc[-1] * 100 if len(monthly) > 1 else 0
volatility = monthly["Sales"].std() / monthly["Sales"].mean() if monthly["Sales"].mean() != 0 else 0

insights = []

if margin < 10:
    insights.append("Low profitability → pricing or cost issue.")
elif margin < 25:
    insights.append("Moderate profitability → optimization possible.")
else:
    insights.append("Strong profitability.")

if loss_df.empty:
    insights.append("No loss-making products.")
else:
    insights.append("Loss-making products impacting profit.")

if growth < 0:
    insights.append("Sales declining → demand issue.")
else:
    insights.append("Sales stable/growing.")

if volatility > 0.5:
    insights.append("High volatility in demand.")
else:
    insights.append("Stable demand pattern.")

for i, ins in enumerate(insights, 1):
    st.write(f"{i}. {ins}")

st.markdown("---")

# =====================================================
# 📈 TREND ANALYSIS (FINAL)
# =====================================================
st.markdown("## 📈 Business Trend Intelligence")

monthly["Sales_Growth"] = monthly["Sales"].pct_change() * 100
monthly["Profit_Growth"] = monthly["Profit"].pct_change() * 100

fig = px.line(
    monthly.reset_index(),
    x="Order.Date",
    y=["Sales", "Profit"],
    title="Sales vs Profit Trend",
    markers=True
)

fig.update_layout(
    xaxis_title="Month",
    yaxis_title="Value",
    legend_title="Metric"
)

st.plotly_chart(fig, use_container_width=True)

if not monthly.empty:
    peak_month = monthly["Sales"].idxmax().strftime("%B %Y")
    low_month = monthly["Sales"].idxmin().strftime("%B %Y")

    st.write(f"""
    - 📈 Peak Month: **{peak_month}**  
    - 📉 Lowest Month: **{low_month}**  
    - 📊 Avg Monthly Sales: **{monthly['Sales'].mean():,.0f}**
    """)

    latest_sales_growth = monthly["Sales_Growth"].iloc[-1]
    latest_profit_growth = monthly["Profit_Growth"].iloc[-1]

    if latest_sales_growth > 0 and latest_profit_growth > 0:
        st.success("Growth in both sales and profit.")
    elif latest_sales_growth > 0 and latest_profit_growth < 0:
        st.warning("Sales up but profit down → margin issue.")
    elif latest_sales_growth < 0 and latest_profit_growth < 0:
        st.error("Both declining → demand issue.")
    else:
        st.info("Mixed trend.")

st.markdown("---")

# =====================================================
# ⚠️ LOSS ANALYSIS (FIXED PROPERLY)
# =====================================================
st.markdown("## ⚠️ Profit Leakage Analysis")

if loss_df.empty:
    st.success("No loss-making transactions.")
else:
    top_loss = loss_df.groupby("Product.Name")["Profit"].sum().sort_values().head(10)
    st.bar_chart(top_loss)

    st.write(f"Total Loss Impact: **{loss_impact:,.0f}**")

    loss_monthly = (
        loss_df.set_index("Order.Date")
        .resample("MS")
        .agg({"Profit": "sum"})
    )

    if not loss_monthly.empty:
        loss_monthly["Loss"] = loss_monthly["Profit"].abs()

        # ✅ FIXED PLOTLY INTEGRATION
        fig_loss = px.line(
            loss_monthly.reset_index(),
            x="Order.Date",
            y="Loss",
            title="Loss Trend Over Time",
            markers=True
        )

        st.plotly_chart(fig_loss, use_container_width=True)

        latest_loss = loss_monthly["Loss"].iloc[-1]
        avg_loss = loss_monthly["Loss"].mean()

        if latest_loss > avg_loss:
            st.warning("Loss increasing.")
        else:
            st.success("Loss improving.")

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
# 🧠 PRIORITY MATRIX
# =====================================================
st.markdown("## 🧠 Action Priority Matrix")

priority_df = pd.DataFrame([
    {"Area": "Profit Margin", "Score": max(0, 100 - margin)},
    {"Area": "Loss Leakage", "Score": loss_ratio * 100},
    {"Area": "Growth Stability", "Score": abs(growth)}
]).sort_values("Score", ascending=False)

st.dataframe(priority_df)

st.markdown("---")

# =====================================================
# 📊 80/20 ANALYSIS
# =====================================================
st.markdown("## 📊 Business Concentration")

top_region = (df.groupby("Region")["Sales"].sum().nlargest(3).sum() / sales) * 100
top_category = (df.groupby("Category")["Profit"].sum().nlargest(2).sum() / profit) * 100 if profit != 0 else 0

st.write(f"Top 3 regions → {top_region:.2f}% revenue")
st.write(f"Top 2 categories → {top_category:.2f}% profit")

st.markdown("---")

# =====================================================
# 📌 RECOMMENDATIONS
# =====================================================
st.markdown("## 📌 Recommendations")

if margin < 15:
    st.write("🔴 Improve pricing")

if not loss_df.empty:
    st.write("🔴 Fix loss-making products")

if growth < 0:
    st.write("🔴 Improve demand strategy")

st.write("🟢 Focus on high-margin segments")

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

st.caption("🚀 Final Executive Dashboard")