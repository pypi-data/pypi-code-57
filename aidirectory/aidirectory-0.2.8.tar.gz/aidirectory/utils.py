import os
from aihelper import aiyaml


def write_post_yaml(data):
    new_data = aiyaml.write_directories(data)
    root = data.get("DIRECTORY", os.getcwd())
    project_name = data.get("PROJECT", "<NAME MISSING>")
    project = os.path.join(root, f"Project {project_name}")
    new_data["DIRECTORY"] = project
    write_path = os.path.join(project, "project parameters.yaml")
    parameters = os.path.join(project, "Parameters")
    baseline = os.path.join(parameters, "Baseline")
    new_data["BASELINE DIRECTORY"] = baseline
    return new_data, write_path


def decompress(data_loaded):
    root = data_loaded.get("DIRECTORY", os.getcwd())
    project_name = data_loaded.get("PROJECT", "<NAME MISSING>")
    project = os.path.join(root, f"Project {project_name}")
    isotherms = [iso for iso in (data_loaded.get("ISOTHERMS", []) or []) if iso]
    gradients = [grad for grad in (data_loaded.get("GRADIENTS", []) or []) if grad]
    methods = data_loaded.get("TECHNIQUES")
    topics = [
        f"Topic {topic}" for topic in (data_loaded.get("TOPICS", []) or []) if topic
    ]
    parameters = os.path.join(project, "Parameters")
    baseline = os.path.join(parameters, "Baseline")
    tg_methods = os.path.join(parameters, "Method")
    return (
        project,
        topics,
        methods,
        isotherms,
        gradients,
        parameters,
        baseline,
        tg_methods,
    )


def isograder(isograd, temperature, methods):
    for temp in temperature:
        iso_path = os.path.join(isograd, str(temp))
        try:
            os.mkdir(iso_path)
        except OSError:
            pass
        for method in methods:
            iso_method_path = os.path.join(iso_path, method)
            try:
                os.mkdir(iso_method_path)
            except OSError:
                pass
