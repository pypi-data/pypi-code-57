"""
gmlp.evolution
==============
Your base module for starting your genetic programming.
"""
from __future__ import absolute_import

import configparser
import json
import os
import random
import re
import time
from io import BytesIO, StringIO

from .fitness import *
from .mutations import *
from .selection import *


class Error(Exception):
    pass


class SettingsError(Error):
    """Settings Not Defined!"""
    pass


class Enviroment:
    """
    Used to start your evolutionary neural network.

    :param goal: This is the goal for your evolutionary neural network. If your population is binary your goal should be binary.

    :param crossover_prob: The probability for your organisms to crossover.
    """

    def __init__(self, goal, crossover_prob):
        self.goal = goal
        self.crossover_prob = crossover_prob

    def generate_population(self, genes=None, pop_size=10000, binary=False):
        """
        Generates a population.

        :param genes: The genes per organism.

        :param pop_size: Your population size.

        :param binary: This is if you want your population in a binary form if True.
        """
        self.genes = genes
        self.size = pop_size
        self.binary = binary
        if self.binary == True:
            return [[random.randint(0, 1) for g in range(self.genes)]for n in range(self.size)]

    def crossover(self, population, target):
        """
        The crossover of your population.

        :param population: Your population.

        :param target: Your target.
        """
        self.pop = population
        self.target = target
        for k in range(int(len(self.pop)-2)):
            if random.random() < self.crossover_prob:
                self.parent1 = self.pop.pop(k)
                self.parent2 = self.pop.pop(k+1)
                self.crossover_point = random.randint(0, len(self.target))
                self.child1 = self.pop.insert(
                    k, self.parent1[0:self.crossover_point]+self.parent2[self.crossover_point:])
                self.child2 = self.pop.insert(
                    k+1, self.parent1[0:self.crossover_point]+self.parent2[self.crossover_point:])
        return self.pop

   

# class NeuralNetwork(Connection):
#     """
#     ``THIS FEATURE IS IN DEVELOPMENT!``
#     """
#     def __init__(self, **sett):
#         if sett in "inputs":
#             self.connect('Inputs', sett['inputs'])
        
#         if sett in "hidden":
#             self.connect('Hidden', sett['hidden'])

#         if sett in "output":
#             self.connect('Output', sett['output'])
        


# class Builder:
#     """
#     ``THIS FEATURE IS IN DEVELOPMENT``
#     For help on this module type Builder().help()
#     """
#     def __init__(self, settings=None):
#         self.settings = settings
#         if self.settings != None:
#             self.cfg = configparser.ConfigParser()
#             self.file = self.cfg.read(self.settings)
#             self.sections = self.cfg.sections()
#             for sect in range(len(self.sections)):
#                 if self.sections[sect] == 'NeuralNet':
#                     self.inputs = self.cfg.get(self.sections[sect], 'inputs')
#                     self.outputs = self.cfg.get(self.sections[sect], 'outputs')
#                     self.hidden = self.cfg.get(self.sections[sect], 'hidden')
                    
#                     NeuralNetwork(inputs=self.inputs, outputs=self.outputs, hidden=self.hidden).show()

#     def help(self):
#         self.info = """
#         The builder class is complicated so here's some help with the class.
#         For the settings param you need an .ini file. Heres an example:

#             Settings.ini

#             [NeuralNet]
#             # This is the params for our neural network.
#             inputs = 20
#             hidden = 1
#             output = 2
#             activation = sigmoid

#             [Evolution]
#             # Our evolutionary neural network params
#             pop_size = 10000
#             fittness_function = fit_func()


#         """
#         print(self.info)



        