import graafilohi
import os
import json
import sys
import matplotlib.pyplot as plt
import networkx as nx
import subprocess
import locale

from helpers import read_selection

GRAPH_DESCRIPTION_FILE = ".git-ws.graphops"
SAVE_FILE_PREFIX = "git-ws.graphops"

PACKAGE_JSON="package.json"
NODEJS_TYPE="nodejs"

class OperationExecutionError(Exception):
    pass


def run_operation_script(script_file_absolute_path, env=[]):
    if script_file_absolute_path is None:
        return None

    if not os.path.isfile(script_file_absolute_path) or not os.access(script_file_absolute_path, os.X_OK):
        return None

    env_dict = {}
    for item in env:
        key, value = item.split("=")
        env_dict[key] = value

    script_directory = os.path.dirname(os.path.realpath(script_file_absolute_path))

    def script_function(*args, **kwargs):
        process = subprocess.Popen(f"{script_file_absolute_path}",
                                   shell=True, stdout=subprocess.PIPE,
                                   env={**os.environ, **env_dict},
                                   stderr=subprocess.STDOUT, cwd=script_directory)
        encoding = locale.getpreferredencoding()
        while True:
            output = process.stdout.readline()
            if process.poll() is not None:
                break
            if output:
                print(output.strip().decode(encoding))
        retval = process.poll()

        if retval > 0:
            raise OperationExecutionError(f"Script execution failed: {script_file_absolute_path}")

    script_name = os.path.basename(os.path.realpath(script_file_absolute_path))
    script_function.__name__ = f"{script_name}-function"
    return script_function


def run_nodejs_script(script, cwd, env=[]):
    env_dict = {}
    for item in env:
        key, value = item.split("=")
        env_dict[key] = value

    def nodejs_script_function(*args, **kwargs):
        process = subprocess.Popen(f"{script}",
                                   shell=True, stdout=subprocess.PIPE,
                                   env={**os.environ, **env_dict},
                                   stderr=subprocess.STDOUT, cwd=cwd)
        encoding = locale.getpreferredencoding()
        while True:
            output = process.stdout.readline()
            if process.poll() is not None:
                break
            if output:
                print(output.strip().decode(encoding))
        retval = process.poll()

        if retval > 0:
            raise OperationExecutionError(f"Script execution failed: {script} in {cwd}")

    nodejs_script_function.__name__ = f"{script}-function"
    return nodejs_script_function

class Graphops:
    def __init__(self, ws, env=[]):
        operations_by_file = {}
        directories = [file for file in os.listdir(ws) if os.path.isdir(os.path.join(ws, file))]
        for directory in directories:
            try:
                with open(os.path.join(ws, directory, GRAPH_DESCRIPTION_FILE)) as jsonfile:
                    data = json.load(jsonfile)
                operations_by_file[directory] = data
            except FileNotFoundError:
                pass
            except json.decoder.JSONDecodeError as e:
                print("Error reading json: ", e)
                sys.exit(1)

        for directory in directories:
            try:
                with open(os.path.join(ws, directory, PACKAGE_JSON)) as pkg_json:
                    data = json.load(pkg_json)
                node_commands = { f"npm-{c}": {"script": f"npm run {c}", "type": NODEJS_TYPE} for c in data.get("scripts", {}).keys() }
                operations_by_file[directory] = {**operations_by_file[directory], **node_commands}
            except FileNotFoundError:
                pass
            except json.decoder.JSONDecodeError as e:
                print("Error reading json: ", e)
                sys.exit(1)
        import pprint
        pp = pprint.PrettyPrinter(indent=4).pprint
        pp(operations_by_file)

        files_per_operation = {}

        for file, operations in operations_by_file.items():
            for op, content in operations.items():
                if op not in files_per_operation:
                    files_per_operation[op] = {}

                files_per_operation[op][file] = content

        graphs = {}
        ws_realpath = os.path.realpath(ws)

        for op, content in files_per_operation.items():
            graphs[op] = graafilohi.ExecutableDirectedMultiGraph()
            nodes = [file for file in content.keys()]
            edges = [(req, file) for file, value in content.items() for req in value.get("requires", [])]

            for node in nodes:
                script = content.get(node, {}).get("script")
                type = content.get(node, {}).get("type")
                if type == NODEJS_TYPE:
                    wd = os.path.join(ws_realpath, node)
                    graphs[op].add_node(node, function=run_nodejs_script(script, wd, env))
                    pass
                else:
                    if script is not None:
                        script_full_path = os.path.join(ws_realpath, node, script)
                    else:
                        script_full_path = None
                    environment = content.get(node, {}).get("environment", {})
                    environment_list = [ f"{k}={v}" for k, v in environment.items()]
                    graphs[op].add_node(node, function=run_operation_script(script_full_path, env + environment_list))

            graphs[op].add_edges_from(edges)

        self.graphs = graphs
        self.operations = files_per_operation

    def visualize_operations(self):
        for operation, graph in self.graphs.items():
            plt.figure(operation)
            color_map = graafilohi.ExecutableDirectedMultiGraph.get_node_colors(graph)
            nx.draw(graph, node_color=color_map, with_labels=True)
        plt.show()

    def visualize_operations_and_save(self):
        for operation, graph in self.graphs.items():
            plt.figure(operation)
            color_map = graafilohi.ExecutableDirectedMultiGraph.get_node_colors(graph)
            nx.draw(graph, node_color=color_map, with_labels=True)
            plt.savefig(f"{SAVE_FILE_PREFIX}-{operation}.png")
        plt.show()

    def simulate_execute_operation(self, operation):
        if operation is None:
            operation = read_selection(self.graphs.keys(), "Select an operation...").get("selection", None)

        if operation not in self.graphs:
            print(f"Unknown operation: {operation}")
            return

        self.graphs[operation].simulate_execute()

    def execute_operation(self, operation):
        if operation is None:
            operation = read_selection(self.graphs.keys(), "Select an operation...").get("selection", None)

        if operation not in self.graphs:
            print(f"Unknown operation: {operation}")
            return
        try:
            self.graphs[operation].execute()
        except OperationExecutionError as e:
            print("Operation failed. Script returned non-zero exit value.")
            print(e)

    def list_operations(self):
        print("Available operations:")
        for operation, files in self.operations.items():
            print(f"{'':4}{operation}:")
            print(f"{'':8}targets:")
            for file in files.keys():
                print(f"{'':12}{file}")