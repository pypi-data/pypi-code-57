import CADETMatch.util as util
import CADETMatch.pareto as pareto

from deap import creator
from deap import tools
from deap import base
import array

meta_hof = pareto.ParetoFront(similar=pareto.similar, similar_fit=pareto.similar_fit_meta(cache),
                                          slice_object=cache.meta_slice)

creator.create("FitnessMaxMeta", base.Fitness, weights=[1.0, 1.0, 1.0, -1.0, -1.0])
creator.create("IndividualMeta", array.array, typecode="d", fitness=creator.FitnessMaxMeta, strategy=None,
                   csv_line=None)

toolbox = base.Toolbox()

def initIndividual(icls, content):
    return icls(content)

toolbox.register("individualMeta", initIndividual, creator.IndividualMeta)

ind_meta = toolbox.individualMeta([5.71E-07,	0.325681352])
ind_meta.fitness.values = [-0.297037238, -0.297037238, -0.297037238, 0.297037238]


new = meta_hof.update([ind_meta])

ind_meta = toolbox.individualMeta([5.73E-07,	0.325681352])
ind_meta.fitness.values = [-0.296955155, -0.296955155, -0.296955155, -0.296955155]

new = meta_hof.update([ind_meta])

a = None