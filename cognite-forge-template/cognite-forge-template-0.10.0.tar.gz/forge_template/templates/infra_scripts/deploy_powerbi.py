import fnmatch
import os
import sys

from pbiapi import PowerBIAPIClient
from ruamel.yaml import YAML

CONFIG_FILE_PATH = "config.yaml"
POWERBI_FILES_FOLDER = "powerbi"
POWERBI_DATASET_FOLDER = os.path.join(POWERBI_FILES_FOLDER, "datasets")
POWERBI_REPORTS_FOLDER = os.path.join(POWERBI_FILES_FOLDER, "reports")


def get_display_name(path: str) -> str:
    return os.path.splitext(os.path.basename(path))[0]


with open(CONFIG_FILE_PATH) as f:
    config = YAML(typ="safe").load(f)["powerbi"]

if len(sys.argv) < 2:
    raise RuntimeError("Expected Power BI token to passed as a command line argument.")

else:
    handler = PowerBIAPIClient(config["tenant_id"], config["application_id"], sys.argv[1])
    prod_workspace = config["production"]["name"]

    report_paths = list(
        map(
            lambda p: os.path.join(POWERBI_REPORTS_FOLDER, p),
            fnmatch.filter(os.listdir(POWERBI_REPORTS_FOLDER), "*.pbix"),
        )
    )
    dataset_paths = list(
        map(
            lambda p: os.path.join(POWERBI_DATASET_FOLDER, p),
            fnmatch.filter(os.listdir(POWERBI_DATASET_FOLDER), "*.pbix"),
        )
    )

    print("\nUploading data sets ...")
    for path in dataset_paths:
        display_name = get_display_name(path)
        handler.import_file_into_workspace(prod_workspace, True, path, display_name)
        print(f"Uploaded {path} as {display_name}")
    print("Done uploading data sets")

    print("\nUploading reports ...")
    for path in report_paths:
        display_name = get_display_name(path)
        handler.import_file_into_workspace(prod_workspace, False, path, display_name)
        print(f"Upladed {path} as {display_name}")
        if len(dataset_paths) == 1:
            dataset_name = get_display_name(dataset_paths[0])
            handler.rebind_report_in_workspace(prod_workspace, dataset_name, display_name)
            print(f"Rebound {display_name} to {dataset_name}")
    print("Done uploading reports")

    existing_datasets = set(map(lambda x: x["name"], handler.get_datasets_in_workspace(prod_workspace)))
    existing_reports = set(map(lambda x: x["name"], handler.get_reports_in_workspace(prod_workspace)))
    datasets_to_remove = existing_datasets - set([get_display_name(file) for file in dataset_paths])
    reports_to_remove = existing_reports - set([get_display_name(file) for file in report_paths])

    print("\nDeleting reports that should not be present ...")
    for path in reports_to_remove:
        handler.delete_report(prod_workspace, path)
        print("Deleted", path)
    print("Done deleting reports")

    print("\nDeleting dataset that should not be present ...")
    for path in datasets_to_remove:
        handler.delete_dataset(prod_workspace, path)
        print("Deleted", path)
    print("Done deleting data sets")
