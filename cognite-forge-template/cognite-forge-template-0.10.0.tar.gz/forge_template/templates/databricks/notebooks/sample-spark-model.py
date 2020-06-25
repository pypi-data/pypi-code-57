# Databricks notebook source
# MAGIC %md # Spark SQL sample
# MAGIC
# MAGIC ### About this notebook
# MAGIC This notebook create very simple model using Spark SQL. It creates two views, one for timeseries and one for datapoints associated with those time series

# COMMAND ----------

# MAGIC %run ../setup/setup-environment.py

# COMMAND ----------

# Creating a sample table with timeseries
ts = spark.sql(
    """    
  CREATE OR REPLACE VIEW {database_name}.timeseries
  COMMENT 'Timeseries used for base Power BI model' AS 
  SELECT 
    name,
    id,
    unit
  FROM {database_name}.api_timeseries
  LIMIT 10
""".format(
        **config
    )
)

# COMMAND ----------

# Select ids of all timeseries related to pumps
ts_ids = ",".join(spark.sql("SELECT id FROM {database_name}.timeseries".format(**config)).toPandas()["id"].astype(str))

# COMMAND ----------

# Creating a sample table with datapoints
dp = spark.sql(
    """
  CREATE OR REPLACE VIEW {database_name}.datapoints AS
  SELECT 
    id,
    timestamp,
    value
  FROM
    {database_name}.api_datapoints
  WHERE
    timestamp > TIMESTAMP(ADD_MONTHS(NOW(),-36)) AND
    timestamp < TIMESTAMP(DATE_ADD(NOW(),1)) AND
    aggregation = 'average' AND
    granularity = '1d' AND
    id in ({ts_ids})
  """.format(
        **config, ts_ids=ts_ids
    )
)
