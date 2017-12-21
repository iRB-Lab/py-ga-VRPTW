# -*- coding: utf-8 -*-
# testEvalVRP.py
# Code to test the EvalVRP method to make sure the optmial individual
# returns the correct cost
# The optimal individual of A-n32-k5 is:
# Route 1: [0 - 21- 31 - 19 - 17 - 13 - 7 - 26 - 0]
# Route 2: [0 - 12 - 1 - 16 - 30 - 0]
# Route 3: [0 - 27 - 24 - 0]
# Route 4: [0 - 29 - 18 - 8 - 9 - 22 - 15 - 10 - 25 - 5 - 20 - 0]
# Route 5: [0 - 14 - 28 - 11 - 4 - 23 - 3 - 2 - 6 - 0]

import os
import random
from json import load
from gavrptw.core import ind2route, printRoute, evalVRPTW
from deap import base, creator, tools

instName = 'A-n32-k5'

random.seed(64)

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
IND_SIZE = 31
# Attribute generator
toolbox.register('indexes', random.sample, range(1, IND_SIZE + 1), IND_SIZE)
# Structure initializers
toolbox.register('individual', tools.initIterate, creator.Individual, toolbox.indexes)
toolbox.register('population', tools.initRepeat, list, toolbox.individual)
toolbox.register('select', tools.selRoulette)
toolbox.register('evaluate', evalVRPTW, instance=instance, unitCost=1.0, initCost=0)

individual = [21, 31, 19, 17, 13, 7, 26, 12, 1, 16, 30, 27, 24, 29, 18, 8, 9, 22, 15, 10, 25, 5, 20, 
                14, 28, 11, 4, 23, 3, 2, 6]

route = ind2route(individual, instance)
printRoute(route)

# Due to the way EvalVRP is written, a vehicle needs to exceed max capacity before
# starting a new vehicle. The optimal route leaves certain vehicles below capacity
# and therefore gives even more optimal (smaller) costs

# TODO: maybe a 2 step optmization is needed