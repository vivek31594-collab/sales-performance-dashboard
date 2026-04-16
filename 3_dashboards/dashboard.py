import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Sales Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("1_data/processed/cleaned_sales.csv")
    df["Order.Date"] = pd.to_datetime(df["Order.Date"])

    # NEW: Profit Margin
    df["Profit_Margin"] = (df["Profit"] / df["Sales"]) * 100

    return df

df = load_data()

# ---------------- HEADER ----------------
st.title("📊 Sales Intelligence & Decision Support System")
st.caption("Business Insights • Profit Optimization • Forecasting")

st.markdown("---")

# ---------------- SIDEBAR ----------------
st.sidebar.header("🔍 Filters")

date_range = st.sidebar.date_input(
    "Date Range",
    [df["Order.Date"].min(), df["Order.Date"].max()]
)

region = st.sidebar.multiselect(
    "Region", df["Region"].unique(), default=df["Region"].unique()
)

category = st.sidebar.multiselect(
    "Category", df["Category"].unique(), default=df["Category"].unique()
)

# ---------------- FILTER DATA ----------------
df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category)) &
    (df["Order.Date"] >= pd.to_datetime(date_range[0])) &
    (df["Order.Date"] <= pd.to_datetime(date_range[1]))
]

if df.empty:
    st.error("No data available")
    st.stop()

# ---------------- KPI SECTION ----------------
st.subheader("📌 Key Metrics")

total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
orders = df["Order.ID"].nunique()
aov = total_sales / orders
margin = (total_profit / total_sales) * 100

# NEW: Monthly Growth
monthly = df.groupby(df["Order.Date"].dt.to_period("M"))["Sales"].sum()

if len(monthly) > 1:
    growth = ((monthly.iloc[-1] - monthly.iloc[-2]) / monthly.iloc[-2]) * 100
else:
    growth = 0

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("💰 Sales", f"₹{total_sales:,.0f}", f"{growth:.2f}% MoM")
c2.metric("📈 Profit", f"₹{total_profit:,.0f}")
c3.metric("🛒 Orders", orders)
c4.metric("💳 AOV", f"₹{aov:,.2f}")
c5.metric("📊 Margin", f"{margin:.2f}%")

st.markdown("---")

# ---------------- SMART INSIGHTS ----------------
st.subheader("🧠 Key Insights")

region_sales = df.groupby("Region")["Sales"].sum()
top_region = region_sales.idxmax()

category_profit = df.groupby("Category")["Profit"].sum()
worst_category = category_profit.idxmin()

col1, col2, col3 = st.columns(3)

col1.success(f"🏆 {top_region} is driving maximum revenue")
col2.warning(f"⚠️ {worst_category} has lowest profitability")
col3.info("📉 High discounts are reducing profit margins")

st.markdown("---")

# ---------------- SALES TREND ----------------
st.subheader("📈 Sales Trend")

trend = df.resample("M", on="Order.Date")["Sales"].sum().reset_index()

fig = px.line(trend, x="Order.Date", y="Sales", markers=True)
st.plotly_chart(fig, use_container_width=True)

# ---------------- CATEGORY PERFORMANCE ----------------
st.subheader("📦 Category Performance")

cat = df.groupby("Category")[["Sales", "Profit"]].sum().reset_index()

fig = px.bar(
    cat,
    x="Category",
    y="Profit",
    color="Profit",
    color_continuous_scale="RdYlGn"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- PROFIT VS SALES ----------------
st.subheader("📊 Profit vs Sales")

fig = px.scatter(
    df,
    x="Sales",
    y="Profit",
    color="Category",
    hover_data=["Product.Name"]
)

st.plotly_chart(fig, use_container_width=True)

st.caption("📌 High sales but low profit indicates pricing issues")

# ---------------- LOSS-MAKING PRODUCTS ----------------
st.subheader("🚨 Loss-Making Products")

loss = df[df["Profit"] < 0]

st.dataframe(loss[["Product.Name", "Sales", "Profit"]].head(10))

st.warning("These products are causing profit leakage")

# ---------------- DISCOUNT IMPACT ----------------
st.subheader("📉 Discount vs Profit")

fig = px.scatter(df, x="Discount", y="Profit", color="Category")
st.plotly_chart(fig, use_container_width=True)

st.info("Higher discounts negatively impact profitability")

# ---------------- FORECAST ----------------
st.subheader("🔮 Sales Forecast")

forecast_df = df.groupby(pd.Grouper(key='Order.Date', freq='M'))['Sales'].sum().reset_index()
forecast_df.rename(columns={"Order.Date": "ds", "Sales": "y"}, inplace=True)

if len(forecast_df) > 2:
    from prophet import Prophet

    model = Prophet()
    model.fit(forecast_df)

    future = model.make_future_dataframe(periods=6, freq='M')
    forecast = model.predict(future)

    fig = px.line(forecast, x="ds", y="yhat")
    st.plotly_chart(fig, use_container_width=True)

# ---------------- DECISION SECTION ----------------
st.subheader("🧠 Recommended Actions")

st.markdown("""
- Increase inventory in high-performing regions  
- Reduce discounting in low-margin categories  
- Focus marketing on top-selling products  
- Investigate loss-making sub-categories  
""")

# ---------------- DOWNLOAD ----------------
st.download_button(
    "📥 Download Data",
    df.to_csv(index=False),
    "filtered_data.csv"
)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("🚀 Built by Vivek Saha")