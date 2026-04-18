-- =====================================================
-- 📦 SALES ANALYTICS PROJECT - DATA ENGINEERING LAYER
-- Author: Vivek Saha
-- Purpose: Schema Documentation & Data Validation
-- Note: Data imported via Wizard to handle encoding (cp1252)
-- =====================================================

-- 1. DATABASE CONTEXT
CREATE DATABASE IF NOT EXISTS sales_analysis;
USE sales_analysis;

-- 2. SCHEMA DEFINITION (RECORD ONLY)
-- This matches the columns created by the Import Wizard.
-- We keep this here so anyone reading your code knows the structure.
/*
CREATE TABLE IF NOT EXISTS sales (
    `Category` TEXT,
    `City` TEXT,
    `Country` TEXT,
    `Customer.ID` TEXT,
    `Customer.Name` TEXT,
    `Discount` INT,
    `Market` TEXT,
    `Order.Date` TEXT,
    `Order.ID` TEXT,
    `Order.Priority` TEXT,
    `Product.ID` TEXT,
    `Product.Name` TEXT,
    `Profit` DOUBLE,
    `Quantity` INT,
    `Region` TEXT,
    `Sales` DOUBLE,
    `Ship.Date` TEXT,
    `Ship.Mode` TEXT,
    `Shipping.Cost` DOUBLE,
    `State` TEXT,
    `Sub.Category` TEXT,
    `Year` INT,
    `Revenue` DOUBLE,
    `Month` TEXT,
    `Profit.Margin` DOUBLE,
    `Order.Value` DOUBLE,
    `Year_Month` TEXT
);
*/

-- 3. FINAL DATA VALIDATION SUITE
-- Run these to confirm your database is ready for the Dashboard.

-- A) Verify Total Row Count (Target: 9,998)
SELECT COUNT(*) AS total_rows_loaded 
FROM sales;

-- B) Verify Numerical Accuracy
SELECT 
    ROUND(SUM(`Sales`), 2) AS total_revenue,
    ROUND(AVG(`Profit.Margin`), 4) AS average_margin,
    MAX(`Quantity`) AS max_single_order_qty
FROM sales;

-- C) Data Alignment Sample
-- This confirms the 'dots' in column names are working correctly.
SELECT 
    `Order.ID`, 
    `Customer.Name`, 
    `Category`, 
    `Sales`, 
    `Year_Month` 
FROM sales 
LIMIT 10;