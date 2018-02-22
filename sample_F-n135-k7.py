# -*- coding: utf-8 -*-
# sample_F-n135-k7.py
# Route #1: 115 114 106 107 108 109 120 
# Route #2: 46 118 18 17 132 131 116 117 119 130 65 19 
# Route #3: 73 74 76 134 77 64 63 79 67 80 33 71 66 
# Route #4: 91 21 25 26 27 28 92 29 94 93 45 43 44 40 3 41 42 2 4 5 6 7 8 9 10 11 12 14 88 15 13 16 90 89 87 86 85 84 83 20 82 
# Route #5: 60 61 54 55 57 105 97 96 38 39 95 37 36 35 99 100 98 104 101 102 50 49 34 32 47 72 
# Route #6: 81 113 129 128 127 121 122 123 125 111 112 126 124 110 69 70 68 133 78 
# Route #7: 22 24 23 59 31 30 58 56 103 53 52 51 62 48 1 75
# Cost 1162

import os
import random
import numpy
from json import load
from csv import DictWriter
from deap import base, creator, tools
from timeit import default_timer as timer #for timer
import multiprocessing
from gavrptw.core import *
from gavrptw.utils import makeDirsForFile, exist

# Global constant for individual size
# Check before running
IND_SIZE = 134

# Create Fitness and Individual Classes
creator.create('FitnessMax', base.Fitness, weights=(1.0,))
creator.create('Individual', list, fitness=creator.FitnessMax)
toolbox = base.Toolbox()

# Attribute generator
toolbox.register('indexes', random.sample, range(1, IND_SIZE + 1), IND_SIZE)
# Structure initializers
toolbox.register('individual', tools.initIterate, creator.Individual, toolbox.indexes)
toolbox.register('population', tools.initRepeat, list, toolbox.individual)

# GA Tools
def gaVRPTW(pop, instName, unitCost, initCost, waitCost, delayCost, indSize, popSize, cxPb, mutPb, NGen, exportCSV=False, customizeData=False):
    if customizeData:
        jsonDataDir = os.path.join('data', 'json_customize')
    else:
        jsonDataDir = os.path.join('data', 'json')
    jsonFile = os.path.join(jsonDataDir, '%s.json' % instName)
    with open(jsonFile) as f:
        instance = load(f)

    # Operator registering
    toolbox.register('evaluate', evalVRPTW, instance=instance, unitCost=unitCost, initCost=initCost, waitCost=waitCost, delayCost=delayCost)
    toolbox.register('select', tools.selRoulette)
    toolbox.register('mate', cxPartialyMatched)
    toolbox.register('mutate', mutInverseIndexes)

    pop=pop

    # Results holders for exporting results to CSV file
    csvData = []
    print 'Start of evolution'
    # Evaluate the entire population
    fitnesses = list(toolbox.map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    # Debug, suppress print()
    # print '  Evaluated %d individuals' % len(pop)
    # Begin the evolution
    for g in range(NGen):
        # print '-- Generation %d --' % g
        # Select the next generation individuals
        # Select elite - the best offspring, keep this past crossover/mutate
        elite = tools.selBest(pop, 1)
        # Keep top 10% of all offspring
        # Roulette select the rest 90% of offsprings
        offspring = tools.selBest(pop, int(numpy.ceil(len(pop)*0.1)))
        offspringRoulette = toolbox.select(pop, int(numpy.floor(len(pop)*0.9))-1)
        offspring.extend(offspringRoulette)
        # Clone the selected individuals
        offspring = list(toolbox.map(toolbox.clone, offspring))
        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < cxPb:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values
        for mutant in offspring:
            if random.random() < mutPb:
                toolbox.mutate(mutant)
                del mutant.fitness.values
        # Evaluate the individuals with an invalid fitness
        invalidInd = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalidInd)
        for ind, fit in zip(invalidInd, fitnesses):
            ind.fitness.values = fit
        # Debug, suppress print()
        # print '  Evaluated %d individuals' % len(invalidInd)
        # The population is entirely replaced by the offspring
        offspring.extend(elite)
        pop[:] = offspring
        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]
        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5
        # Debug, suppress print()
        # print '  Min %s' % min(fits)
        # print '  Max %s' % max(fits)
        # print '  Avg %s' % mean
        # print '  Std %s' % std
        # Write data to holders for exporting results to CSV file
        if exportCSV:
            csvRow = {
                'generation': g,
                'evaluated_individuals': len(invalidInd),
                'min_fitness': min(fits),
                'max_fitness': max(fits),
                'avg_fitness': mean,
                'std_fitness': std,
                'avg_cost': 1 / mean,
            }
            csvData.append(csvRow)
    print '-- End of (successful) evolution --'
    bestInd = tools.selBest(pop, 1)[0]
    print 'Best individual: %s' % bestInd
    print 'Fitness: %s' % bestInd.fitness.values[0]
    printRoute(ind2route(bestInd, instance))
    print 'Total cost: %s' % (1 / bestInd.fitness.values[0])
    if exportCSV:
        csvFilename = '%s_uC%s_iC%s_wC%s_dC%s_iS%s_pS%s_cP%s_mP%s_nG%s.csv' % (instName, unitCost, initCost, waitCost, delayCost, indSize, popSize, cxPb, mutPb, NGen)
        csvPathname = os.path.join('results', csvFilename)
        print 'Write to file: %s' % csvPathname
        makeDirsForFile(pathname=csvPathname)
        if not exist(pathname=csvPathname, overwrite=True):
            with open(csvPathname, 'w') as f:
                fieldnames = ['generation', 'evaluated_individuals', 'min_fitness', 'max_fitness', 'avg_fitness', 'std_fitness', 'avg_cost']
                writer = DictWriter(f, fieldnames=fieldnames, dialect='excel')
                writer.writeheader()
                for csvRow in csvData:
                    writer.writerow(csvRow)


def main():
    random.seed(64)

    instName = 'F-n135-k7'

    unitCost = 1.0
    initCost = 0.0
    waitCost = 0.0
    delayCost = 0.0

    indSize = IND_SIZE
    popSize = 12800
    cxPb = 0.8
    mutPb = 0.1
    NGen = 100

    exportCSV = True
    customizeData = True

    # Global creation of the individuals for GA
    # Initialize the population
    pop = toolbox.population(n=popSize)

    gaVRPTW(
        pop=pop,
        instName=instName,
        unitCost=unitCost,
        initCost=initCost,
        waitCost=waitCost,
        delayCost=delayCost,
        indSize=indSize,
        popSize=popSize,
        cxPb=cxPb,
        mutPb=mutPb,
        NGen=NGen,
        exportCSV=exportCSV,
        customizeData=customizeData
    )

if __name__ == '__main__':
    pool = multiprocessing.Pool()
    toolbox.register('map', pool.map)

    tic = timer()
    main()
    print 'Computing Time: %s' % (timer() - tic)

    pool.close()