"""
gmlp.mutations
==============
Used for mutating your population. 
\n``More mutations are to come in future versions.``
"""
from __future__ import absolute_import

import random


def ValueEncodingMut(population, mutation_prob):
    """
    Value Encoding Mutation.

    :param population: the population you will be mutating. The have genes like this -> [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    :param mutation_prob: the mutation probability usually .15 but you'll have to see what's best for you.
    """
    for pop in range(len(population)):
        if random.random() < mutation_prob:
            random_population_org = random.randint(0, len(population)-1)
            popped_org = population.pop(random_population_org)
            for c in range(len(popped_org)):
                if random.random() < .5:
                    popped_org[c] += 1
                else:
                    popped_org[c] -= 1
            population.insert(random_population_org, popped_org)
    return population


def ShuffleMut(population, mutation_prob):
    """
    Shuffle mutation.

    :param population: Your selected population you wish to mutate.

    :param mutation_prob: The probability that your organisms will mutate.
    """
    if not population == list(population):
        population = list(population)
    for pop in range(len(population)):
        if random.random() < mutation_prob:
            rand_pop_place = random.randint(0, len(population)-1)
            random.shuffle(population[rand_pop_place])
    return population


def BinaryInvertMut(population, mutation_prob):
    """
    Inverts your binary population.

    :param population: Your selected population you wish to mutate.

    :param mutation_prob: The probability that your organisms will mutate.
    """
    for n in range(len(population)):
        if random.random() < mutation_prob:
            rand = random.randint(0, len(population)-1)
            if population[rand] == 0:
                population[rand] = 1
            else:
                population[rand] = 0
    return population
