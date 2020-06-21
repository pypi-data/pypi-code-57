import json
import urllib
from requests.exceptions import HTTPError
import networkx as nx
from networkx.readwrite import json_graph

from collections import MutableMapping
from collections import MutableSequence

import copy


class Paper(MutableMapping):
    """
    Contains a single paper object and behaves like a Dict.
    Abstract base class of MutableMapping (see: https://treyhunner.com/2019/04/why-you-shouldnt-inherit-from-list-and-dict-in-python/)
    Did not use UserDict because of it's legacy status and subclassing from Dict would require re-implementing some basic behaviour (see link)
    """

    def __init__(self, filename=None, doi=None, data=()):
        """
        Initialize a Paper with at least a 'title' and a 'paperId'. Data source can either be directly from the API of semanticscholar.org via a DOI, or from a file, or by initializing.
        Will follow the layout of the data returned by the API of semanticscholar.org

        :param filename: location of a json file to load
        :param doi: full DOI that will be use to retreive the item from semantic scholar.org
        :param data: a dict containing the description of a paper

        """

        self.mapping = {}
        self.update(data)

        if filename and doi:
            raise ValueError("Cannot use both filename and doi to retreive paper")
        elif filename:
            self.load_from_file(filename)
        elif doi:
            self.load_from_semantic_scholar(doi)

    def __getitem__(self, key):
        return self.mapping[key]

    def __delitem__(self, key):
        """ Enforces a paper always has a title and paperId"""
        if key == 'title':
            raise ValueError('Paper cannot have an empty title')

        if key == 'paperId':
            raise ValueError('Paper cannot have an empty paperId')
        del self.mapping[key]

    def __setitem__(self, key, value):
        """ Enforces a paper always has a title and paperId"""
        if key == 'title' and not value:  # empty strings are falsy https://www.python.org/dev/peps/pep-0008/#id51
            raise ValueError('Paper cannot have an empty title')

        if key == 'title' and not isinstance(value, str):
            raise TypeError('title must be a string')

        if key == 'paperId' and not value:
            raise ValueError('Paper cannot have an empty paperId')

        if key == 'paperId' and not isinstance(value, str):
            raise TypeError('paperId must be a string')

        self.mapping[key] = value

    def __iter__(self):
        return iter(self.mapping)

    def __len__(self):
        return len(self.mapping)

    def __repr__(self):
        return f"{type(self).__name__}({self.mapping})"

    # def __str__(self):
    #    return self.mapping['title']

    def load_url(self, url):
        try:
            f = urllib.request.urlopen(url)
        except urllib.error.HTTPError as e:
            print('Could not download page')
            return False
        else:
            return f

    def validate_json(self, json_data):
        if 'title' not in json_data:
            raise ValueError("Paper is missing the title key")

        if 'paperId' not in json_data:
            raise ValueError("Paper is missing the paperId key")

        return True

    def load_from_semantic_scholar(self, doi):
        url = 'https://api.semanticscholar.org/v1/paper/'

        data = self.load_url("{}{}".format(url, doi))

        if not data:
            raise ValueError("Download failed")

        json_data = json.loads(data.read())

        if not self.validate_json(json_data):
            raise ValueError("Not passing validation on JSON file")

        self.mapping = json_data

    def load_from_file(self, fname):
        f = open(fname, 'r')
        s = f.read()
        f.close()
        json_data = json.loads(s)

        if not self.validate_json(json_data):
            raise ValueError("Not passing validation on JSON file")

        self.mapping = json_data


