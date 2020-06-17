import string
import itertools
import numpy as np
import pandas as pd
from functools import lru_cache
from tributary.lazy import Node
from ipywidgets import Output, VBox
from perspective import Table, PerspectiveWidget


@lru_cache(None)
def _genData():
    return list(string.ascii_uppercase)  # + list(''.join(_) for _ in itertools.product(string.ascii_uppercase, repeat=2))


class Grid(object):
    def __init__(self):
        schema = {x: str for x in _genData()}
        schema['index'] = int

        self._table = Table(schema, index='index')
        l = np.empty((100, ), str)
        data = {x: l for x in _genData()}
        data['index'] = np.arange(100)
        self._table.update(pd.DataFrame(data))
        self._widget = PerspectiveWidget(self._table, columns=_genData(), editable=True)
        self._widget.on_update(self.handle_message)
        self._out = Output()
        self._graph = VBox([])
        self._nodes = {}

    def render(self):
        return VBox([self._widget, self._out, self._graph])

    def handle_message(self, widget, content):
        with self._out:
            data = content['args'][0]
            for update in data:
                self._process(update)

    def _process(self, data):
        keys = list(set(data.keys()) - set(("__INDEX__",)))
        out_symbol = keys[0] + str(data['__INDEX__'][0])
        print(out_symbol)

        data = data[keys[0]]
        print(data)

        if out_symbol not in self._nodes:
            self._nodes[out_symbol] = Node(value=data)
        else:
            self._nodes[out_symbol].setValue(data)

        self._graph.children = [self._nodes[out_symbol].dagre()]
