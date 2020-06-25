# Databricks notebook source
# MAGIC %md # Setup development environment
# MAGIC
# MAGIC ### Prerequisites
# MAGIC Python 3.7+
# MAGIC
# MAGIC ### About this notebook
# MAGIC This notebook initializes the development environment. This notebook should be run in the top of all other notebooks. It assumes that a Databricks widget called _notebook_path_ exists. The notebook will to the following for you:
# MAGIC - **Cmd 2**: Install three python libraries; ruamel.yaml (for reading the .yaml config file), pbiapi (Python SDK for Power BI), congite-sdk.
# MAGIC - **Cmd 3**: Figure out if this notebook is in the development or production environment. If running this notebook from a job, the parameter 'stage' needs to be set.
# MAGIC - **Cmd 4**: Read the config file and store the data in the file as a Python dictionary in a variable named _config_
# MAGIC - **Cmd 5**: Initializes a Cognite Python SDK client and stores it in the variable named _client_
# MAGIC
# MAGIC To use in other notebooks, simply include a cell with the following code: `%run ../setup/setup-environment.py`. Please note that the file path is relative to the notebook you run it from.

# COMMAND ----------

# Install necessary Python libraries on the cluster
# ruamel.yaml is used to read the config file
# pbiapi is used for interacting with PowerBI (triggering a dataset refresh)
dbutils.library.installPyPI("ruamel.yaml")
dbutils.library.installPyPI("pbiapi", version="0.1.4")
dbutils.library.installPyPI("cognite-sdk", version="1.5.0")

# COMMAND ----------

# Which stage (development or production) is this notebook?
try:
  dbutils.notebook.entry_point.getDbutils().notebook().getContext().currentRunId().get()
  stage = dbutils.widgets.get("stage")
except Exception:
  path = dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()
  if "/prod/" in path:
    stage = "production"
  else:
    stage = "development"

# COMMAND ----------

from cognite.client import CogniteClient
from ruamel.yaml import YAML

if stage not in ["production", "development"]:
  raise InputError(f"Illegal stage, {stage}")

# Read config file
yaml_config_path = "YAML_CONFIG_PATH_PLACEHOLDER"
with open(yaml_config_path, encoding="utf-8") as f:
    full_config = YAML(typ="safe").load(f)

if "powerbi" in full_config:
    powerbi_config = full_config["powerbi"]  # This config is only needed if working with PowerBI
db_config = full_config["databricks"]
config = db_config[stage]
config["project_description"] = db_config["project_description"]
config["group_name"] = config["group"]["name"]
config["api_key"] = dbutils.secrets.get(
    config["scope"]["name"], "cdf_api_key"
)  # Assumes that the cdf-read-key exists in the scope
print("Done reading config. Available as a Python variable named 'config' (a dictionary)")


# COMMAND ----------

api_key = config["api_key"]
project = config["cdf_project_name"]
client_name = f"forge-{config['cdf_project_name']}"
client = CogniteClient(api_key=api_key, project=project, client_name=client_name)
print("Done creating Cognite Python SDK client. Available as a Python variables named 'client'")
