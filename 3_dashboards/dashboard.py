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
    return df

df = load_data()

# ---------------- HEADER ----------------
st.markdown("""
<h1 style='text-align: center; color: #2E86C1;'>📊 Sales Intelligence Dashboard</h1>
<p style='text-align: center;'>Business Insights • Profit Optimization • Forecasting</p>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------------- SIDEBAR ----------------
st.sidebar.header("🔎 Filters")

min_date = df["Order.Date"].min()
max_date = df["Order.Date"].max()

date_range = st.sidebar.date_input("Date Range", [min_date, max_date])

region_list = st.sidebar.multiselect("Region", df["Region"].unique(), default=df["Region"].unique())
category_list = st.sidebar.multiselect("Category", df["Category"].unique(), default=df["Category"].unique())

top_n = st.sidebar.slider("Top Products", 5, 20, 10)

# ---------------- FILTER ----------------
df_selection = df[
    (df["Region"].isin(region_list)) &
    (df["Category"].isin(category_list)) &
    (df["Order.Date"] >= pd.to_datetime(date_range[0])) &
    (df["Order.Date"] <= pd.to_datetime(date_range[1]))
].copy()

if df_selection.empty:
    st.warning("No data available")
    st.stop()

# ---------------- KPI ----------------
total_sales = df_selection["Sales"].sum()
total_profit = df_selection["Profit"].sum()
orders = df_selection["Order.ID"].nunique()
aov = total_sales / orders
margin = (total_profit / total_sales) * 100

df_selection["Year"] = df_selection["Order.Date"].dt.year
sales_by_year = df_selection.groupby("Year")["Sales"].sum()
yoy = sales_by_year.pct_change().iloc[-1] if len(sales_by_year) > 1 else 0

st.markdown("## 📌 Key Metrics")
c1, c2, c3, c4, c5, c6 = st.columns(6)

c1.metric("💰 Sales", f"${total_sales:,.0f}")
c2.metric("📈 Profit", f"${total_profit:,.0f}")
c3.metric("🛒 Orders", orders)
c4.metric("💳 AOV", f"${aov:,.2f}")
c5.metric("📊 Margin", f"{margin:.2f}%")
c6.metric("📈 YoY", f"{yoy:.2%}")

st.markdown("---")

# ---------------- SMART INSIGHTS ----------------
st.markdown("## 🧠 Smart Insights")

top_region = df_selection.groupby("Region")["Sales"].sum().idxmax()
top_category = df_selection.groupby("Category")["Sales"].sum().idxmax()
worst_category = df_selection.groupby("Category")["Profit"].sum().idxmin()

col1, col2, col3 = st.columns(3)
col1.success(f"🏆 Top Region: {top_region}")
col2.success(f"📦 Best Category: {top_category}")
col3.error(f"⚠️ Lowest Profit Category: {worst_category}")

# ---------------- BUSINESS RECOMMENDATIONS ----------------
st.markdown("## 📌 Business Recommendations")

if margin < 10:
    st.error("Profit margin is low — reduce discounts or optimize costs")

if yoy < 0:
    st.warning("Negative growth detected — investigate declining segments")

st.success(f"Focus marketing and inventory on {top_region} region")

# ---------------- ROOT CAUSE ANALYSIS ----------------
st.markdown("## 🔍 Root Cause Analysis")

subcat_profit = df_selection.groupby("Sub.Category")["Profit"].sum().reset_index()
low_profit_subcat = subcat_profit.sort_values(by="Profit").head(5)

st.write("### ⚠️ Lowest Profit Sub-Categories")
st.dataframe(low_profit_subcat)

if not low_profit_subcat.empty:
    worst_sub = low_profit_subcat.iloc[0]["Sub.Category"]
    st.error(f"Major profit leakage is coming from '{worst_sub}' sub-category")

# ---------------- PROFIT VS SALES ----------------
st.markdown("## 📊 Profit vs Sales Analysis")

fig_scatter = px.scatter(
    df_selection,
    x="Sales",
    y="Profit",
    color="Category",
    hover_data=["Product.Name"]
)

st.plotly_chart(fig_scatter, use_container_width=True)
st.info("High sales but low profit products indicate pricing or cost issues.")

# ---------------- TABS ----------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📈 Sales", "🌍 Region", "📦 Products", "👥 Segment", "🔮 Forecast"]
)

# ---------------- SALES ----------------
with tab1:
    sales_cat = df_selection.groupby("Category")["Sales"].sum().reset_index()
    fig1 = px.bar(sales_cat, x="Category", y="Sales", color="Category")

    trend = df_selection.resample("M", on="Order.Date")["Sales"].sum().reset_index()
    fig2 = px.line(trend, x="Order.Date", y="Sales", markers=True)

    c1, c2 = st.columns(2)
    c1.plotly_chart(fig1, use_container_width=True)
    c2.plotly_chart(fig2, use_container_width=True)

# ---------------- REGION ----------------
with tab2:
    region = df_selection.groupby("Region")["Sales"].sum().reset_index()
    fig = px.pie(region, names="Region", values="Sales", hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

# ---------------- PRODUCTS ----------------
with tab3:
    top_products = (
        df_selection.groupby("Product.Name")["Sales"]
        .sum().sort_values(ascending=False).head(top_n).reset_index()
    )

    fig = px.bar(top_products, x="Sales", y="Product.Name", orientation="h", color="Sales")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### ❌ Loss Making Products")
    loss = df_selection[df_selection["Profit"] < 0]
    st.dataframe(loss[["Product.Name", "Sales", "Profit"]].head(10))

# ---------------- SEGMENT ----------------
with tab4:
    seg = df_selection.groupby("Segment")["Sales"].sum().reset_index()
    fig = px.bar(seg, x="Segment", y="Sales", color="Segment")
    st.plotly_chart(fig, use_container_width=True)

# ---------------- FORECAST ----------------
with tab5:
    st.info("Forecast based on historical trends for business planning")

    forecast_df = df_selection.groupby(
        pd.Grouper(key='Order.Date', freq='M')
    )['Sales'].sum().reset_index()

    forecast_df.rename(columns={"Order.Date": "ds", "Sales": "y"}, inplace=True)

    if len(forecast_df) < 2:
        st.warning("Not enough data for forecast")
    else:
        from prophet import Prophet

        model = Prophet()
        model.fit(forecast_df)

        future = model.make_future_dataframe(periods=6, freq='M')
        forecast = model.predict(future)

        fig = px.line(forecast, x="ds", y="yhat")
        st.plotly_chart(fig, use_container_width=True)

        st.success("Use forecast for demand planning and inventory optimization.")

# ---------------- DOWNLOAD ----------------
st.download_button(
    "📥 Download Data",
    df_selection.to_csv(index=False),
    "filtered_data.csv"
)

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("🚀 Built by Vivek Saha | Data Analyst Portfolio")