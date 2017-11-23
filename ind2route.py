# -*- coding: utf-8 -*-
# ind2route.py
# Code to run the ind2route function from core
# Also used to test the crossover function PMX

import os
import random
from json import load
from gavrptw.core import ind2routeMS, printRoute, evalVRPMS
from deap import base, creator, tools

instName = 'VRPMS_Data_Small'

random.seed(64)

def cxPartialyMatched(ind1, ind2):
    """Executes a partially matched crossover (PMX) on the input individuals.
    The two individuals are modified in place. This crossover expects
    :term:`sequence` individuals of indices, the result for any other type of
    individuals is unpredictable.
    
    :param ind1: The first individual participating in the crossover.
    :param ind2: The second individual participating in the crossover.
    :returns: A tuple of two individuals.

    Moreover, this crossover generates two children by matching
    pairs of values in a certain range of the two parents and swapping the values
    of those indexes. For more details see [Goldberg1985]_.

    This function uses the :func:`~random.randint` function from the python base
    :mod:`random` module.
    
    .. [Goldberg1985] Goldberg and Lingel, "Alleles, loci, and the traveling
       salesman problem", 1985.
    """

    """
    Author: Paul
    Changes: decrease the index count by 1 to account for the way indivduals are
            generated with 0 being the terminal.

    """
    size = min(len(ind1), len(ind2))
    p1, p2 = [0]*size, [0]*size

    # Initialize the position of each indices in the individuals
    for i in xrange(size):
        p1[ind1[i]-1] = i
        p2[ind2[i]-1] = i
    # Choose crossover points
    #cxpoint1 = random.randint(0, size)
    #cxpoint2 = random.randint(0, size - 1)
    cxpoint1 = 7
    cxpoint2 = 9
    if cxpoint2 >= cxpoint1:
        cxpoint2 += 1
    else: # Swap the two cx points
        cxpoint1, cxpoint2 = cxpoint2, cxpoint1
    
    # Apply crossover between cx points
    for i in xrange(cxpoint1, cxpoint2):
        # Keep track of the selected values
        temp1 = ind1[i]
        temp2 = ind2[i]
        # Swap the matched value
        ind1[i], ind1[p1[temp2-1]] = temp2, temp1
        ind2[i], ind2[p2[temp1-1]] = temp1, temp2
        # Position bookkeeping
        p1[temp1-1], p1[temp2-1] = p1[temp2-1], p1[temp1-1]
        p2[temp1-1], p2[temp2-1] = p2[temp2-1], p2[temp1-1]
    
    return ind1, ind2

# Customize data dir location
jsonDataDir = os.path.join('data', 'json_customize')
jsonFile = os.path.join(jsonDataDir, '%s.json' % instName)
with open(jsonFile) as f:
    instance = load(f)

# Create individuals
creator.create('FitnessMax', base.Fitness, weights=(1.0,))
creator.create('Individual', list, fitness=creator.FitnessMax)

# Initialize values
toolbox = base.Toolbox()
IND_SIZE = 10
# Attribute generator
toolbox.register('indexes', random.sample, range(1, IND_SIZE + 1), IND_SIZE)
# Structure initializers
toolbox.register('individual', tools.initIterate, creator.Individual, toolbox.indexes)
toolbox.register('population', tools.initRepeat, list, toolbox.individual)
toolbox.register('mate', cxPartialyMatched)
toolbox.register('select', tools.selRoulette)
toolbox.register('evaluate', evalVRPMS, instance=instance, unitCost=1.0, initCost=30, lightUnitCost=1, lightInitCost=10)

pop = toolbox.population(n=2)
print(pop)

#individual = toolbox.individual()
# route1 = ind2routeMS(individual, instance)
#evalVRPMS(individual, instance, unitCost=1.0, initCost=30, lightUnitCost=1, lightInitCost=10)

fitnesses = list(map(toolbox.evaluate, pop))
for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
print '  Evaluated %d individuals' % len(pop)

offspring = pop

for child1, child2 in zip(offspring[::2], offspring[1::2]):
            toolbox.mate(child1, child2)

print(offspring)
