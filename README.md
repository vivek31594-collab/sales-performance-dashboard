# 📊 Sales Performance Analytics Dashboard

🧑‍💻 Author: Vivek Saha  

---

# 📌 Project Overview

This project is an end-to-end **Sales Analytics & Data Engineering solution** that transforms raw transactional data into actionable business insights using SQL, Python, and Streamlit.

It simulates a real-world enterprise analytics pipeline used in consulting firms such as PwC, Deloitte, and KPMG.

---

# 🎯 Business Objective

The objective is to analyze sales performance and enable data-driven decision-making.

Key goals:
- Identify revenue and profit trends
- Detect loss-making products
- Evaluate regional and category performance
- Monitor business profitability
- Ensure data quality before analytics
- Provide actionable business recommendations

---

# 🧭 Business Story Flow (End-to-End Pipeline)

📥 Data Ingestion → Raw CSV Sales Data  
🔧 Data Engineering → Schema + Cleaning in SQL  
🔍 Data Quality Layer → Validation + PASS/FAIL checks  
⚙️ Processing Layer → Pandas transformations  
📊 Analytics Layer → KPIs + Trends  
🧠 Insights Layer → Business interpretation  
📌 Decision Layer → Recommendations for business improvement  
🚀 Deployment Layer → Streamlit Dashboard (Cloud)

---

# 🏗️ Project Architecture
Raw CSV Data
↓
MySQL (Data Storage)
↓
SQL Data Quality Layer
↓
Python (Pandas Processing)
↓
Analytics & KPI Engine
↓
Streamlit Dashboard
↓
Cloud Deployment


---

# 🧹 Data Engineering Layer

- Structured schema design
- Column standardization
- Handling encoding issues (cp1252)
- Data type normalization

---

# 🔍 Data Quality Framework

✔ Null value detection  
✔ Duplicate record detection  
✔ Business rule validation  
✔ Profit & Sales consistency checks  
✔ Shipping and date validation  
✔ Final PASS/FAIL dataset readiness flag  

---

# ⚙️ Data Pipeline Automation (IMPORTANT)

This project follows a structured ETL-style pipeline:

## 📥 1. Data Ingestion
Raw sales data imported from CSV into MySQL.

## 🧹 2. Data Engineering
Schema design and structured data formatting.

## 🔍 3. Data Quality Layer
SQL-based validation:
- Missing values
- Duplicates
- Business rule violations

## ⚙️ 4. Processing Layer
Python-based transformations:
- Profit Margin calculation
- Time-series feature creation

## 📊 5. Analytics Layer
- KPI generation
- Sales & profit trends
- Segment analysis

## 📈 6. Visualization Layer
Streamlit dashboard for interactive insights.

## 🚀 7. Deployment
Hosted on Streamlit Cloud for live access.

---

# 📊 Key SQL Outputs

- Total Revenue & Profit
- Region-wise performance
- Category analysis
- Loss-making products
- Data quality validation results

---

# 📊 Key Dashboard Features

- Executive KPI Summary
- Data Quality Score Indicator
- Sales trend analysis
- Category & region insights
- Profit vs Sales relationship
- Loss-making product detection
- Discount impact analysis
- Risk indicators dashboard
- Downloadable dataset

---

# 🧠 Business Insights

- Certain regions contribute disproportionately to revenue
- Discounts negatively impact profit margins
- Specific product categories generate losses
- Profitability varies significantly across segments

---

# 💡 Business Recommendations (NEW – IMPORTANT)

Based on analytics findings:

✔ Reduce excessive discounts in low-margin categories  
✔ Focus marketing efforts on high-performing regions  
✔ Review or discontinue consistently loss-making products  
✔ Optimize pricing strategy for underperforming segments  
✔ Improve inventory allocation based on demand patterns  

---

# 📊 KPI Interpretation (Executive Layer)

- **Revenue:** Indicates overall business scale  
- **Profit:** Measures actual business sustainability  
- **Margin:** Indicates pricing and cost efficiency  
- **Orders:** Reflects customer demand strength  
- **Growth Rate:** Shows business trajectory  

---

# ⚠️ Assumptions & Data Handling

- Missing values handled using safe imputation or removal  
- Zero sales values excluded from margin calculations  
- Date inconsistencies cleaned and standardized  
- Duplicate records treated as data quality issues  
- Encoding issues handled (cp1252 format)

---

# ⚙️ Tech Stack

- MySQL → Data storage & validation  
- SQL → Data quality & analytics  
- Python (Pandas) → Processing & feature engineering  
- Streamlit → Dashboard UI  
- Plotly → Visualizations  
- Git/GitHub → Version control  
- Streamlit Cloud → Deployment  

---

# 🧠 Skills Demonstrated

- Data Engineering  
- SQL Data Quality Framework  
- Business Intelligence  
- Analytical Thinking  
- Dashboard Development  
- End-to-End Pipeline Design  
- Consulting-style storytelling  

---

# 🚀 Future Improvements

- Automate ETL pipeline using Airflow / Python scheduler  
- Add real-time streaming data support  
- Integrate Power BI dashboard layer  
- Deploy API-based architecture  
- Add predictive forecasting (ML layer)

---

# 📌 Project Impact

This project demonstrates a **real-world analytics workflow** from raw data ingestion to business decision-making.

It reflects strong capability in:
- Data engineering
- Data analysis
- Business intelligence
- Dashboard development

Making it suitable for **Data Analyst / Business Analyst roles in consulting and product companies**.

---

# 🚀 Built by Vivek Saha  
Sales Analytics | Data Engineering | Business Intelligence