# -*- coding: utf-8 -*-
# The VRPMS portion of P-n10-x instances

import os
import random
import numpy
from json import load
from csv import DictWriter
from deap import base, creator, tools
from timeit import default_timer as timer #for timer

# GA Tools
def gaTSPMV(instName, tsp, unitCost, waitCost, delayCost, speed, indSize, popSize, 
                            lightUnitCost, lightWaitCost, lightDelayCost, lightSpeed,
                            lightRange, lightCapacity,
                            cxPb, mutPb, NGen, exportCSV=False, customizeData=False):
    if customizeData:
        jsonDataDir = os.path.join('data', 'json_customize')
    else:
        jsonDataDir = os.path.join('data', 'json')
    jsonFile = os.path.join(jsonDataDir, '%s.json' % instName)
    with open(jsonFile) as f:
        instance = load(f)

    # Create Fitness and Individual Classes
    creator.create('FitnessMax', base.Fitness, weights=(1.0,))
    creator.create('Individual', list, fitness=creator.FitnessMax)
    toolbox = base.Toolbox()
    print "tsp at the moment is:" 
    print tsp
    splitLightList = mvcore.splitLightCustomers(instance, tsp, lightRange=lightRange, lightCapacity=lightCapacity)
    toolbox.register('individual', mvcore.initMVIndividuals, creator.Individual, splitLightList, tsp)
    toolbox.register('population', tools.initRepeat, list, toolbox.individual)

    pop = toolbox.population(n=popSize)

    # Operator registering
    toolbox.register('evaluate', mvcore.evalTSPMS, instance=instance, unitCost=unitCost, waitCost=waitCost, delayCost=delayCost, speed=speed,
                                                    lightUnitCost=lightUnitCost, lightWaitCost=lightWaitCost, lightDelayCost=lightDelayCost, lightSpeed=lightSpeed)
    toolbox.register('select', tools.selRoulette)
    toolbox.register('mate', mvcore.cxSinglePointSwap)
    toolbox.register('mutate', core.mutInverseIndexes)

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

    print 'Total cost: %s' % (1 / bestInd.fitness.values[0])
    if exportCSV:
        csvFilename = '%s-VRPMS_uC%s_wC%s_dC%s_sP%s_luC%s_lwC%s_ldC%s_lsP%s_iS%s_pS%s_cP%s_mP%s_nG%s.csv' % (instName, unitCost, waitCost, delayCost, speed,
                                                                                          lightUnitCost, lightWaitCost, lightDelayCost, lightSpeed,
                                                                                          indSize, popSize, cxPb, mutPb, NGen)
        csvPathname = os.path.join('results', csvFilename)
        print 'Write to file: %s' % csvPathname
        utils.makeDirsForFile(pathname=csvPathname)
        if not utils.exist(pathname=csvPathname, overwrite=True):
            with open(csvPathname, 'w') as f:
                fieldnames = ['generation', 'evaluated_individuals', 'min_fitness', 'max_fitness', 'avg_fitness', 'std_fitness', 'avg_cost']
                writer = DictWriter(f, fieldnames=fieldnames, dialect='excel')
                writer.writeheader()
                for csvRow in csvData:
                    writer.writerow(csvRow)
    return bestInd, bestInd.fitness.values[0]

def main():
    random.seed(73)

    instName = 'P-n100-0'

    unitCost = 0.1
    waitCost = 0.05
    delayCost = 0.01
    speed = 5
    lightUnitCost = 0.02
    lightWaitCost = 0.0
    lightDelayCost = 0.01
    lightSpeed = 1
    lightRange = 200
    lightCapacity = 10

    popSize = 500
    cxPb = 0.9
    mutPb = 0
    NGen = 200

    exportCSV = True
    customizeData = True

    # This should be the outcome of running the gavrptw module
    bestVRP = [[53, 23, 65, 7, 14, 51, 45, 74, 61, 30, 76, 82, 19, 6, 73, 80, 10, 91, 68, 26, 48, 38, 100, 36, 37, 86, 57, 69, 3, 67, 64, 17, 62, 59, 39, 40, 1, 95, 44, 94], [22, 70, 52, 20, 56, 50, 85, 32, 49, 87, 97, 92, 21, 11, 2, 15, 88, 58, 46, 16, 66, 29, 31, 63, 41, 34, 27, 25, 79, 55, 24, 77, 84, 81, 18, 33, 9, 83, 12, 99, 35], [90, 8, 43, 54, 47, 4, 89, 5, 42, 75, 93, 13, 28, 98, 71, 60, 78, 72, 96]]
    bestVRPMV = []
    bestVRPMVCost = 0

    for tsp in bestVRP:
        indSize = len(tsp)
        bestSubTSP, bestSubTSPFitness = gaTSPMV(
            instName=instName,
            tsp=tsp,
            unitCost=unitCost,
            waitCost=waitCost,
            delayCost=delayCost,
            speed=speed,
            lightUnitCost=lightUnitCost,
            lightWaitCost=lightWaitCost,
            lightDelayCost=lightDelayCost,
            lightSpeed=lightSpeed,
            lightRange=lightRange,
            lightCapacity=lightCapacity,
            indSize=indSize,
            popSize=popSize,
            cxPb=cxPb,
            mutPb=mutPb,
            NGen=NGen,
            exportCSV=exportCSV,
            customizeData=customizeData
        )
        bestVRPMV.append(bestSubTSP)
        bestVRPMVCost = bestVRPMVCost + 1/bestSubTSPFitness
        print "Best VRPMS Cost is: %f" % bestVRPMVCost
        print bestVRPMV
    return

if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
        from gatspmv import mvcore
        from gavrptw import core, utils 
    else:
        from ..gatspmv import mvcore
        from ..gavrptw import core, utils 
    tic = timer()
    main()
    print 'Computing Time: %s' % (timer() - tic)