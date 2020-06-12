"""
GMLP.selection
"""
from __future__ import absolute_import

import random


def tournament_selection(population, scores, tournament_size):
    """
    Selects the fittest.

    :param population: This is your population param to be selected from.

    :param scores: Each of your population's fitness.

    :param tournament_size: How much organisms you want to select for each iteration.
    """
    population = population
    scores = scores
    tournament_size = tournament_size
    fittest = []
    for fit in range(0, len(population)):
        random_org = random.randint(0, len(scores)-1)
        prev_score = scores[random_org]
        prev_pop = population[random_org]
        for t in range(0, tournament_size):
            fighters = random.randint(0, len(scores)-1)
            if scores[fighters] < prev_score:
                prev_score = scores[fighters]
                prev_pop = population[fighters]
        fittest.append(prev_pop)
    return fittest
