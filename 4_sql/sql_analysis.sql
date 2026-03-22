-- Top performing region
SELECT Region, SUM(Sales) AS Total_Sales
FROM sales
GROUP BY Region
ORDER BY Total_Sales DESC;

-- Profit by category
SELECT Category, SUM(Profit) AS Total_Profit
FROM sales
GROUP BY Category
ORDER BY Total_Profit DESC;

-- Loss making products
SELECT Product_Name, Sales, Profit
FROM sales
WHERE Profit < 0
ORDER BY Profit ASC;