# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 17:43:16 2016

@author: xeNon
"""

import sys
import random
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing

from deap import base, creator, tools
#from scoop import futures
from timeit import default_timer as timer

# Create Fitness and Individual Classes
creator.create('FitnessMin', base.Fitness, weights=(-1.0,)) # Weights must be a sequence
creator.create('Individual', list, fitness=creator.FitnessMin)

# Create Individual Type
IND_SIZE = 2

toolbox = base.Toolbox()
def rand():
    return random.uniform(-3,3)
    
toolbox.register('attr_float', rand)
toolbox.register('individual', tools.initRepeat, creator.Individual,
                 toolbox.attr_float, n=IND_SIZE)
                
# Create Population Type
toolbox.register('population', tools.initRepeat, list, toolbox.individual)

# Define evaluation Function
def evaluate(individual):
    """Fitness evaluation. Must return a tuple even for single objective optimization.
    """
    x = (individual[0])
    y = (individual[1])
    
    # Do some heavy stuff
    n = 1873895732
    import math
    for i in range(10000000):
        math.sqrt(n)
        i = i + 1

    print 'Done!'
    sys.stdout.flush() 
    return (rosenbrock(x,y),) # Must be an iterable
    
def rosenbrock(x,y):
    return (1-x)**2 + 100*(y-x**2)**2
    
# Define Operators
toolbox.register('mate', tools.cxTwoPoint)
toolbox.register('mutate', tools.mutGaussian, mu = 0, sigma = 1, indpb = 0.1)
toolbox.register('select', tools.selTournament, tournsize=3)
toolbox.register('evaluate', evaluate)
#toolbox.register('map', futures.map) # SHELL: python -m scoop file.py

# Optimization Algorithm
def main():
    """Defines the optimization process. Should be contained in the main function.
    """
    
    # General Settings
    POP_SIZE = 20   # Population size
    NGEN = 1        # Number of generations
    CXPB = 0.2      # Crossover probability
    MUTPB = 0.5     # Mutation probablilty
    
    # Initialize population
    pop = toolbox.population(n=POP_SIZE)
    
    # Evaluate the entire initial population
    jobs = toolbox.map(toolbox.evaluate, pop)
    fitnesses = jobs.get()
    print('Done initial population evaluation.')
    # Assign the fitnesses
    for ind, fit in zip(pop,fitnesses):
        ind.fitness.values = fit
        
    # Evolutionary Loop
    for g in range(NGEN):
        # Select the next generations individuals (len(pop) individuals)
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = map(toolbox.clone, offspring)
        
        # Apply crossover on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):  # Chooses offspring with neighbouring indices to mutate
            if random.random() < CXPB: 
                # Do crossover inplace
                toolbox.mate(child1, child2)
                # Request reevaluation of fitnesses
                del child1.fitness.values
                del child2.fitness.values
                
        # Apply mutation on the offspring
        for mutant in offspring:
            if random.random() < MUTPB:
                # Do mutation inplace
                toolbox.mutate(mutant)
                # Request reevaluation of fitness
                del mutant.fitness.values
                
        # Evaluate fitnesses of individuales with invalid fitnesses
                invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
                jobs = toolbox.map(toolbox.evaluate, invalid_ind)
                fitnesses = jobs.get()
                for ind, fit in zip(invalid_ind, fitnesses):
                    ind.fitness.values = fit
                    
        # Replace the population by the offspring
        pop[:] = offspring
    
    return pop

if __name__ == '__main__':
    
    pool = multiprocessing.Pool(processes=4)
    toolbox.register('map', pool.map_async)
    
    tic = timer()
    pop = main()
    pool.close()
    print timer()-tic