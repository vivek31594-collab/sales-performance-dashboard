-- =====================================================
-- 🔍 SALES DATA QUALITY ASSURANCE LAYER
-- Author: Vivek Saha
-- Purpose: Ensure dataset integrity before analytics
-- =====================================================

USE sales_analysis;

-- =========================
-- 1. NULL VALUE VALIDATION
-- =========================
SELECT 
    SUM(CASE WHEN Region IS NULL OR Region = '' THEN 1 ELSE 0 END) AS Null_Region,
    SUM(CASE WHEN Market IS NULL OR Market = '' THEN 1 ELSE 0 END) AS Null_Market,
    SUM(CASE WHEN Category IS NULL OR Category = '' THEN 1 ELSE 0 END) AS Null_Category,
    SUM(CASE WHEN Sales IS NULL THEN 1 ELSE 0 END) AS Null_Sales,
    SUM(CASE WHEN Profit IS NULL THEN 1 ELSE 0 END) AS Null_Profit
FROM sales;

-- =========================
-- 2. DUPLICATE RECORD CHECK
-- =========================
SELECT 
    Region,
    Market,
    Category,
    Sub_Category,
    Product_Name,
    COUNT(*) AS Duplicate_Count
FROM sales
GROUP BY Region, Market, Category, Sub_Category, Product_Name
HAVING COUNT(*) > 1;

-- =========================
-- 3. INVALID DATA CHECK (LOGICAL ERRORS)
-- =========================
SELECT *
FROM sales
WHERE Sales < 0
   OR Profit < -100000
   OR Sales IS NULL
   OR Profit IS NULL;

-- =========================
-- 4. DATA SUMMARY SNAPSHOT
-- =========================
SELECT 
    COUNT(*) AS Total_Records,
    SUM(Sales) AS Total_Sales,
    SUM(Profit) AS Total_Profit,
    ROUND(AVG(Sales), 2) AS Avg_Sales,
    ROUND(AVG(Profit), 2) AS Avg_Profit
FROM sales;