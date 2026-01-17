# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "d4c22bc5-cd66-4861-97b9-cbbec683c7f3",
# META       "default_lakehouse_name": "lh_bronze",
# META       "default_lakehouse_workspace_id": "f6403c30-0561-47b4-9f65-bc88f7a1986c",
# META       "known_lakehouses": [
# META         {
# META           "id": "d4c22bc5-cd66-4861-97b9-cbbec683c7f3"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

import sempy.fabric as fabric

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Helper functions for fabric resources

def get_silver_lh():
    return mssparkutils.lakehouse.get("lh_silver")

def setup_workspace_id():
    return fabric.get_workspace_id()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

def filter_customers(source_df):
    return source_df.filter("category != 'N/A'")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

def load_customers():
    df = spark.sql("SELECT * FROM lh_bronze.customers LIMIT 1000")
    display(filter_customers(df))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

if __name__ == "__main__":
    load_customers()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
