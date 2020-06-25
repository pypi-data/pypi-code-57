# Databricks notebook source
# MAGIC %md # Setup base model (database and views)
# MAGIC 
# MAGIC ### Prerequisites
# MAGIC Python 3.7+
# MAGIC 
# MAGIC ### About this notebook
# MAGIC This notebook create a database with views. There is one view for each of the following CDF resource types: assets, events, datapoints, timeseries, files, 3dmodels.
# MAGIC 
# MAGIC - **Cmd 2**: The setup-environment notebook is run to setup the development environment (installing commonly used libraries and reading a configuration file). The parameters from the configuration file is available as a Python dictionary named _config_.

# COMMAND ----------

# MAGIC %run ../setup/setup-environment.py

# COMMAND ----------

# Will create tables and database if True. If False the database will be deleted (if it exists)
CREATE = True 

# COMMAND ----------

# Create database:
if CREATE:
  spark.sql(
      """
      CREATE DATABASE IF NOT EXISTS {database_name} 
      COMMENT '{project_description}'
      """.format(
          **config
      )
  )

# COMMAND ----------

# Grant permissions:
if CREATE:
  spark.sql("GRANT ALL PRIVILEGES ON DATABASE {database_name} TO `{group_name}`".format(**config))

# COMMAND ----------

# Create table with assets
if CREATE:
  for cdf_type in ["assets", "events"]:
    spark.sql("DROP TABLE IF EXISTS {database_name}.api_{cdf_type}".format(cdf_type=cdf_type, **config))
    spark.sql(
        """
    CREATE TABLE IF NOT EXISTS {database_name}.api_{cdf_type} USING cognite.spark.v1
    OPTIONS (type '{cdf_type}',
             apiKey '{api_key}',
             partitions '80')
    COMMENT 'View of {cdf_type} in CDF from base model'
    """.format(
            cdf_type=cdf_type, **config
        )
    )

# COMMAND ----------

if CREATE:
  for cdf_type in ["datapoints", "timeseries", "files", "3dmodels"]:
    spark.sql("DROP TABLE IF EXISTS {database_name}.api_{cdf_type}".format(cdf_type=cdf_type, **config))
    spark.sql(
        """
    CREATE TABLE IF NOT EXISTS {database_name}.api_{cdf_type} USING cognite.spark.v1
    OPTIONS (type '{cdf_type}',
             apiKey '{api_key}')
    COMMENT 'View of {cdf_type} in CDF from base model'
    """.format(
            cdf_type=cdf_type, **config
        )
    )

# COMMAND ----------

if not CREATE:
  spark.sql("DROP DATABASE IF EXISTS {database_name} CASCADE".format(**config))

# COMMAND ----------

# Display database table metadata
if CREATE:
  display(spark.catalog.listTables(config["database_name"]))

# COMMAND ----------

# Display schemas for database tables
if CREATE:
  for t in ["api_assets", "api_datapoints", "api_events", "api_timeseries", "api_files", "api_3dmodels"]:
      print(">>", t)
      spark.table("%s.%s" % (config["database_name"], t)).printSchema()
