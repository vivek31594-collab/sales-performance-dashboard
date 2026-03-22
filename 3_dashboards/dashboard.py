import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Sales Performance Dashboard",
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

# ---------------- TITLE ----------------
st.markdown("""
<h1 style='text-align: center; color: #2E86C1;'>📊 Sales Performance Dashboard</h1>
<p style='text-align: center;'>Advanced Business Insights & Forecasting</p>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------------- SIDEBAR ----------------
st.sidebar.header("🔎 Filters")

min_date = df["Order.Date"].min()
max_date = df["Order.Date"].max()

date_range = st.sidebar.date_input(
    "Date Range",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

region_list = st.sidebar.multiselect(
    "Region",
    df["Region"].unique(),
    default=df["Region"].unique()
)

category_list = st.sidebar.multiselect(
    "Category",
    df["Category"].unique(),
    default=df["Category"].unique()
)

top_n = st.sidebar.slider("Top N Products", 5, 20, 10)

# ---------------- FILTER DATA ----------------
df_selection = df[
    (df["Region"].isin(region_list)) &
    (df["Category"].isin(category_list)) &
    (df["Order.Date"] >= pd.to_datetime(date_range[0])) &
    (df["Order.Date"] <= pd.to_datetime(date_range[1]))
].copy()

if df_selection.empty:
    st.warning("⚠️ No data for selected filters")
    st.stop()

# ---------------- KPI CALCULATIONS ----------------
total_sales = df_selection["Sales"].sum()
total_profit = df_selection["Profit"].sum()
total_orders = df_selection["Order.ID"].nunique()
avg_order_value = total_sales / total_orders
profit_margin = (total_profit / total_sales) * 100

df_selection["Year"] = df_selection["Order.Date"].dt.year
sales_by_year = df_selection.groupby("Year")["Sales"].sum()

yoy_growth = sales_by_year.pct_change().iloc[-1] if len(sales_by_year) > 1 else 0

# ---------------- KPI SECTION ----------------
st.markdown("## 📌 Key Metrics")

col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.metric("💰 Sales", f"${total_sales:,.0f}")
col2.metric("📈 Profit", f"${total_profit:,.0f}")
col3.metric("🛒 Orders", total_orders)
col4.metric("💳 AOV", f"${avg_order_value:,.2f}")
col5.metric("📊 Margin", f"{profit_margin:.2f}%")
col6.metric("📈 YoY", f"{yoy_growth:.2%}")

st.markdown("---")

# ---------------- DYNAMIC INSIGHTS ----------------
st.markdown("## 🧠 Smart Insights")

top_region = df_selection.groupby("Region")["Sales"].sum().idxmax()
top_category = df_selection.groupby("Category")["Sales"].sum().idxmax()

worst_category = df_selection.groupby("Category")["Profit"].sum().idxmin()

st.success(f"🏆 Top Region: {top_region}")
st.success(f"📦 Best Category: {top_category}")
st.warning(f"⚠️ Lowest Profit Category: {worst_category}")

# ---------------- TABS ----------------
tab1, tab2, tab3, tab4 = st.tabs(["📈 Sales", "🌍 Region", "📦 Products", "🔮 Forecast"])

# ---------------- TAB 1: SALES ----------------
with tab1:
    st.subheader("Sales Overview")

    sales_category = df_selection.groupby("Category")["Sales"].sum().reset_index()

    fig1 = px.bar(
        sales_category,
        x="Category",
        y="Sales",
        color="Category",
        template="plotly_white"
    )

    sales_trend = df_selection.resample("M", on="Order.Date")["Sales"].sum().reset_index()

    fig2 = px.line(
        sales_trend,
        x="Order.Date",
        y="Sales",
        markers=True,
        template="plotly_white"
    )

    col1, col2 = st.columns(2)
    col1.plotly_chart(fig1, use_container_width=True)
    col2.plotly_chart(fig2, use_container_width=True)

# ---------------- TAB 2: REGION ----------------
with tab2:
    st.subheader("Regional Performance")

    region_sales = df_selection.groupby("Region")["Sales"].sum().reset_index()

    fig = px.pie(
        region_sales,
        names="Region",
        values="Sales",
        hole=0.4
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------- TAB 3: PRODUCTS ----------------
with tab3:
    st.subheader("Top Products")

    top_products = (
        df_selection.groupby("Product.Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )

    fig = px.bar(
        top_products,
        x="Sales",
        y="Product.Name",
        orientation="h",
        color="Sales",
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------- TAB 4: FORECAST ----------------
with tab4:
    st.subheader("6-Month Forecast")

    forecast_df = df_selection.groupby(
        pd.Grouper(key='Order.Date', freq='M')
    )['Sales'].sum().reset_index()

    forecast_df.rename(columns={"Order.Date": "ds", "Sales": "y"}, inplace=True)

    if len(forecast_df) < 2:
        st.warning("Not enough data for forecasting")
    else:
        from prophet import Prophet

        model = Prophet()
        model.fit(forecast_df)

        future = model.make_future_dataframe(periods=6, freq='M')
        forecast = model.predict(future)

        fig = px.line(forecast, x="ds", y="yhat")
        st.plotly_chart(fig, use_container_width=True)

# ---------------- DOWNLOAD ----------------
st.download_button(
    "📥 Download Data",
    df_selection.to_csv(index=False),
    "filtered_data.csv"
)

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("Built by **Vivek Saha** | Data Analyst Portfolio 🚀")