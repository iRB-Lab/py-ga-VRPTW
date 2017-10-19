# -*- coding: utf-8 -*-
# ind2route.py
# Code to run the ind2route function from core

import os
import random
from json import load
from gavrptw.core import ind2route, printRoute, evalVRPTW
from deap import base, creator, tools

instName = 'VRPMS_Data_Small'

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

individual = toolbox.individual()
route = ind2route(individual, instance)
printRoute(route, twoResources=True)
evalVRPTW(individual, instance, unitCost=1.0, initCost=30, lightUnitCost=1, lightInitCost=10)
