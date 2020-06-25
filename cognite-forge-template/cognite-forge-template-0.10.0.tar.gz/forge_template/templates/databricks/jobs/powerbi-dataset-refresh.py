# Databricks notebook source
# MAGIC %md
# MAGIC # Power BI dataset refresh
# MAGIC In order for the dataset refresh to work a PowerBI service principal token needs to be present in the scope as _powerbi-key_.
# MAGIC Furthermore, for the refresh to work, the correct server url, database name and databricks credentials needs to be set on the Power BI side. This can be done by following these steps:
# MAGIC 1. Log into Power BI
# MAGIC 2. Navigate to your workspace
# MAGIC 3. Go to Datasets
# MAGIC 4. In the Action column click the three dots next to the base_dataset.
# MAGIC 5. Choose settings
# MAGIC 6. Under Datasource Credentials and Parameters fill in the necessary information.

# COMMAND ----------

# MAGIC %run ../setup/setup-environment.py

# COMMAND ----------

import requests
# PowerBI: Trigger a dataset refresh
from pbiapi import PowerBIAPIClient

if not powerbi_config:
    print(
        "Power BI not configured in the config.yaml file. Please overwrite the file manually with a version containing Power BI configuration, or use the forge-template cli to do it."
    )
else:
    tenant_id = powerbi_config["tenant_id"]
    client_id = powerbi_config["application_id"]
    client_secret = dbutils.secrets.get(config["scope"]["name"], "powerbi-key")
    workspace_name = powerbi_config[stage]["name"]

    client = PowerBIAPIClient(tenant_id=tenant_id, client_id=client_id, client_secret=client_secret)
    datasets = client.get_datasets_in_workspace(workspace_name)
    for dataset in datasets:
        client.refresh_dataset_by_id(workspace_name, dataset["id"])
