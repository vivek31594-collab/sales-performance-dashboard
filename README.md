📊 Sales Performance Analytics Dashboard
🧑‍💻 Author

Vivek Saha

📌 Project Overview

This project is a end-to-end Sales Analytics solution that combines data engineering, SQL-based data validation, and dashboard development to extract meaningful business insights from raw sales data.

The system ensures data quality, consistency, and analytical readiness before building dashboards and reporting layers.

🎯 Business Objective

To analyze sales performance across regions, products, and customers in order to:

Identify revenue trends
Detect loss-making products
Evaluate profit margins
Ensure data integrity before analytics
Support business decision-making with clean data
🏗️ Project Architecture
Raw CSV Data
     ↓
Data Import (MySQL Workbench)
     ↓
Data Engineering Layer (Schema + Validation)
     ↓
Data Quality Checks (SQL Scripts)
     ↓
Analytics Layer (KPIs + Aggregations)
     ↓
Dashboard (Streamlit / Visualization Layer)
🧹 Data Engineering Layer
Schema definition for structured ingestion
Handling of encoding issues (cp1252)
Standardized column naming conventions
Structured table design for analytics readiness
🔍 Data Quality Framework

The project includes a production-grade validation system:

✔ Data Integrity Checks
Null value detection across all key columns
Duplicate record identification (Order + Product level)
Missing value percentage analysis
✔ Business Rule Validation
Sales > 0
Quantity > 0
Profit not null
Shipping date ≥ order date
✔ Consistency Checks
Profit cannot exceed Sales
Shipping cost validation
Margin anomaly detection
✔ Data Freshness
Latest order date tracking
Dataset recency monitoring
✔ Final Quality Flag
Automated PASS / FAIL system for dataset readiness
📊 Key SQL Analysis Outputs
Total Revenue
Total Profit
Average Sales & Profit
Region-wise performance
Top & bottom performing products
Loss-making product detection
⚙️ Tech Stack
MySQL – Data storage & SQL analytics
SQL – Data cleaning & validation
Python (optional layer) – Dashboard integration
Streamlit (optional) – Visualization layer
Git & GitHub – Version control
📁 Project Structure
sales-analysis-dashboard/
│
├── 1_data/
├── 2_notebooks/
│
├── 3_dashboards/
│
├── 4_sql/
│   ├── sql_analysis.sql
│
├── setup/
│   ├── create_load.sql
│   ├── create_and_load.sql
│
├── utils/
│   ├── __init__.py
│   ├── datacleaning.py
│   ├── dataloader.py
│
├── screenshots/
│   ├── duplicate_check.png
│   ├── invalid_data_check.png
│   ├── null_check.png
│
├── .gitignore
├── requirements.txt
├── README.md
📈 Key Insights
Identified high-performing regions contributing majority revenue
Detected loss-making products impacting profitability
Found inconsistencies in shipping cost vs sales data
Established clean dataset pipeline for analytics reporting
🧠 Skills Demonstrated
Data Cleaning & Validation (SQL)
Data Engineering Fundamentals
Business Problem Solving
Analytical Thinking
Data Quality Framework Design
Dashboard Readiness Preparation
🚀 Future Improvements
Automate data pipeline using Python ETL
Add real-time dashboard updates
Integrate Power BI for advanced visualization
Deploy dashboard on cloud
📌 Conclusion

This project demonstrates a complete data analytics pipeline from raw data to business insights, focusing heavily on data quality assurance and structured analytics design, making it suitable for real-world business reporting systems.