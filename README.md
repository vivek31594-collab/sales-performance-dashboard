# 📊 Sales Analysis Dashboard

## Project Overview

The **Sales Analysis Dashboard** project analyzes retail sales data and provides interactive visualizations to understand business performance.

The project uses **Python for data analysis** and **Streamlit to build an interactive dashboard** that helps explore key sales metrics such as revenue, profit, product performance, and regional trends.

This project demonstrates the practical skills required for a **Data Analyst role**, including:

* Data cleaning and preprocessing
* Exploratory Data Analysis (EDA)
* Data visualization
* Business insights generation
* Dashboard development

---

# 🎯 Project Objectives

The main objectives of this project are:

* Analyze sales performance across different regions
* Identify the most profitable product categories
* Understand customer segments and buying behavior
* Track sales trends over time
* Build an interactive dashboard for business decision making

---

# 🛠 Tools and Technologies

The following tools and technologies were used in this project:

| Tool             | Purpose                       |
| ---------------- | ----------------------------- |
| Python           | Data analysis and processing  |
| Pandas           | Data manipulation             |
| NumPy            | Numerical computations        |
| Matplotlib       | Data visualization            |
| Seaborn          | Statistical visualization     |
| Plotly           | Interactive charts            |
| Streamlit        | Dashboard development         |
| Jupyter Notebook | Data analysis and exploration |

---

# 📂 Project Structure

sales_dashboard_project/

data/
  superstore_sales.csv → Dataset used for analysis

notebooks/
  sales_analysis.ipynb → Exploratory data analysis and insights

dashboards/
  dashboard.py → Streamlit dashboard application

utils/
  data_loader.py → Helper functions for loading data

requirements.txt → List of Python dependencies

README.md → Project documentation

venv/ → Virtual environment for project dependencies

---

# 📊 Dataset Description

The dataset contains retail sales data with the following fields:

| Column        | Description                                         |
| ------------- | --------------------------------------------------- |
| Order ID      | Unique order identifier                             |
| Order Date    | Date when order was placed                          |
| Ship Date     | Date when order was shipped                         |
| Customer Name | Name of the customer                                |
| Segment       | Customer segment (Consumer, Corporate, Home Office) |
| Region        | Sales region                                        |
| Category      | Product category                                    |
| Sub Category  | Product sub-category                                |
| Product Name  | Name of the product                                 |
| Sales         | Revenue generated                                   |
| Quantity      | Number of items sold                                |
| Discount      | Discount applied                                    |
| Profit        | Profit earned                                       |

This dataset allows analysis of **sales trends, customer behavior, and profitability**.

---

# 📈 Key Analysis Performed

The following analyses were performed during the project:

### 1. Sales Trend Analysis

Analyzed how sales change over time using monthly and yearly sales trends.

### 2. Regional Performance

Compared total sales and profit across different regions.

### 3. Product Category Analysis

Identified the best-performing and worst-performing product categories.

### 4. Customer Segment Analysis

Analyzed purchasing behavior across customer segments.

### 5. Profitability Analysis

Determined which products generate the highest profit.

---

# 📊 Dashboard Features

The Streamlit dashboard includes the following features:

* Total Sales KPI
* Total Profit KPI
* Category-wise sales distribution
* Regional sales comparison
* Monthly sales trend visualization
* Interactive filtering options
* Data table preview

These features allow users to **interactively explore sales performance**.

---

# 🚀 How to Run the Project

Follow these steps to run the project locally.

### 1. Clone the Repository

git clone https://github.com/yourusername/sales_dashboard_project.git

---

### 2. Navigate to the Project Folder

cd sales_dashboard_project

---

### 3. Create Virtual Environment

python -m venv venv

---

### 4. Activate Virtual Environment

Windows

venv\Scripts\activate

---

### 5. Install Dependencies

pip install -r requirements.txt

---

### 6. Run the Streamlit Dashboard

streamlit run dashboards/dashboard.py

After running the command, the dashboard will open in your browser.

---

# 📷 Dashboard Preview

The dashboard provides interactive visualizations that allow users to explore:

* Sales performance
* Profit trends
* Regional comparisons
* Product category insights

---

# 📌 Key Business Insights

Some insights that can be obtained from this dashboard include:

* Which region generates the highest revenue
* Which product category contributes most to sales
* Monthly sales growth trends
* Customer segments with the highest purchasing power
* Most profitable products

These insights help businesses **improve sales strategy and decision making**.

---

# 🔮 Future Improvements

Possible improvements for this project include:

* Adding forecasting models for sales prediction
* Integrating real-time data sources
* Improving dashboard interactivity
* Deploying the dashboard online using Streamlit Cloud

---

## Live Dashboard

https://sales-performance-dashboard-kfyh3y4ibdsr6gka6yymla.streamlit.app/

## Project Workflow

### 1. Data Collection
The retail sales dataset was collected and stored in the project data directory. The dataset contains information such as order details, product categories, regional sales, and profit metrics.

### 2. Data Loading
The dataset was loaded into Python using the Pandas library through a reusable data loader module to ensure modular and maintainable code.

### 3. Data Cleaning and Preprocessing
The dataset was cleaned to ensure data quality. Key steps included:
- Handling missing values
- Removing duplicate records
- Converting date columns into proper datetime format
- Standardizing column names
- Preparing the dataset for analysis

### 4. Exploratory Data Analysis (EDA)
Exploratory data analysis was conducted to understand sales patterns and business trends. This included:
- Analyzing sales distribution across categories
- Evaluating regional performance
- Identifying top-performing products
- Understanding sales trends over time

### 5. Data Visualization
Multiple visualizations were created using Plotly and Matplotlib to highlight key insights such as:
- Monthly sales trends
- Sales by product category
- Regional sales distribution
- Top 10 products by revenue

### 6. Dashboard Development
An interactive dashboard was developed using Streamlit to present key business metrics and visual insights. The dashboard includes:
- KPI metrics (Total Sales, Profit, Orders)
- Interactive filters for Region and Category
- Dynamic charts for trend analysis and product performance

### 7. Deployment
The dashboard application was deployed using Streamlit Cloud, enabling users to interact with the analysis through a web-based interface.

# 👨‍💻 Author

Vivek Saha
Aspiring Data Analyst

Skills demonstrated in this project:

* Data Analysis
* Data Visualization
* Python Programming
* Business Intelligence
* Dashboard Development
