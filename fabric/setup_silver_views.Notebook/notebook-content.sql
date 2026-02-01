-- Fabric notebook source

-- METADATA ********************

-- META {
-- META   "kernel_info": {
-- META     "name": "sqldatawarehouse"
-- META   },
-- META   "dependencies": {
-- META     "lakehouse": {
-- META       "default_lakehouse": "265f8d08-6bfb-4020-818f-bd67d415216f",
-- META       "default_lakehouse_name": "lh_silver",
-- META       "default_lakehouse_workspace_id": "f6403c30-0561-47b4-9f65-bc88f7a1986c",
-- META       "known_lakehouses": [
-- META         {
-- META           "id": "265f8d08-6bfb-4020-818f-bd67d415216f"
-- META         }
-- META       ]
-- META     },
-- META     "warehouse": {
-- META       "default_warehouse": "7f22aec0-eb8a-481b-842b-17070549ecb0",
-- META       "known_warehouses": [
-- META         {
-- META           "id": "7f22aec0-eb8a-481b-842b-17070549ecb0",
-- META           "type": "Lakewarehouse"
-- META         }
-- META       ]
-- META     }
-- META   }
-- META }

-- CELL ********************

USE lh_silver;
GO

-- METADATA ********************

-- META {
-- META   "language": "sql",
-- META   "language_group": "sqldatawarehouse"
-- META }

-- CELL ********************

CREATE OR ALTER VIEW [dbo].[vw_invalid_customers]
AS
  SELECT 
    Customer,
    CASE Category
      WHEN 'Novelty Shop' THEN 1
      ELSE 0 
    END as CategoryType,
    YEAR(ValidTo) - YEAR(getdate()) as ValidYears
  FROM customers
  WHERE TRY_CAST(PostalCode AS INT) is NULL; 


-- METADATA ********************

-- META {
-- META   "language": "sql",
-- META   "language_group": "sqldatawarehouse"
-- META }

-- CELL ********************

CREATE OR ALTER VIEW [dbo].[vw_customers]
AS
  SELECT 
    Customer,
    CASE Category
      WHEN 'Novelty Shop' THEN 1
      ELSE 0 
    END as CategoryType,
    YEAR(ValidTo) - YEAR(getdate()) as ValidYears
  FROM customers
  WHERE TRY_CAST(PostalCode AS INT) > 7000; 

-- METADATA ********************

-- META {
-- META   "language": "sql",
-- META   "language_group": "sqldatawarehouse"
-- META }

-- CELL ********************

SELECT TOP 10 * FROM vw_customers

-- METADATA ********************

-- META {
-- META   "language": "sql",
-- META   "language_group": "sqldatawarehouse"
-- META }
