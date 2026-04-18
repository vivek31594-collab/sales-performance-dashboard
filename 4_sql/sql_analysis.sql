-- =====================================================
-- 📊 SALES ANALYTICS DASHBOARD PROJECT (FINAL UPGRADED)
-- Author: Vivek Saha
-- Purpose: End-to-end business performance analysis using SQL
-- Skills: Aggregations, Window Functions, CTEs, HAVING, Bucketing, Data Quality Awareness
-- =====================================================

USE sales_analysis;

-- =====================================================
-- 0️⃣ SAFETY FILTER (DATA CLEANLINESS LAYER)
-- =====================================================
-- Ensures nulls do not break calculations
-- (Industry best practice)

-- =====================================================
-- 1️⃣ KPI SUMMARY (EXECUTIVE OVERVIEW)
-- =====================================================
SELECT 
    COUNT(*) AS Total_Transactions,
    SUM(Sales) AS Total_Sales,
    SUM(Profit) AS Total_Profit,
    ROUND(SUM(Profit) * 100.0 / NULLIF(SUM(Sales), 0), 2) AS Profit_Margin_Percent,
    ROUND(AVG(Profit), 2) AS Avg_Profit_Per_Transaction
FROM sales
WHERE Sales IS NOT NULL AND Profit IS NOT NULL;


-- =====================================================
-- 2️⃣ REGION PERFORMANCE + CONTRIBUTION %
-- =====================================================
SELECT 
    Region,
    SUM(Sales) AS Total_Sales,
    ROUND(
        SUM(Sales) * 100.0 / (SELECT SUM(Sales) FROM sales WHERE Sales IS NOT NULL),
        2
    ) AS Contribution_Percent
FROM sales
WHERE Sales IS NOT NULL
GROUP BY Region
ORDER BY Total_Sales DESC;


-- =====================================================
-- 3️⃣ REGION RANKING (WINDOW FUNCTIONS)
-- =====================================================
SELECT 
    Region,
    SUM(Sales) AS Total_Sales,
    RANK() OVER (ORDER BY SUM(Sales) DESC) AS Sales_Rank,
    DENSE_RANK() OVER (ORDER BY SUM(Sales) DESC) AS Dense_Rank
FROM sales
WHERE Sales IS NOT NULL
GROUP BY Region;


-- =====================================================
-- 4️⃣ TOP 5 PRODUCTS BY SALES
-- =====================================================
SELECT 
    Product_Name,
    SUM(Sales) AS Total_Sales
FROM sales
WHERE Sales IS NOT NULL
GROUP BY Product_Name
ORDER BY Total_Sales DESC
LIMIT 5;


-- =====================================================
-- 5️⃣ SUB-CATEGORY PROFIT PERFORMANCE
-- =====================================================
SELECT 
    Sub_Category,
    SUM(Profit) AS Total_Profit
FROM sales
WHERE Profit IS NOT NULL
GROUP BY Sub_Category
ORDER BY Total_Profit ASC;


-- =====================================================
-- 6️⃣ CATEGORY PROFITABILITY ANALYSIS
-- =====================================================
SELECT 
    Category,
    SUM(Sales) AS Total_Sales,
    SUM(Profit) AS Total_Profit,
    ROUND(SUM(Profit) * 100.0 / NULLIF(SUM(Sales), 0), 2) AS Profit_Margin_Percent
FROM sales
WHERE Sales IS NOT NULL AND Profit IS NOT NULL
GROUP BY Category;


-- =====================================================
-- 7️⃣ MARKET PERFORMANCE ANALYSIS
-- =====================================================
SELECT 
    Market,
    SUM(Sales) AS Total_Sales
FROM sales
WHERE Sales IS NOT NULL
GROUP BY Market
ORDER BY Total_Sales DESC;


-- =====================================================
-- 8️⃣ LOSS-MAKING PRODUCTS (BUSINESS RISK ANALYSIS)
-- =====================================================
SELECT 
    Product_Name,
    SUM(Sales) AS Total_Sales,
    SUM(Profit) AS Total_Profit
FROM sales
GROUP BY Product_Name
HAVING SUM(Profit) < 0
ORDER BY Total_Profit ASC;


-- =====================================================
-- 9️⃣ HIGH-PERFORMING REGIONS (TOP CONTRIBUTORS)
-- =====================================================
SELECT 
    Region,
    SUM(Sales) AS Total_Sales
FROM sales
GROUP BY Region
HAVING SUM(Sales) > (SELECT AVG(Sales) FROM sales)
ORDER BY Total_Sales DESC;


-- =====================================================
-- 🔟 ADVANCED ANALYSIS USING CTE
-- =====================================================
WITH region_sales AS (
    SELECT 
        Region,
        SUM(Sales) AS Total_Sales,
        SUM(Profit) AS Total_Profit
    FROM sales
    GROUP BY Region
)
SELECT *
FROM region_sales
ORDER BY Total_Sales DESC;


-- =====================================================
-- 1️⃣1️⃣ SALES VS PROFIT BUCKETING (TREND ANALYSIS)
-- =====================================================
SELECT 
    FLOOR(Sales / 100) * 100 AS Sales_Bucket,
    COUNT(*) AS Transaction_Count,
    AVG(Profit) AS Avg_Profit
FROM sales
GROUP BY Sales_Bucket
ORDER BY Sales_Bucket;


-- =====================================================
-- 1️⃣2️⃣ EXECUTIVE SUMMARY (FINAL INSIGHT BLOCK)
-- =====================================================
SELECT 
    COUNT(DISTINCT Region) AS Total_Regions,
    COUNT(DISTINCT Product_Name) AS Total_Products,
    SUM(Sales) AS Total_Revenue,
    SUM(Profit) AS Total_Profit,
    ROUND(AVG(Profit), 2) AS Avg_Profit_Per_Transaction,
    ROUND(MAX(Profit), 2) AS Max_Profit,
    ROUND(MIN(Profit), 2) AS Max_Loss
FROM sales;