class PaperList(MutableSequence):
    """
    Behaves almost like a list except that 1) elements need to be Paper and 2) paperId needs to be unique (set-like)
    Additionally can be populated from a doi list or filename list
    From https://docs.python.org/3/library/collections.abc.html#collections.abc.MutableSequence
    Concrete subclasses must provide __new__ or __init__, __getitem__, __setitem__, __delitem__, __len__, and insert().

    """

    def __init__(self, _list):
        self._list = []
        for el in _list:
            self.append(el)

    def _is_unique(self, paper):
        """Ensures the PaperList does not contain Papers with the same paperId """
        if type(paper) is not Paper:
            raise TypeError("the item you are trying to add should be of the type Paper")

        if paper['paperId'] in [paper['paperId'] for paper in self._list]:  # only allow unique paperId
            raise ValueError("This paperId is already present, only unique paperIds allowed")

        return True

    def __len__(self):
        return len(self._list)

    def __getitem__(self, item):
        return self._list[item]

    def __delitem__(self, item):
        del self._list[item]

    def __setitem__(self, index, value):
        if self._is_unique(value):
            self._list[index] = value

    def insert(self, index, value):
        if self._is_unique(value):
            self._list.insert(index, value)

    def load_from_semantic_scholar(self, doi_list):
        """
        Given a list of strings that have a (valid) DOI, pull down the data from semantic scholar
        :param doi_list: list of strings containg a DOI

        """

        if type(doi_list) is not list:
            raise TypeError("the doi_list must be a list of strings")

        for this_doi in doi_list:
            if type(this_doi) is not str:
                raise TypeError("the doi in the doi_list must be strings")

            new_paper = Paper()
            new_paper.load_from_semantic_scholar(this_doi)
            self.append(new_paper)

    def load_from_file(self, filename_list):
        """
        Given a list of filenames pointing to json files populate a PaperList

        :param filename_list:  list of strings containing the path to the json files

        TODO: implement pathtype https://docs.python.org/3/library/pathlib.html#module-pathlib
        """
        if type(filename_list) is not list:
            raise TypeError("the filename_list must be a list of strings")

        for this_filename in filename_list:
            if type(this_filename) is not str:
                raise TypeError("the filename in the doi_list must be strings")
            new_paper = Paper()
            new_paper.load_from_file(this_filename)
            self.append(new_paper)

    # TODO: Implement the proper __str__
    def __str__(self):
        return "[" + ", ".join([str(paper) for paper in self]) + "]"

    def __eq__(self, other):
        """ Compare two PaperLists
        Note that the order matters. So [A,B] != [B,A]
        """

        # if not isinstance(other, PaperList):
        #    TypeError('object to compare needs to be a PaperList')
        if len(self) != len(other):
            return False

        for idx, element in enumerate(self):
            if element != other[idx]:
                return False
        return True

    @property
    def titles(self):
        """ returns a list of title strings. ie ['title - a', 'title - b']"""
        return [paper['title'] for paper in self._list]

    @property
    def paperIds(self):
        """ returns a list of paperId strings. ie ['a', 'b']"""
        return [paper['paperId'] for paper in self._list]


