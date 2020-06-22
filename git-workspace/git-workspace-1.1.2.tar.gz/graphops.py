import graafilohi
import os
import json
import sys
import matplotlib.pyplot as plt
import networkx as nx
import subprocess
import locale

GRAPH_DESCRIPTION_FILE = ".git-ws.graphops"
SAVE_FILE_PREFIX = "git-ws.graphops"


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
                                   stderr=subprocess.PIPE, cwd=script_directory)
        while True:
            output = process.stdout.readline()
            if process.poll() is not None:
                break
            if output:
                print(output.strip().decode(locale.getpreferredencoding()))
        retval = process.poll()

        if retval > 0:
            raise OperationExecutionError(f"Script execution failed: {script_file_absolute_path}")

    script_name = os.path.basename(os.path.realpath(script_file_absolute_path))
    script_function.__name__ = f"{script_name}-function"
    return script_function


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
                if script is not None:
                    script_full_path = os.path.join(ws_realpath, node, script)
                else:
                    script_full_path = None
                graphs[op].add_node(node, function=run_operation_script(script_full_path, env))

            graphs[op].add_edges_from(edges)

        self.graphs = graphs

    def visualize_operations(self):
        keys = list(self.graphs.keys())
        for operation, graph in self.graphs.items():
            plt.figure(keys.index(operation))
            color_map = graafilohi.ExecutableDirectedMultiGraph.get_node_colors(graph)
            nx.draw(graph, node_color=color_map, with_labels=True)
        plt.show()

    def visualize_operations_and_save(self):
        keys = list(self.graphs.keys())
        for operation, graph in self.graphs.items():
            plt.figure(keys.index(operation))
            color_map = graafilohi.ExecutableDirectedMultiGraph.get_node_colors(graph)
            nx.draw(graph, node_color=color_map, with_labels=True)
            plt.savefig(f"{SAVE_FILE_PREFIX}-{operation}.png")
        plt.show()

    def simulate_execute_operation(self, operation):
        if operation not in self.graphs:
            print(f"Unknown operation: {operation}")
            return

        self.graphs[operation].simulate_execute()

    def execute_operation(self, operation):
        if operation not in self.graphs:
            print(f"Unknown operation: {operation}")
            return
        try:
            self.graphs[operation].execute()
        except OperationExecutionError as e:
            print("Operation failed. Script returned non-zero exit value.")
            print(e)
