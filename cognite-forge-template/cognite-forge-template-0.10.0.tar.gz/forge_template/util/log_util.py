import logging
from typing import Any, Dict, Iterable, List


def print_message(msg: str) -> None:
    logging.info(msg)


def print_entity_exists(entity_name: str = "", entity_type: str = "") -> None:
    logging.info(f"Databricks {entity_type} with name {entity_name} already exists.")


def print_success_created(entity_name: Any, entity_type: str = "") -> None:
    logging.info(f"Successfully created {entity_name} [{entity_type}].")


def print_success_deleted(entity_name: Any, entity_type: str = "") -> None:
    logging.info(f"Successfully deleted {entity_name} [{entity_type}].")


def print_success_removed(
    sub_entity_name: str = "", entity_name: str = "", sub_entity_type: str = "", entity_type: str = ""
) -> None:
    logging.info(f"Successfully removed {sub_entity_name} [{sub_entity_type}] from {entity_name} [{entity_type}].")


def print_success_added(parent_entity_name="", parent_entity_type="", entity_name="", entity_type="") -> None:
    logging.info(f"Successfully added {entity_name} [{entity_type}] to {parent_entity_name} " f"[{parent_entity_type}]")


def print_rollback(entity_type: str) -> None:
    logging.info(f"Rolling back all {entity_type} that have been created")


def print_resources_to_update(resource_dict: Dict, resource_type_to_add: str, main_resource_type: str) -> None:
    for resource_name, resource_list in resource_dict.items():
        if resource_list:
            print_resource_update(resource_list, resource_name, resource_type_to_add, main_resource_type)


def print_remotes_to_rename(rename_list: List) -> None:
    for (original_name, new_name) in rename_list:
        logging.info(f"Remote: {original_name} will be renamed to {new_name}")


def print_files_to_be_added() -> None:
    logging.info("All files in this repository except those in .gitignore will be added to the new remote")


def print_resource_update(
    resource_list: List, main_resource: str, resource_type_to_add: str, main_resource_type: str
) -> None:
    logging.info(
        f"{main_resource_type}: "
        + ", ".join([f"{resource} [{resource_type_to_add}]" for resource in resource_list])
        + f" will be added to {main_resource} [{main_resource_type}]"
    )


def print_resource_to_add(resource_list: Iterable[Any], resource_type: str) -> None:
    if resource_list:
        for resource in resource_list:
            logging.info(f"{resource_type}: {resource} will be added.")


def print_resource_already_exists(resource_name: Any, resource_type: str, override: bool = False) -> None:
    logging.info(
        f"Resource {resource_name} [{resource_type}] already exists. It will "
        + ("" if override else "not")
        + " be re-created."
    )
