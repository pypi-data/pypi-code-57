# SPDX-FileCopyrightText: 2019 Vincent Lequertier <vi.le@autistici.org>
# SPDX-License-Identifier: GPL-3.0-or-later

from itertools import tee
import string
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import networkx as nx
import matplotlib.pyplot as plt
import multiprocessing as mp
import typing


class GraphOfWords:
    """
    Represent a graph of words object

    Args:
        window_size (int): The size of window
        language (str, optional): The language of the text
    """

    def __init__(self, window_size=10, language="english"):

        self.window_size = window_size
        self.stops = stopwords.words(language) + list(string.punctuation)
        self.graph = nx.DiGraph()

    def __window(self, iterable: typing.Iterable) -> typing.Iterable:
        """
        Create a sliding window

        Args:
            iterable (Iterbale): Predicted values

        Returns:
            typing.Iterable: The windows
        """

        iters = tee(iterable, self.window_size)
        for i in range(1, self.window_size):
            for each in iters[i:]:
                next(each, None)
        return list(zip(*iters))

    def analyse_sentence(self, sentence: str) -> list:
        """
        Treat a single sentence with a sliding window connecting words in a
        graph Return a list of edges insteads, then the graph will be created
        from this graph

        Args:
            sentence (str): The sentence to process

        Returns:
            list: The graph edges.

        """
        edges = []
        seen_words = []
        if self.remove_stopwords is True:
            # Strip stop words and punctuation marks
            words = [w for w in word_tokenize(sentence.lower()) if w not in self.stops]
        else:
            words = word_tokenize(sentence.lower())
        word_windows = self.__window(words)

        # Slide a window across the sentence
        for idx_word_window, word_window in enumerate(word_windows, start=0):
            for idx, outer_word in enumerate(word_window):
                for idx_inner, inner_word in enumerate(word_window[idx + 1 :], start=2):
                    word_id = "{0}_{1}_{2}".format(
                        outer_word, inner_word, (idx_inner + idx_word_window + idx)
                    )
                    if word_id not in seen_words:
                        edges.append(
                            (outer_word, inner_word, self.window_size - idx_inner + 2)
                        )
                        seen_words.append(word_id)
        return edges

    def build_graph(self, text: str, remove_stopwords: bool = True, workers: int = 4):
        """
        Build the graph itself

        Args:
            text (str): The text to create the graph on, or a list of sentences
            remove_stopwords (bool, optional): Whether the stopwords should be removed or not
            workers (int, optional): Number of cores to use
        """

        if isinstance(text, str):
            sentences = sent_tokenize(text)
        elif isinstance(text, list):
            sentences = text
        else:
            raise ValueError

        self.remove_stopwords = remove_stopwords

        pool = mp.Pool(processes=workers)
        edges = pool.map(self.analyse_sentence, sentences)
        pool.close()
        pool.join()
        edges = [edge for sublist in edges for edge in sublist]
        self.graph.add_weighted_edges_from(edges)

    def display_graph(self):
        """
        Create a graph plot and display it
        """

        dmin = 1
        ncenter = 0
        pos = nx.spring_layout(self.graph)
        max_neighbors = 0

        for n in pos:
            n_neighbors = len(list(self.graph.neighbors(n)))
            x, y = pos[n]
            d = (x - 0.5) ** 2 + (y - 0.5) ** 2
            if d < dmin:
                dmin = d
            if max_neighbors < n_neighbors:
                ncenter = n
                max_neighbors = n_neighbors

        p = dict(nx.single_source_shortest_path_length(self.graph, ncenter))
        weights = [
            int(self.graph[u][v]["weight"] / self.window_size)
            for u, v in self.graph.edges()
        ]
        nx.draw(self.graph, pos, width=weights, font_size=14, with_labels=False)
        nx.draw_networkx_edges(self.graph, pos, nodelist=[ncenter], alpha=0.4)
        # Cmap defines the color scale
        nx.draw_networkx_nodes(
            self.graph,
            pos,
            nodelist=list(p.keys()),
            node_color=list(p.values()),
            cmap=plt.cm.Reds_r,
        )

        # Put labels on the top of each node by increasing y abscise
        for p in pos:
            pos[p][1] += 0.04
        nx.draw_networkx_labels(self.graph, pos)
        plt.axis("off")
        plt.show()

    def write_graph_edges(self, filename: str):
        """
        Write the edge list to a file

        Args:
            filename (str): The path to the file
        """
        nx.write_weighted_edgelist(self.graph, filename, "utf-8")
