import os
import yaml

from alfa_cli.config import algorithm

ARGUMENTS = algorithm.initialization.specification.arguments

def generate_files(specification):
    main_folder = _create_main_folder(specification)
    for function in specification["functions"]:
        _generate_function_files(main_folder, function)
    _generate_configuration_file(main_folder, specification)

def _create_main_folder(specification):
    algorithm_folder_name = specification["name"].replace(' ', '-').lower()
    cwd_name = os.path.basename(os.getcwd())
    if algorithm_folder_name == cwd_name:
        return "."

    os.mkdir(algorithm_folder_name)
    return os.path.join(".", algorithm_folder_name)

def _generate_function_files(main_folder, function):
    for function_name, function_spec in function.items():
        function_folder = os.path.join(main_folder, function_name)
        os.mkdir(function_folder)

        handler = function_spec["function"]["handler"]
        handler_filename, handler_function = handler.split(".")
        runtime = function_spec["provider"]["runtime"]
        function_arguments = _generate_function_arguments(function_name, runtime)
        if runtime == "python":
            handler_filename += ".py"
            with open(os.path.join(function_folder, handler_filename), "w") as handler_file:
                handler_file.write(f"def {handler_function}({function_arguments}):\n    # define logic here")
            with open(os.path.join(function_folder, 'requirements.txt'), "w") as req_file:
                pass
        elif runtime == "node":
            handler_filename += ".js"
            with open(os.path.join(function_folder, handler_filename), "w") as handler_file:
                handler_file.write(f"exports.{handler_function} = function({function_arguments}) {{\n    // define logic here\n}};")
            with open(os.path.join(function_folder, 'package.json'), "w") as req_file:
                req_file.write(f'{{\n  "name": "{function_name}",\n  "version": "1.0.0",\n  "dependencies": {{\n  }}\n}}')

def _generate_function_arguments(function_name, runtime):
    if not ARGUMENTS[function_name]:
        return ''

    function_arguments = ''
    for i, argument in enumerate(ARGUMENTS[function_name]):
        function_arguments += argument.key
        runtime_default = argument.get(f"default_{runtime}")
        space = "" if runtime == "python" else " "
        if runtime_default:
            function_arguments += f"{space}={space}{runtime_default}"
        elif argument.default:
            function_arguments += f"{space}={space}{argument.default}"
        if i < len(ARGUMENTS[function_name]) - 1:
            function_arguments += ", "
    return function_arguments

def _generate_configuration_file(main_folder, specification):
    with open(os.path.join(main_folder, algorithm.defaults.specification.path), "w") as output:
        specification.pop("name", None)
        functions = {"functions": specification.pop("functions")}

        output.writelines(yaml.dump(specification, sort_keys=False))
        output.write("\n")
        output.writelines(yaml.dump(functions, sort_keys=False))
