from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
PACKAGE_NAME = "forge_template"

CODE_DIR = ROOT_DIR / PACKAGE_NAME
TEMPLATE_DIR = CODE_DIR / "templates"

# Schema paths
SCHEMA_DIR = CODE_DIR / "schema"
YAML_CONFIG_SCHEMA_PATH = SCHEMA_DIR / "config_schema.yaml"
YAML_SECRETS_SCHEMA_PATH = SCHEMA_DIR / "secrets_schema.yaml"

# Config paths
YAML_CONFIG_PATH = Path("config.yaml")
YAML_SECRETS_PATH = Path("secrets.yaml")

# Databricks paths
DATABRICKS_TEMPLATE_DIR = TEMPLATE_DIR / "databricks"
DATABRICKS_OUTPUT_DIR = Path("databricks")

# Power BI paths
POWERBI_TEMPLATE_DIR = TEMPLATE_DIR / "powerbi"
POWERBI_OUTPUT_DIR = Path("powerbi")
POWERBI_BASE_DATASET_PATH = POWERBI_OUTPUT_DIR / "datasets" / "base_dataset.pbix"
POWERBI_BASE_REPORT_PATH = POWERBI_OUTPUT_DIR / "reports" / "base_report.pbix"

# SA Replication paths
PROJECT_BUCKET = "sa-sandbox-training"
JOB_BUCKET = "sa-sandbox-training"
SCHEDULE_BUCKET = "europe-west1-composer-ccb9555e-bucket"
PROJECT_FILES_PATH = "beam-component/config/"
JOB_FILES_PATH = "beam-component/config/replicate/"
SCHEDULE_FILES_PATH = "dags/"

# Github Actions paths
SCRIPT_TEMPLATE_DIR = TEMPLATE_DIR / "infra_scripts"
POWERBI_SCRIPT_PATH = SCRIPT_TEMPLATE_DIR / "deploy_powerbi.py"
DATABRICKS_SCRIPT_TEMPLATE_PATH = SCRIPT_TEMPLATE_DIR / "deploy_databricks.py"
SCRIPT_OUTPUT_DIR = Path("pipeline_scripts")

WORKFLOW_TEMPLATE_DIR = TEMPLATE_DIR / "github_workflows"
POWERBI_WORKFLOW_TEMPLATE_PATH = WORKFLOW_TEMPLATE_DIR / "deploy_powerbi.yaml"
DATABRICKS_WORKFLOW_TEMPLATE_PATH = WORKFLOW_TEMPLATE_DIR / "deploy_databricks.yaml"
WORKFLOW_OUTPUT_DIR = Path(".github") / "workflows"
