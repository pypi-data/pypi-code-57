"""Implements the "Bottle" interface."""
import uuid
from typing import Dict, List, Any
import io
import json

import requests

from ialib.genie_metalanguage import *
from ialib.genome_info import Genome


class QueryError(Exception):
    """Raised if any query to any node returns an error."""
    pass


class ConnectionError(Exception):
    """Raised if any query to any node returns an error."""
    pass


class BottleClient:
    """Interface for interacting with bottles."""
    def __init__(self, bottle_info):
        """
        Provide bottle information in a dictionary.

        ex:
        from ialib.BottleClient import BottleClient

        bottle_info = {'api_key': 'ABCD-1234',
                    'name': 'genie-bottle',
                    'domain': 'intelligent-artifacts.com',
                    'secure': False}

        bottle = BottleClient(bottle_info)
        bottle.connect()

        bottle.setIngressNodes(['P1'])
        bottle.setQueryNodes(['P1'])

        """
        self.genome = None
        self.bottle_info = bottle_info
        self.name = bottle_info['name']
        self.domain = bottle_info['domain']
        self.api_key = bottle_info['api_key']
        self.ingress_nodes = []
        self.query_nodes = []
        self.all_nodes = []
        self.failures = []
        self.system_failures = []
        self._connected = False
        self.genome = None
        self.genie = None
        self.local = False
        if 'secure' not in self.bottle_info or self.bottle_info['secure']:
            self.secure = True
        else:
            self.secure = False
        self.url = 'https://{name}.{domain}/api'.format(**self.bottle_info)
        if 'local' in self.bottle_info and self.bottle_info['local']:
            self.url = 'http://localhost/api'
            self.local = True

    def __repr__(self) -> str:
        return '<{name}.{domain}| secure: %r, connected: %s, genie: %s, \
                  ingress_nodes: %i, query_nodes: %i, failures: %i>'.format(
                      **self.bottle_info) % (
                          self.secure, self._connected, self.genie, len(self.ingress_nodes), len(self.query_nodes), len(self.failures))

    def connect(self) -> Dict:
        """Grabs the bottle's genie's genome for node definitions."""
        response_data = requests.post(self.url, verify=self.secure, json={"method": "connect", "params": {"api_key": self.api_key}, "jsonrpc": "2.0", "id": 1}).json()
        if 'result' not in response_data:
            self._connected = False
            raise ConnectionError("Connection failed!", response_data)

        result = response_data['result']
        self.genome = Genome(result['genome'])
        self.genie = result['genome']['agent']
        self.all_nodes = [{"name": i['name'], "id": i['id']} for i in self.genome.primitives.values()]
        if result['connection'] == 'okay':
            self._connected = True
        else:
            self._connected = False

        return {'connection': result['connection'], 'genie': result['genie']}

    def set_ingress_nodes(self, nodes: List = None) -> List:
        """Use list of primitive names to define where data will be sent."""
        if nodes is None:
            nodes = []
        self.ingress_nodes = [{'id': self.genome.primitive_map[node], 'name': node} for node in nodes]
        return self.ingress_nodes

    def set_query_nodes(self, nodes: List = None) -> List:
        """Use list of primitive names to define which nodes should return answers."""
        if nodes is None:
            nodes = []
        self.query_nodes = [{'id': self.genome.primitive_map[node], 'name': node} for node in nodes]
        return self.query_nodes

    def _query(self, method: str, data: Dict = None, nodes: List = None, unique_id: str = None) -> List:
        """Internal helper function to make an RPC call with the given *query* and *data*."""
        if not self._connected:
            raise ConnectionError('Not connected to a bottle. You must call `connect()` on a BottleClient instance before making queries')
        result = []
        if unique_id is not None:
            if data:
                    data['unique_id'] = unique_id
            else:
                data = {'unique_id': unique_id}

        if isinstance(nodes[0], str):
            nodes = [{'name': name, 'id': self.genome.primitive_map[name]} for name in nodes]
        for node in nodes:
            try:
                if data is not None:
                    response = requests.post(self.url, verify=self.secure, json={"method": method, "params": {"api_key": self.api_key, "primitive_id": node['id'], 'data': data},
                         "jsonrpc": "2.0", "id": 1}).json()
                    response = response['result']
                else:
                    response = requests.post(self.url, verify=self.secure, json={"method": method, "params": {"api_key": self.api_key, "primitive_id": node['id']},
                         "jsonrpc": "2.0", "id": 1}).json()
                    response = response['result']
                result.append({node['name']: response})
            except Exception as exception:
                self.failures.append({node['name']: {'class': exception.__class__.__name__, 'message': str(exception)}})
                raise QueryError("Query Failure:", {'class': exception.__class__.__name__, 'message': str(exception)}) from exception
        if unique_id is not None:
            return result, unique_id
        return result

    def query(self, node, query, data=None, nodes: List = None):
        """Direct to bottle RPC call with the given *query* and *data*."""
        result = []
        try:
            if data:
                response = requests.post(self.url, verify=self.secure, json={"method": query, "params": {"api_key": self.api_key, "primitive_id": self.genome.primitive_map[node], 'data': data},
                        "jsonrpc": "2.0", "id": 1}).json()
                response=response['result']
            else:
                response = requests.post(self.url, verify=self.secure, json={"method": query, "params": {"api_key": self.api_key, "primitive_id": self.genome.primitive_map[node]},
                        "jsonrpc": "2.0", "id": 1}).json()['result']
            result.append({node: response})
        except Exception as exception:
            self.failures.append({node: exception})
            raise Exception("Query Failure:", {node: exception})
        return result

    def observe(self, data: Dict = None, nodes: List = None) -> List:
        """Exclusively uses the 'observe' call.  All commands must be provided via Genie Metalanguage data."""
        if nodes is None:
            nodes = self.ingress_nodes
        return self._query('observe', data, nodes=nodes)

    def observe_event(self, data: Dict = None, unique_id: str = None) -> List:
        """Exclusively uses the 'observe' call.  All commands must be provided via Genie Metalanguage data."""
        results = []
        if unique_id is None:
            unique_id = str(uuid.uuid4())
        for node, node_data in data.items():
            result, uid = self._query('observe', node_data, nodes=[node], unique_id=unique_id)
            results.append(result[0])
        return results, uid

    def observe_classification(self, data=None, nodes: List = None):
        """
        Best practice is to send a classification to all [ingress and] query nodes as a singular symbol in the last event.
        This function does that for us.
        """
        if not self._connected:
            raise ConnectionError('Not connected to a bottle. You must call `connect()` on a BottleClient instance before making queries')
        if nodes is None:
            nodes = self.query_nodes
        return self._query("observe", data, nodes=nodes)

    def show_status(self, nodes: List = None) -> List:
        """Return the current status of the bottle."""
        if nodes is None:
            nodes = self.all_nodes
        return self._query('showStatus', nodes=nodes)

    def learn(self, nodes: List = None) -> List:
        """Return the learn results."""
        if nodes is None:
            nodes = self.ingress_nodes
        return self._query('learn', nodes=nodes)

    def get_wm(self, nodes: List = None) -> List:
        """Return information about Working Memory."""
        if nodes is None:
            nodes = self.all_nodes
        return self._query('getWM', nodes=nodes)

    def get_predictions(self, unique_id: str = None, nodes: List = None) -> List:
        """Return prediction result data."""
        if nodes is None:
            nodes = self.query_nodes
        return self._query('getPredictions', nodes=nodes, unique_id=unique_id)

    def clear_wm(self, nodes: List = None) -> List:
        """Clear the Working Memory of the Genie."""
        if nodes is None:
            nodes = self.ingress_nodes
        return self._query('clearWM', nodes=nodes)

    def clear_all_memory(self, nodes: List = None) -> List:
        """Clear both the Working Memory and persisted memory."""
        if nodes is None:
            nodes = self.ingress_nodes
        return self._query('clearAllMemory', nodes=nodes)

    def get_percept_data(self, nodes: List = None) -> List:
        """Return percept data."""
        if nodes is None:
            nodes = self.query_nodes
        return self._query('getPerceptData', nodes=nodes)

    def get_cognition_data(self, nodes: List = None) -> List:
        """Return cognition data."""
        if nodes is None:
            nodes = self.query_nodes
        return self._query('getCognitionData', nodes=nodes)

    def get_cogitated(self, nodes: List = None) -> List:
        """Return cogitated data."""
        if nodes is None:
            nodes = self.query_nodes
        return self._query('getCogitated', nodes=nodes)

    def get_decision_table(self, nodes: List = None) -> List:
        """Return a decision table."""
        if nodes is None:
            nodes = self.query_nodes
        return self._query('getDecisionTable', nodes=nodes)

    def get_action_data(self, nodes: List = None) -> List:
        """Return action data."""
        if nodes is None:
            nodes = self.query_nodes
        return self._query('getActionData', nodes=nodes)

    def change_genes(self, gene_data: Dict) -> List:
        """
        Use primitive names.
        This will do live updates to an existing agent, rather than stopping an agent and starting a new one as per 'injectGenome'.
        gene_data of form:

            {node-name: {gene: value}}

        where node-id is the ID of a primitive or manipulative.

        Only works on primitive nodes at this time.
        """
        if not self._connected:
            raise ConnectionError('Not connected to a bottle. You must call `connect()` on a BottleClient instance before making queries')
        self.genome.change_genes(gene_data)
        result = []
        for node, updates in gene_data.items():  ## only primitive nodes at this time.
            for gene, value in updates.items():
                response = requests.post(self.url, verify=self.secure, json={'params': {'api_key': self.api_key, 'primitive_id': self.genome.primitive_map[node], 'data': {gene: value}}, 'method': 'updateGenes', 'jsonrpc': '2.0', 'id': 1}
                    ).json()
                if 'error' in response or response["result"] != 'updated-genes':
                    self.system_failures.append({node: response})
                    print("System Failure:", {node: response})
                result.append({node: response})
        return result

    def inject_genome(self, genome: Dict) -> Dict:
        """Halt all primitives in the current bottle and start those described in *genome*.

        *genome* must be either a JSON-serializable object or a file-like object.
        """
        if not self._connected:
            raise ConnectionError('Not connected to a bottle. You must call `connect()` on a BottleClient instance before making queries')
        if isinstance(genome, io.TextIOBase):
            genome = json.load(genome)

        self.genome.change_genes(genome)
        response = requests.post(self.url, verify=self.secure, json={"method": "injectGenome", "params": {"api_key": self.api_key, 'genome': json.dumps(genome)}, "jsonrpc": "2.0", "id": 1})

        if response.status_code != 200:
            self.system_failures.append({'bottle-api': response.json()})
            print("System Failure:", {'bottle-api': response.json()})

        return response.json()

    def get_cost_benefit(self, nodes: List = None) -> List:
        """Return cost benefit"""
        if nodes is None:
            nodes = self.query_nodes
        return self._query('getCostBenefit', nodes=nodes)

    def get_gene(self, gene: Dict, nodes: List = None) -> List[Dict[str, Dict[str, str]]]:
        """
        Use primitive names.
        This will return the gene-value of an existing agent, gene_data of form (similar to that
        of the change_genes method):

            {node-name: gene}

        where node-name is the ID of a primitive or manipulative.

        Only works on primitive nodes at this time.
        """
        if not self._connected:
            raise ConnectionError('Not connected to a bottle. You must call `connect()` on a BottleClient instance before making queries')
        result = []
        for node_name, attribute in gene.items():
            try:
                response = requests.post(self.url, verify=self.secure, json={"method": "getGene", "params": {"api_key": self.api_key, "primitive_id": self.genome.primitive_map[node_name], "data": attribute},
                     "jsonrpc": "2.0", "id": 1}).json()['result']
                result.append({node_name: {attribute : response}})

            except Exception as exception:
                self.failures.append({node_name: exception})
                raise Exception("Query Failure:", {node_name: exception})

        return result

    def get_model(self, data: Dict, nodes: List = None) -> List[Dict[str, Dict[str, str]]]:
        """
        Returns model.

        data : {primitive_name : name}

        Model name is unique, so it should not matter that we query all nodes, only
        one model will be found. How will the absense of a name in a primitive be
        conveyed?
        """
        if not self._connected:
            raise ConnectionError('Not connected to a bottle. You must call `connect()` on a BottleClient instance before making queries')
        result = []
        for node_name, model_name in data.items():
            try:
                response = requests.post(self.url, verify=self.secure, json={"method": "getModel", "params": {"api_key": self.api_key, "primitive_id": self.genome.primitive_map[node_name], "data": model_name},
                     "jsonrpc": "2.0", "id": 1}).json()['result']
                result.append({node_name: {model_name : response}})

            except Exception as exception:
                self.failures.append({node_name: exception})
                raise Exception("Query Failure:", {node_name: exception})

        return result

    def get_name(self, nodes: List = None) -> List[Dict[str, str]]:
        """
        """
        if nodes is None:
            nodes = self.all_nodes
        return self._query('getName', True, nodes=nodes)

    def get_time(self, nodes: List = None) -> List:
        """
        """
        if nodes is None:
            nodes = self.all_nodes
        return self._query('getTime', True, nodes=nodes)

    def get_vector(self, data: Dict) -> List:
        """
        """
        if not self._connected:
            raise ConnectionError('Not connected to a bottle. You must call `connect()` on a BottleClient instance before making queries')
        result = []
        for node_name, vector_name in data.items():
            try:
                response = requests.post(self.url, verify=self.secure, json={"method": "getVector", "params": {"api_key": self.api_key, "primitive_id": self.genome.primitive_map[node_name], "data": vector_name},
                     "jsonrpc": "2.0", "id": 1}).json()['result']
                result.append({node_name: {vector_name: response}})

            except Exception as exception:
                self.failures.append({node_name: exception})
                raise Exception("Query Failure:", {node_name: exception})

        return result

    def increment_recall_threshold(self, data: Dict) -> List[Dict[str, Any]]:
        """
        TODO: update local genome
        TODO: Change param name 'data' -> 'increment'
        """
        if not self._connected:
            raise ConnectionError('Not connected to a bottle. You must call `connect()` on a BottleClient instance before making queries')
        result = []
        for node_name, val in data.items():
            try:
                response = requests.post(self.url, verify=self.secure, json={"method": "incrementRecallThreshold", "params": {"api_key": self.api_key, "primitive_id": self.genome.primitive_map[node_name], "data": val},
                     "jsonrpc": "2.0", "id": 1}).json()['result']
                result.append({node_name: {"recall_threshold": response}})

            except Exception as exception:
                self.failures.append({node_name: exception})
                raise Exception("Query Failure:", {node_name: exception})

        return result

    def show_predictions_knowledge_details(self) -> List:
        """
        """
        return []

    def start_acting(self, nodes: List = None) -> List[Dict[str, Any]]:
        """
        Allow query nodes to start acting.

        TODO: Should user be able to specify which nodes.
        """
        if nodes is None:
            nodes = self.query_nodes
        return self._query('startActing', True, nodes=nodes)

    def start_sleeping(self, nodes: List = None) -> List[Dict[str, Any]]:
        """
        Tells all nodes to start sleeping.

        TODO: Should user be able to specify which nodes.
        """
        if nodes is None:
            nodes = self.all_nodes
        return self._query('startSleeping', True, nodes=nodes)

    def stop_acting(self, nodes: List = None) -> List[Dict[str, Any]]:
        """
        Stop query nodes from acting.

        TODO: Should user be able to specify which nodes.
        """
        if nodes is None:
            nodes = self.query_nodes
        return self._query('stopActing', True, nodes=nodes)

    def stop_sleeping(self, nodes: List = None) -> List[Dict[str, Any]]:
        """
        Wakes up all sleeping nodes.

        TODO: Should user be able to specify which nodes.
        """
        if nodes is None:
            nodes = self.all_nodes
        return self._query('stopSleeping', True, nodes=nodes)

    def ping(self, nodes: List = None) -> List[Dict[str, Any]]:
        """Ping a node to ensure it's up."""
        if nodes is None:
            nodes = self.all_nodes

        if not self._connected:
            raise ConnectionError(
                'Not connected to a bottle. You must call `connect()` on a BottleClient instance before making queries')

        return requests.post(self.url, verify=self.secure, json={"method": "ping", "jsonrpc": "2.0", "id": 1}).json()['result']