class PaperNetwork(object):
    """
    Main class translates Papers into NetworkX DiGraph.
    Exposes two main attributes:
    * collection is a PaperList of Papers
    * graph is a NetworkX DiGraph based on the collection


    """

    # Defines which attributes from the paper instance to copy over into the NetworkX graph
    ATTRIBUTE_LIST = ['title', 'year', 'url', 'authors', 'venue', 'warning']

    def __init__(self, doi_list=None, filename_list=None):
        """

        :param doi_list: list of DOIs, elements in string format. Will be fetched from semantic scholar directly
        :param filename_list: list of filenames, elements in string format. 

        """

        self.collection = PaperList([])
        self._graph = nx.DiGraph()  # create empty Directional graph with NetworkX: https://networkx.github.io/documentation/stable/reference/classes/digraph.html

        self._previous_collection = PaperList([])
        self._previous_graph = nx.DiGraph()
        
        if doi_list:
            self.collection.load_from_semantic_scholar(doi_list)

        if filename_list:
            self.collection.load_from_file(filename_list)
        

    @property
    def graph(self):
        """
        A NetworkX DiGraph containing the paper network.

        The graph is recalculated when the collection is changed.
        This does mean that any previous changes made to the graph are overwritten

        The accessor of the graph.node is the paperId

        """

        if self.collection != self._previous_collection:

            self._previous_collection = copy.deepcopy(self.collection)
            # self._previous_collection = PaperList(self.collection) #We need a deepcopy as above to track changes in the PaperList, this does not work

            self._graph = nx.DiGraph()  # Start with an empty graph again
            self._parse_papers()
        return self._graph

    def _copy_paper_attributes_to_graph(self, node, json):
        """
        :param node: the key to the node on the graph object
        :param json: this can either be a Paper instance (and thus accessed like a Dict) or a Dict (for example when passed from references or citations)
        """

        if not isinstance(node, str):
            raise TypeError('Node identifier needs to be a string, such as the paperId')

        if not (isinstance(json, Paper) or isinstance(json, dict)):
            raise TypeError('JSON argument needs to be a Paper or dict')

        if node in self._graph.nodes():
            for this_key in self.ATTRIBUTE_LIST:
                if this_key in json:
                    self._graph.nodes[node][this_key] = json[this_key]
                else:
                    self._graph.nodes[node][this_key] = []
        else:
            raise ValueError('The node is not part of the graph, add the node first')

    def _parse_papers(self):
        """
        Go through all the Papers in the collection and add them to the NetworkX DiGraph
        The index of on the node is the paperId

        """
        for this_paper in self.collection:
            self._graph.add_node(this_paper['paperId'])
            self._copy_paper_attributes_to_graph(this_paper['paperId'], this_paper)

            for this_citation in this_paper['citations']:
                self._graph.add_edge(this_citation['paperId'], this_paper['paperId'])  # not this is directional!
                self._copy_paper_attributes_to_graph(this_citation['paperId'], this_citation)

            for this_reference in this_paper['references']:
                self._graph.add_edge(this_paper['paperId'], this_reference['paperId'])  # note that this is directional!
                self._copy_paper_attributes_to_graph(this_reference['paperId'], this_reference)

            if len(this_paper['references']) < 10:
                self._graph.nodes[this_paper['paperId']]['warning'].append('Serious warning: reference list seems very short (<10)')

            if len(this_paper['citations']) < 10:
                self._graph.nodes[this_paper['paperId']]['warning'].append('Note: seems like not widely cited (<5)')

    def calculate_json(self, mimimum_citation_count_of_references=1, minimum_times_citing_collection=1):
        """

        Returns a json representation of the graph
        :param mimimum_citation_count_reference: how often is a reference paper cited by the collection? All reference papers are at least cited once (otherwise they would not be in the graph). A number higher than 1 will thus reduce the number of nodes reported back.  Defined as >= not > (default = 1)
        :param minimum_times_citing_collection: how often is a paper citing papers in the collection? A number higher than 1 will thus reduce the number of nodes reported back. Defined as >= not > (default = 1)

        Returns a JSON representation of the graph containing 'nodes' and 'links'. The JSON can be read, for example, by D3.

        """

        # Note that in this function we use self._graph and self.graph. _graph is used when writing properties to the graph, while graph is used for read actions.

        REFERENCE_PAPER = 0
        PRE_COLLECTION_PAPER = 5
        COLLECTION_PAPER = 1


        paper_type = {}  # contains a numerical representation of the paper type

        times_citing_collection = {}

        # Set paper_type on all papers to REFERENCE_PAPER
        for paper in self.graph.nodes():
            paper_type.update({paper: REFERENCE_PAPER})

        # Tag all the predecessor papers from the collection with PRE_COLLECTION_PAPER
        for my_paper in self.collection:
            if my_paper['paperId'] in self.graph.nodes:
                for pre_paper in self.graph.predecessors(my_paper['paperId']):
                    paper_type.update({pre_paper: PRE_COLLECTION_PAPER})

        # Tag all the collection papers with bb=1 (note that this will overwrite the 5 from above)
        for paper in self.graph.nodes():
            if paper in self.collection.paperIds:
                paper_type.update({paper: COLLECTION_PAPER})

            times_citing_collection[paper] = 0  # initialize 0 otherwise datatables complains

        # Set the total number of incoming citations for each node, including references. This helps to find which references are often cited
        for ix, indeg in self.graph.in_degree():
            self._graph.nodes[ix]['in_degree'] = indeg

        for my_paper in self.collection.paperIds:
            for pre_paper in self.graph.predecessors(my_paper):  # Limit the citation count to only the collection
                times_citing_collection[pre_paper] = times_citing_collection.get(pre_paper, 0) + 1  # count the outgoing references to collection papers

        nx.set_node_attributes(self._graph, paper_type, 'corpus')
        #nx.set_node_attributes(self._graph,citesize, 'citesize')
        #nx.set_node_attributes(self._graph, id_dict,'id_name')
        nx.set_node_attributes(self._graph, times_citing_collection, 'out_degree')

        
        if mimimum_citation_count_of_references > 1 or minimum_times_citing_collection > 1:
            #degree_dict = dict(G.in_degree(G.nodes()))

            # Always include the collection it self (last part of the list)
            nodes_to_plot = [k for k, v in dict(self.graph.in_degree(self.graph.nodes())).items() if v >= mimimum_citation_count_of_references] + [k for k, v in times_citing_collection.items() if v >= minimum_times_citing_collection] + self.collection.paperIds
            self._graph = self.graph.subgraph(nodes_to_plot)


        data = json_graph.node_link_data(self.graph, attrs={'id':'id', 'source': 'source', 'target': 'target', 'key': 'key'})
        
        return data

    def __str__(self):
        return ', '.join([str(paper['title']) for paper in self.collection])