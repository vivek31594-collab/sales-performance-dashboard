-- =====================================================
-- 📦 SALES ANALYTICS PROJECT - DATA ENGINEERING LAYER
-- Author: Vivek Saha
-- Purpose: Create database, schema, and load dataset
-- =====================================================

-- =========================
-- 1. DATABASE SETUP
-- =========================
CREATE DATABASE IF NOT EXISTS sales_analysis;
USE sales_analysis;

-- =========================
-- 2. CLEAN TABLE RECREATION
-- =========================
DROP TABLE IF EXISTS sales;

CREATE TABLE sales (
    Region VARCHAR(50),
    Market VARCHAR(50),
    Category VARCHAR(100),
    Sub_Category VARCHAR(100),
    Product_Name VARCHAR(255),
    Sales DOUBLE,
    Profit DOUBLE
);

-- =========================
-- 3. DATA LOAD (CSV IMPORT)
-- =========================
-- NOTE: Use LOCAL INFILE for portability across systems

LOAD DATA LOCAL INFILE 'C:/Users/User/Downloads/sales-analysis-dashboard/data/cleanedsales.csv'
INTO TABLE sales
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- =========================
-- 4. VALIDATION CHECK (MANDATORY)
-- =========================
SELECT 
    COUNT(*) AS Total_Rows_Loaded,
    SUM(Sales) AS Total_Sales,
    SUM(Profit) AS Total_Profit
FROM sales;