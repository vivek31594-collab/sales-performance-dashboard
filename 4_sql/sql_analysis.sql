-- =====================================================
-- 📊 SALES ANALYTICS DASHBOARD PROJECT (PROFESSIONAL GRADE - FINAL)
-- Author: Vivek Saha
-- Purpose: End-to-end business performance analysis for Dashboarding
-- Compatibility: MySQL 5.7+ (No window function dependency)
-- =====================================================

USE sales_analysis;

-- =====================================================
-- 0️⃣ DATA INTEGRITY CHECK
-- =====================================================
SELECT 
    COUNT(*) AS Total_Rows,
    COUNT(DISTINCT Sub_Category) AS SubCat_Count
FROM sales;


-- =====================================================
-- 1️⃣ KPI SUMMARY (EXECUTIVE OVERVIEW)
-- =====================================================
SELECT 
    COUNT(*) AS Total_Transactions,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    ROUND(SUM(Profit) * 100.0 / NULLIF(SUM(Sales), 0), 2) AS Profit_Margin_Percent,
    ROUND(AVG(Profit), 2) AS Avg_Profit_Per_Transaction
FROM sales
WHERE Sales IS NOT NULL AND Profit IS NOT NULL;


-- =====================================================
-- 2️⃣ REGION PERFORMANCE + CONTRIBUTION %
-- =====================================================
SELECT 
    Region,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(
        SUM(Sales) * 100.0 / (SELECT SUM(Sales) FROM sales),
        2
    ) AS Contribution_Percent
FROM sales
GROUP BY Region
ORDER BY Total_Sales DESC;


-- =====================================================
-- 3️⃣ REGION RANKING (COMPATIBLE VERSION)
-- =====================================================
SET @rank := 0;

SELECT 
    Region,
    Total_Sales,
    @rank := @rank + 1 AS Sales_Rank
FROM (
    SELECT 
        Region,
        ROUND(SUM(Sales), 2) AS Total_Sales
    FROM sales
    GROUP BY Region
    ORDER BY Total_Sales DESC
) ranked_regions;


-- =====================================================
-- 4️⃣ TOP 10 PRODUCTS BY SALES
-- =====================================================
SELECT 
    Product_Name,
    Category,
    ROUND(SUM(Sales), 2) AS Total_Sales
FROM sales
GROUP BY Product_Name, Category
ORDER BY Total_Sales DESC
LIMIT 10;


-- =====================================================
-- 5️⃣ SUB-CATEGORY PROFIT PERFORMANCE
-- =====================================================
SELECT 
    Sub_Category,
    ROUND(SUM(Profit), 2) AS Total_Profit
FROM sales
GROUP BY Sub_Category
ORDER BY Total_Profit DESC;


-- =====================================================
-- 6️⃣ CATEGORY PROFITABILITY ANALYSIS
-- =====================================================
SELECT 
    Category,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    ROUND(SUM(Profit) * 100.0 / NULLIF(SUM(Sales), 0), 2) AS Profit_Margin_Percent
FROM sales
GROUP BY Category
ORDER BY Profit_Margin_Percent DESC;


-- =====================================================
-- 7️⃣ MARKET PERFORMANCE ANALYSIS
-- =====================================================
SELECT 
    Market,
    ROUND(SUM(Sales), 2) AS Total_Sales
FROM sales
GROUP BY Market
ORDER BY Total_Sales DESC;


-- =====================================================
-- 8️⃣ LOSS-MAKING PRODUCTS (BUSINESS RISK ANALYSIS)
-- =====================================================
SELECT 
    Product_Name,
    Category,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit
FROM sales
GROUP BY Product_Name, Category
HAVING SUM(Profit) < 0
ORDER BY Total_Profit ASC;


-- =====================================================
-- 9️⃣ ABOVE-AVERAGE SALES REGIONS
-- =====================================================
SELECT 
    Region,
    ROUND(SUM(Sales), 2) AS Total_Sales
FROM sales
GROUP BY Region
HAVING SUM(Sales) > (
    SELECT AVG(Sales_Per_Region) 
    FROM (
        SELECT SUM(Sales) AS Sales_Per_Region 
        FROM sales 
        GROUP BY Region
    ) sub
)
ORDER BY Total_Sales DESC;


-- =====================================================
-- 🔟 ADVANCED ANALYSIS (REGIONAL EFFICIENCY - FIXED)
-- =====================================================
SELECT 
    Region,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    COUNT(*) AS Order_Count,
    ROUND(SUM(Profit) / NULLIF(COUNT(*), 0), 2) AS Profit_Per_Order
FROM sales
GROUP BY Region
ORDER BY Total_Sales DESC;


-- =====================================================
-- 1️⃣1️⃣ SALES DISTRIBUTION (BUCKETING)
-- =====================================================
SELECT 
    FLOOR(Sales / 500) * 500 AS Sales_Bucket,
    COUNT(*) AS Transaction_Count
FROM sales
GROUP BY Sales_Bucket
ORDER BY Sales_Bucket;


-- =====================================================
-- 1️⃣2️⃣ FINAL EXECUTIVE SUMMARY
-- =====================================================
SELECT 
    COUNT(DISTINCT Region) AS Total_Regions,
    COUNT(DISTINCT Category) AS Total_Categories,
    COUNT(DISTINCT Product_Name) AS Total_Unique_Products,
    ROUND(SUM(Sales), 2) AS Total_Revenue,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    ROUND(AVG(Profit), 2) AS Avg_Profit_Per_Txn
FROM sales;