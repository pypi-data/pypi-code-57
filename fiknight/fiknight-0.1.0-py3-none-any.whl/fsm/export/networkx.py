#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Copyright (C) 2020  Trijeet Sethi
#This project is written under the GPL license. For the full GPL license, please see the base directory COPYING file or visit <https://www.gnu.org/licenses/>.

##Std Lib Imports:
import itertools

##Internal Imports:
from fiknight.fsm.core import *

##External Imports:
import networkx as nx
import matplotlib.pyplot as plt

def extractTransitions(machine: object) -> object:
    '''
    Function to access strictly the transitions of a machine.

    returns:
    a list of every transition in tuple form.

    '''

    ##Extraction:
    transition_list = []
    for i in machine.state_stack:
        for val in i.transitions.next_states.values():
            transition_list.append((i.name, val.name))

    return transition_list

def getGraph(machine: object, filepath: str) -> int:
    '''
    Function that wraps connectivity to graph drawing.
    Depends on: networkx and matplotlib

    output:
    png of diagram at designated filepath.
    '''

    DG = toNetworkx(machine)
    pos=nx.circular_layout(DG)
    pos_higher = {}
    y_off = 0.05
    x_off = 0.05
    labels = {i:i for i in DG.nodes}

    for k, v in pos.items():
        pos_higher[k] = (v[0]-x_off, v[1]+y_off)

    try:
        nx.draw(DG,
            pos=pos,
            node_color="#FF7F50",
            node_shape='d',
            node_size=100,
            edge_color="#4682B4",
            with_labels=True,
            )
        # nx.draw_networkx_labels(G=DG, labels = labels, pos = pos_higher, font_size = 10, with_labels = True)
        plt.title('State Machine Diagram')
        plt.savefig(filepath)
    except Exception as e:
        print(e)
        return -1
    return 0


def toNetworkx(machine: object) -> object:
    '''
    Function to build a networkx graph from the state machine.

    returns:
    a networkx graph object
    '''

    ##Walk through the machine's states to grab nodes and transitions:
    nodes = [state.name for state in machine.state_stack]
    transitions = extractTransitions(machine)
    edges = [item for sublist in transitions for item in transitions]

    DG = nx.DiGraph()
    DG.add_nodes_from(nodes)
    DG.add_edges_from(edges)
    print(f"Created a network with {DG.number_of_nodes()} and {DG.number_of_edges()} edges.")

    return DG
