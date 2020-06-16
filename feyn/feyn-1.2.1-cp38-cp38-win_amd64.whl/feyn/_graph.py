"""A graph is a path from some input registers to an output register.

The graph is a result of running a simulation. It is one of the many possible paths from the inputs to the output. It can be compared to a model in various other machine learning frameworks.
"""
import json
from pathlib import Path
from typing import AnyStr, TextIO, Union

import numpy as np

import _feyn
import feyn
import feyn.losses

# Update this number whenever there are breaking changes to save/load
# (or to_dict/from_dict). Then use it intelligently in Graph.load.
SCHEMA_VERSION = "2020-02-07"

PathLike = Union[AnyStr, Path]

def _lattice_loc_hash(location):
    return location[0] + location[1]*1000 + location[2]*100000

class Graph(_feyn.Graph):
    """
    A Graph represents a single mathematical model which can be used used for predicting.

    The constructor is for internal use. You will typically use `QGraph[ix]` to pick graphs from QGraphs, or load them from a file with Graph.load().

    Arguments:
        size -- The number of nodes this graph contains. The actual nodes must be added to the graph after construction.
    """

    def __init__(self, size: int):
        """Construct a new 'Graph' object."""
        super().__init__(size)

        self.loss_value = None

    def predict(self, X) -> np.ndarray:
        """
        Calculate predictions based on input values.

        >>> graph.predict({ "age": [34, 78], "sex": ["male", "female"] })
        [True, False]

        Arguments:
            X -- The input values. Can be either a dict mapping register names to value arrays, or a pandas.DataFrame.

        Returns:
            np.ndarray -- The calculated predictions.
        """
        if type(X).__name__ == 'dict':
            for k in X:
                if type(X[k]).__name__ == 'list':
                    X[k] = np.array(X[k])

        # Magic support for pandas DataFrame
        if type(X).__name__ == "DataFrame":
            X = {col: X[col].values for col in X.columns}

        return super()._query(X, None)

    @property
    def edges(self) -> int:
        """Get the total number of edges in this graph."""
        return super().edge_count

    @property
    def depth(self) -> int:
        """Get the depth of the graph"""
        return self[-1].depth

    def save(self, file: Union[PathLike, TextIO]) -> None:
        """
        Save the `Graph` to a file-like object.

        The file can later be used to recreate the `Graph` with `Graph.load`.

        Arguments:
            file -- A file-like object or path to save the graph to.
        """
        as_dict = self._to_dict()
        as_dict["version"] = SCHEMA_VERSION

        if isinstance(file, (str, bytes, Path)):
            with open(file, mode="w") as f:
                json.dump(as_dict, f)
        else:
            json.dump(as_dict, file)

    @staticmethod
    def load(file: Union[PathLike, TextIO]) -> object:  # we cant reference graph here. Doc website needs a return signature
        """
        Load a `Graph` from a file.

        Usually used together with `Graph.save`.

        Arguments:
            file -- A file-like object or a path to load the `Graph` from.

        Returns:
            Graph -- The loaded `Graph`-object.
        """
        if isinstance(file, (str, bytes, Path)):
            with open(file, mode="r") as f:
                as_dict = json.load(f)
        else:
            as_dict = json.load(file)

        return Graph._from_dict(as_dict)

    def __hash__(self):
        return super().__hash__()

    def __eq__(self, other):
        return other.__hash__() == self.__hash__()

    def __contains__(self, item:str):
        return item in [interaction.name for interaction in self]

    def _fit(self, data, epochs, loss_function, verbose=False):
        out_reg = self[-1]
        Y = data[out_reg.name]

        out_reg._loss = loss_function.c_derivative

        for epoch in range(epochs):
            predictions = super()._query(data, Y)
            self.loss_value = loss_function(Y.astype(float), predictions)

            if verbose:
                print("Epoch %i: loss %.4f" %(epoch, self.loss_value))

        return self.loss_value

    def _to_dict(self):
        nodes = []
        links = []
        for ix in range(len(self)):
            interaction = self[ix]
            nodes.append({
                "id": interaction._index,
                "spec": interaction.spec,
                "location": interaction._latticeloc,
                "peerlocation": interaction._peerlocation,
                "legs": len(interaction.sources),
                "strength": interaction._strength,
                "name": interaction.name,
                "state": interaction.state._to_dict()
            })
            for ordinal, src in enumerate(interaction.sources):
                if src != -1:
                    links.append({
                        'source': src,
                        'target': interaction._index,
                        'ord': ordinal
                    })

        return {
            'directed': True,
            'multigraph': True,
            'nodes': nodes,
            'links': links
        }

    def _repr_svg_(self):
        return feyn._current_renderer.rendergraph(self)

    @staticmethod
    def _get_interaction(data: dict) -> _feyn.Interaction:
        interaction = feyn.Interaction(data["spec"], tuple(data["location"]), peerlocation=data["peerlocation"], strength=data["strength"], name=data["name"])
        interaction.state._from_dict(data["state"])

        return interaction

    @staticmethod
    def _from_dict(gdict):
        sz = len(gdict["nodes"])
        graph = Graph(sz)
        for ix, node in enumerate(gdict["nodes"]):
            interaction = Graph._get_interaction(node)
            graph[ix] = interaction

        for edge in gdict["links"]:
            interaction = graph[edge["target"]]
            ord = edge["ord"]
            interaction._set_source(ord, edge["source"])
        return graph
