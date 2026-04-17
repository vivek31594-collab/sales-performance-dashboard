-- ===================================
-- 📊 SALES ANALYSIS SQL (FINAL)
-- ===================================

-- 1️⃣ KPI SUMMARY
SELECT 
    SUM(Sales) AS Total_Sales,
    SUM(Profit) AS Total_Profit,
    ROUND(SUM(Profit) * 100.0 / SUM(Sales), 2) AS Profit_Margin_Percent
FROM sales;


-- ===================================
-- 2️⃣ REGION PERFORMANCE (WITH %)
-- ===================================
SELECT 
    Region,
    SUM(Sales) AS Total_Sales,
    ROUND(SUM(Sales) * 100.0 / SUM(SUM(Sales)) OVER(), 2) AS Contribution_Percent
FROM sales
GROUP BY Region
ORDER BY Total_Sales DESC;


-- ===================================
-- 3️⃣ REGION RANKING (WINDOW FUNCTIONS)
-- ===================================
SELECT 
    Region,
    SUM(Sales) AS Total_Sales,
    RANK() OVER (ORDER BY SUM(Sales) DESC) AS Rank_Position,
    ROW_NUMBER() OVER (ORDER BY SUM(Sales) DESC) AS Row_Number_Position
FROM sales
GROUP BY Region;


-- ===================================
-- 4️⃣ TOP 5 PRODUCTS BY SALES
-- ===================================
SELECT 
    Product_Name,
    SUM(Sales) AS Total_Sales
FROM sales
GROUP BY Product_Name
ORDER BY Total_Sales DESC
LIMIT 5;


-- ===================================
-- 5️⃣ SUB-CATEGORY PROFIT ANALYSIS
-- ===================================
SELECT 
    Sub_Category,
    SUM(Profit) AS Total_Profit
FROM sales
GROUP BY Sub_Category
ORDER BY Total_Profit ASC;


-- ===================================
-- 6️⃣ CATEGORY PROFIT MARGIN
-- ===================================
SELECT 
    Category,
    SUM(Sales) AS Total_Sales,
    SUM(Profit) AS Total_Profit,
    ROUND(SUM(Profit) * 100.0 / SUM(Sales), 2) AS Profit_Margin_Percent
FROM sales
GROUP BY Category;


-- ===================================
-- 7️⃣ MARKET PERFORMANCE
-- ===================================
SELECT 
    Market,
    SUM(Sales) AS Total_Sales
FROM sales
GROUP BY Market
ORDER BY Total_Sales DESC;


-- ===================================
-- 8️⃣ LOSS-MAKING PRODUCTS
-- ===================================
SELECT 
    Product_Name,
    Sales,
    Profit
FROM sales
WHERE Profit < 0
ORDER BY Profit ASC;


-- ===================================
-- 9️⃣ HIGH-PERFORMING REGIONS (HAVING)
-- ===================================
SELECT 
    Region,
    SUM(Sales) AS Total_Sales
FROM sales
GROUP BY Region
HAVING SUM(Sales) > 100000
ORDER BY Total_Sales DESC;


-- ===================================
-- 🔟 CTE EXAMPLE (ADVANCED SQL)
-- ===================================
WITH region_sales AS (
    SELECT 
        Region, 
        SUM(Sales) AS Total_Sales
    FROM sales
    GROUP BY Region
)

SELECT *
FROM region_sales
ORDER BY Total_Sales DESC;


-- ===================================
-- 1️⃣1️⃣ SALES VS PROFIT BUCKETING
-- ===================================
SELECT 
    ROUND(Sales, -2) AS Sales_Bucket,
    AVG(Profit) AS Avg_Profit
FROM sales
GROUP BY Sales_Bucket
ORDER BY Sales_Bucket;