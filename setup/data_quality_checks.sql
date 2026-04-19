-- =====================================================
-- 🔍 SALES DATA QUALITY ASSURANCE LAYER (PRODUCTION GRADE)
-- Author: Vivek Saha
-- Purpose: Full dataset validation before analytics/dashboarding
-- =====================================================

USE sales_analysis;

-- =====================================================
-- 0. BASIC DATA OVERVIEW
-- =====================================================
SELECT COUNT(*) AS Total_Rows FROM sales;


-- =====================================================
-- 1. NULL / EMPTY VALUE CHECK (QUALITY METRICS)
-- =====================================================
SELECT 
    COUNT(*) AS Total_Rows,

    SUM(CASE WHEN Region IS NULL OR TRIM(Region) = '' THEN 1 ELSE 0 END) AS Null_Region,
    ROUND(100 * SUM(CASE WHEN Region IS NULL OR TRIM(Region) = '' THEN 1 ELSE 0 END) / COUNT(*), 2) AS Pct_Null_Region,

    SUM(CASE WHEN Market IS NULL OR TRIM(Market) = '' THEN 1 ELSE 0 END) AS Null_Market,
    ROUND(100 * SUM(CASE WHEN Market IS NULL OR TRIM(Market) = '' THEN 1 ELSE 0 END) / COUNT(*), 2) AS Pct_Null_Market,

    SUM(CASE WHEN Category IS NULL OR TRIM(Category) = '' THEN 1 ELSE 0 END) AS Null_Category,
    ROUND(100 * SUM(CASE WHEN Category IS NULL OR TRIM(Category) = '' THEN 1 ELSE 0 END) / COUNT(*), 2) AS Pct_Null_Category,

    SUM(CASE WHEN `Sub.Category` IS NULL OR TRIM(`Sub.Category`) = '' THEN 1 ELSE 0 END) AS Null_SubCategory,
    ROUND(100 * SUM(CASE WHEN `Sub.Category` IS NULL OR TRIM(`Sub.Category`) = '' THEN 1 ELSE 0 END) / COUNT(*), 2) AS Pct_Null_SubCategory,

    SUM(CASE WHEN `Product.Name` IS NULL OR TRIM(`Product.Name`) = '' THEN 1 ELSE 0 END) AS Null_Product,
    ROUND(100 * SUM(CASE WHEN `Product.Name` IS NULL OR TRIM(`Product.Name`) = '' THEN 1 ELSE 0 END) / COUNT(*), 2) AS Pct_Null_Product,

    SUM(CASE WHEN Sales IS NULL THEN 1 ELSE 0 END) AS Null_Sales,
    SUM(CASE WHEN Profit IS NULL THEN 1 ELSE 0 END) AS Null_Profit,
    SUM(CASE WHEN Quantity IS NULL THEN 1 ELSE 0 END) AS Null_Quantity

FROM sales;


-- =====================================================
-- 2. DUPLICATE RECORD CHECK (PROPER BUSINESS LOGIC)
-- =====================================================
SELECT 
    `Order.ID`,
    `Product.ID`,
    COUNT(*) AS Duplicate_Count
FROM sales
GROUP BY `Order.ID`, `Product.ID`
HAVING COUNT(*) > 1;


-- =====================================================
-- 3. BUSINESS RULE VALIDATION (INVALID RECORDS)
-- =====================================================
SELECT 
    `Order.ID`,
    Sales,
    Profit,
    Quantity
FROM sales
WHERE 
    Sales IS NULL OR Sales <= 0
    OR Quantity IS NULL OR Quantity <= 0
    OR Profit IS NULL;


-- =====================================================
-- 4. DATE CONSISTENCY CHECK
-- =====================================================
SELECT 
    `Order.ID`,
    `Order.Date`,
    `Ship.Date`
FROM sales
WHERE 
    `Order.Date` IS NULL
    OR `Ship.Date` IS NULL
    OR `Ship.Date` < `Order.Date`
    OR `Order.Date` > CURDATE();


