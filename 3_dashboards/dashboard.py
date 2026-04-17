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
    df = pd.read_csv("1_data/processed/cleanedsales.csv")

    # 🔥 CLEAN COLUMN NAMES (CRITICAL FIX)
    df.columns = df.columns.str.strip().str.replace(".", "_", regex=False)

    # 🔥 SAFE DATE CONVERSION
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")

    # 🔥 SAFE PROFIT MARGIN CALC
    df["Profit_Margin"] = (df["Profit"] / df["Sales"].replace(0, pd.NA)) * 100

    return df

df = load_data()

# ---------------- HEADER ----------------
st.title("📊 Sales Intelligence & Decision Support System")
st.caption("Business Insights • Profit Optimization • Forecasting")

st.markdown("---")

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("🔍 Filters")

min_date = df["Order_Date"].min()
max_date = df["Order_Date"].max()

date_range = st.sidebar.date_input(
    "Date Range",
    [min_date, max_date]
)

region = st.sidebar.multiselect(
    "Region",
    df["Region"].dropna().unique(),
    default=df["Region"].dropna().unique()
)

category = st.sidebar.multiselect(
    "Category",
    df["Category"].dropna().unique(),
    default=df["Category"].dropna().unique()
)

# ---------------- FILTER DATA ----------------
df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category)) &
    (df["Order_Date"] >= pd.to_datetime(date_range[0])) &
    (df["Order_Date"] <= pd.to_datetime(date_range[1]))
]

if df.empty:
    st.error("No data available for selected filters")
    st.stop()

# ---------------- KPI SECTION ----------------
st.subheader("📌 Key Metrics")

total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
orders = df["Order_ID"].nunique()

aov = total_sales / orders if orders else 0
margin = (total_profit / total_sales) * 100 if total_sales else 0

monthly = df.groupby(df["Order_Date"].dt.to_period("M"))["Sales"].sum()

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
best_category = category_profit.idxmax()

col1, col2, col3 = st.columns(3)

col1.success(f"🏆 {top_region} is driving maximum revenue")
col2.warning(f"⚠️ {worst_category} has lowest profitability")
col3.info("📉 Discounts may be impacting profit margins")

st.markdown("---")

# ---------------- SALES TREND ----------------
st.subheader("📈 Sales Trend")

trend = df.resample("M", on="Order_Date")["Sales"].sum().reset_index()

fig = px.line(trend, x="Order_Date", y="Sales", markers=True)
st.plotly_chart(fig, use_container_width=True)

# ---------------- CATEGORY PERFORMANCE ----------------
st.subheader("📦 Category Performance")

cat = df.groupby("Category")[["Sales", "Profit"]].sum().reset_index()

fig = px.bar(
    cat,
    x="Category",
    y="Profit",
    color="Profit"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- PROFIT VS SALES ----------------
st.subheader("📊 Profit vs Sales")

fig = px.scatter(
    df,
    x="Sales",
    y="Profit",
    color="Category",
    hover_data=["Product_Name"]
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- LOSS MAKING PRODUCTS ----------------
st.subheader("🚨 Loss-Making Products")

loss = df[df["Profit"] < 0]

st.dataframe(
    loss[["Product_Name", "Sales", "Profit"]].head(10)
)

st.warning("These products are causing profit leakage")

# ---------------- DISCOUNT IMPACT ----------------
st.subheader("📉 Discount vs Profit")

fig = px.scatter(df, x="Discount", y="Profit", color="Category")
st.plotly_chart(fig, use_container_width=True)

# ---------------- RISK INDICATORS ----------------
st.subheader("🚨 Risk Indicators")

if margin < 15:
    st.error("Low profit margin → Immediate action required")

if growth < 0:
    st.error("Negative growth → Business decline risk")

if len(loss) > 0:
    st.warning("Loss-making products detected")

st.markdown("---")

# ---------------- FORECAST (SAFE IMPORT) ----------------
st.subheader("🔮 Sales Forecast")

try:
    from prophet import Prophet

    forecast_df = df.groupby(pd.Grouper(key="Order_Date", freq="M"))["Sales"].sum().reset_index()
    forecast_df.columns = ["ds", "y"]

    if len(forecast_df) > 2:
        model = Prophet()
        model.fit(forecast_df)

        future = model.make_future_dataframe(periods=6, freq="M")
        forecast = model.predict(future)

        fig = px.line(forecast, x="ds", y="yhat")
        st.plotly_chart(fig, use_container_width=True)

        st.info("Forecast generated using Prophet model")

except Exception as e:
    st.warning("Forecasting module skipped (Prophet not available or data insufficient)")

# ---------------- DOWNLOAD ----------------
st.download_button(
    "📥 Download Data",
    df.to_csv(index=False),
    "filtered_data.csv"
)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("🚀 Built by Vivek Saha")