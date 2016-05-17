# -*- coding: utf-8 -*-

import os
import sys
import json
import random
from deap import base, creator, tools
from basic.common import ROOT_PATH, makeDirsForFile, existFile


def evalVRPSTW(ind, inst):
    pass
    return fitness


def mutReverseIndexes(ind):
    start, stop = sorted(random.sample(range(len(ind)), 2))
    mutant = ind[:start] + ind[stop:start-1:-1] + ind[stop+1:]
    return (mutant, )


def ind2route(ind):
    pass
    return route


def gaVRPSTW(InstName, unitCost, initCost, waitCost, delayCost, IndSize, PopSize, CxPb, MutPb, NGen):
    rootpath = ROOT_PATH
    jsonDataDir = os.path.join(rootpath,'data', 'json')
    jsonFile = os.path.join(jsonDataDir, '%s.js' % InstName)
    with open(jsonFile) as f:
        instance = json.load(f)

    creator.create('FitnessMax', base.Fitness, weights=(1.0,))
    creator.create('Individual', list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()

    # Attribute generator
    toolbox.register('indices', random.sample, range(1, IndSize + 1), IndSize)

    # Structure initializers
    toolbox.register('individual', tools.initIterate, creator.Individual, toolbox.indices)
    toolbox.register('population', tools.initRepeat, list, toolbox.individual)

    # Operator registering
    toolbox.register('evaluate', evalVRPSTW)
    toolbox.register('mate', tools.cxPartialyMatched)
    toolbox.register('mutate', mutReverseIndexes)
    toolbox.register('select', tools.selRoulette)

    pop = toolbox.population(n=PopSize)


def main():
    InstName = 'R101'

    unitCost = 8.0
    initCost = 60.0
    waitCost = 0.5
    delayCost = 1.5

    IndSize = 25
    PopSize = 80
    CxPb = 0.85
    MutPb = 0.01
    NGen = 100

    # InstName = 'C204'

    # unitCost = 8.0
    # initCost = 100.0
    # waitCost = 1.0
    # delayCost = 1.5

    # IndSize = 100
    # PopSize = 400
    # CxPb = 0.85
    # MutPb = 0.02
    # NGen = 300

    gaVRPSTW(InstName, unitCost, initCost, waitCost, delayCost, IndSize, PopSize, CxPb, MutPb, NGen)

if __name__ == '__main__':
    main()