-- =====================================================
-- 5. CATEGORY / DIMENSION SANITY CHECK
-- =====================================================
SELECT DISTINCT Region FROM sales;
SELECT DISTINCT Market FROM sales;
SELECT DISTINCT Category FROM sales;
SELECT DISTINCT `Sub.Category` FROM sales;
SELECT DISTINCT `Ship.Mode` FROM sales;


-- =====================================================
-- 6. OUTLIER SUMMARY (RANGE CHECK)
-- =====================================================
SELECT 
    MIN(Sales) AS Min_Sales,
    MAX(Sales) AS Max_Sales,
    ROUND(AVG(Sales), 2) AS Avg_Sales
FROM sales;

SELECT 
    MIN(Profit) AS Min_Profit,
    MAX(Profit) AS Max_Profit,
    ROUND(AVG(Profit), 2) AS Avg_Profit
FROM sales;

SELECT 
    MIN(Quantity) AS Min_Quantity,
    MAX(Quantity) AS Max_Quantity,
    ROUND(AVG(Quantity), 2) AS Avg_Quantity
FROM sales;


-- =====================================================
-- 7. TOP / BOTTOM PERFORMANCE CHECK
-- =====================================================
SELECT 
    `Order.ID`,
    Sales,
    Profit
FROM sales
ORDER BY Sales DESC
LIMIT 10;

SELECT 
    `Order.ID`,
    Sales,
    Profit
FROM sales
WHERE Profit < 0
ORDER BY Profit ASC
LIMIT 10;


-- =====================================================
-- 8. DASHBOARD SUMMARY SNAPSHOT
-- =====================================================
SELECT 
    COUNT(*) AS Total_Records,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    ROUND(AVG(Sales), 2) AS Avg_Sales,
    ROUND(AVG(Profit), 2) AS Avg_Profit,
    ROUND(SUM(`Shipping.Cost`), 2) AS Total_Shipping_Cost
FROM sales;


-- =====================================================
-- 9. ADVANCED CONSISTENCY CHECKS
-- =====================================================

-- Profit cannot exceed Sales (logical validation)
SELECT 
    `Order.ID`,
    Sales,
    Profit
FROM sales
WHERE Profit > Sales;

-- Shipping cost should not exceed Sales
SELECT 
    `Order.ID`,
    Sales,
    `Shipping.Cost`
FROM sales
WHERE `Shipping.Cost` > Sales;

-- Margin sanity check (-100% to +100%)
SELECT 
    `Order.ID`,
    Sales,
    Profit,
    CASE 
        WHEN Sales = 0 THEN NULL
        ELSE Profit / Sales
    END AS Profit_Margin
FROM sales
WHERE Sales > 0
  AND (Profit / Sales < -1 OR Profit / Sales > 1);


-- =====================================================
-- 10. DATA FRESHNESS CHECK
-- =====================================================
SELECT 
    MAX(`Order.Date`) AS Latest_Order_Date,
    DATEDIFF(CURDATE(), MAX(`Order.Date`)) AS Days_Since_Last_Order
FROM sales;


-- =====================================================
-- 11. FINAL DATA QUALITY STATUS (PRODUCTION GRADE ENGINE)
-- =====================================================
SELECT 
    CASE 
        WHEN EXISTS (
            SELECT 1 FROM sales 
            WHERE Sales IS NULL OR Sales <= 0
               OR Quantity IS NULL OR Quantity <= 0
               OR Profit IS NULL
        )
        OR EXISTS (
            SELECT 1
            FROM sales
            GROUP BY `Order.ID`, `Product.ID`
            HAVING COUNT(*) > 1
        )
        OR EXISTS (
            SELECT 1 FROM sales
            WHERE `Ship.Date` < `Order.Date`
        )
        OR EXISTS (
            SELECT 1 FROM sales
            WHERE Profit > Sales
        )
        THEN 'FAIL'
        ELSE 'PASS'
    END AS Data_Quality_Status;


-- =====================================================
-- END OF PRODUCTION DATA QUALITY SCRIPT
-- =====================================================