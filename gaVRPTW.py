# -*- coding: utf-8 -*-

import os
import sys
import json
import random
from deap import base, creator, tools
from basic.common import ROOT_PATH, makeDirsForFile, existFile


def ind2route(individual, instance):
    route = []
    subRoute = []
    vehicleCapacity = instance['vehicle_capacity']
    vehicleLoad = 0
    deportDueTime =  instance['deport']['due_time']
    elapsedTime = 0
    lastCustomerID = 0
    for customerID in individual:
        # Update vehicle load
        demand = instance['customer_%d' % customerID]['demand']
        updatedVehicleLoad = vehicleLoad + demand

        # Update elapsed time
        serviceTime = instance['customer_%d' % customerID]['service_time']
        returnTime = instance['distance_matrix'][customerID][0]
        updatedElapsedTime = elapsedTime + instance['distance_matrix'][lastCustomerID][customerID] + serviceTime + returnTime

        # Validate vehicle load and elapsed time
        if (updatedVehicleLoad <= vehicleCapacity) and (updatedElapsedTime <= deportDueTime):
            # Add to current sub-route
            subRoute.append(customerID)
            vehicleLoad = updatedVehicleLoad
            elapsedTime = updatedElapsedTime - returnTime
        else:
            # Save current sub-route
            route.append(subRoute)
            # Initialize a new sub-route and add to it
            subRoute = [customerID]
            vehicleLoad = demand
            elapsedTime = instance['distance_matrix'][0][customerID] + serviceTime
    if subRoute != []:
        route.append(subRoute)
    return route


def printRoute(route, merge=False):
    routeStr = '0'
    subRouteCount = 0
    for subRoute in route:
        subRouteCount += 1
        subRouteStr = '0'
        for customerID in subRoute:
            subRouteStr = subRouteStr + ' - ' + str(customerID)
            routeStr = routeStr + ' - ' + str(customerID)
        subRouteStr = subRouteStr + ' - 0'
        if not merge:
            print 'Vehicle %d\'s route: %s' % (subRouteCount, subRouteStr)
        routeStr = routeStr + ' - 0'
    if merge:
        print routeStr
    return


def evalVRPTW(individual, instance, unitCost, initCost, waitCost, delayCost):
    timeCost = waitCost * max(instance['customer_%d' % customerID]['ready_time'] - arrivalTime, 0) + delayCost * max(arrivalTime - instance['customer_%d' % customerID]['due_time'], 0)
    fitness = 1.0 / timeCost
    return fitness


def mutReverseIndexes(individual):
    start, stop = sorted(random.sample(range(len(ind)), 2))
    mutant = individual[:start] + individual[stop:start-1:-1] + individual[stop+1:]
    return (mutant, )


def selImprovedRoulette(individuals, k):
    pass
    return selIndividuals


def gaVRPTW(instName, unitCost, initCost, waitCost, delayCost, indSize, popSize, cxPb, mutPb, NGen):
    rootpath = ROOT_PATH
    jsonDataDir = os.path.join(rootpath,'data', 'json')
    jsonFile = os.path.join(jsonDataDir, '%s.js' % instName)
    with open(jsonFile) as f:
        instance = json.load(f)

    creator.create('FitnessMax', base.Fitness, weights=(1.0,))
    creator.create('Individual', list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()

    # Attribute generator
    toolbox.register('indices', random.sample, range(1, indSize + 1), indSize)

    # Structure initializers
    toolbox.register('individual', tools.initIterate, creator.Individual, toolbox.indices)
    toolbox.register('population', tools.initRepeat, list, toolbox.individual)

    # Operator registering
    toolbox.register('evaluate', evalVRPTW)
    toolbox.register('mate', tools.cxPartialyMatched)
    toolbox.register('mutate', mutReverseIndexes)
    toolbox.register('select', selImprovedRoulette)

    pop = toolbox.population(n=popSize)

    print 'Start of evolution'

    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    print '  Evaluated %d individuals' % len(pop)

    # Begin the evolution
    for g in range(NGen):
        print '-- Generation %d --' % g

        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))

        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

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
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        print '  Evaluated %d individuals' % len(invalid_ind)

        # The population is entirely replaced by the offspring
        pop[:] = offspring

        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]

        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5

        print '  Min %s' % min(fits)
        print '  Max %s' % max(fits)
        print '  Avg %s' % mean
        print '  Std %s' % std

    print '-- End of (successful) evolution --'

    best_ind = tools.selBest(pop, 1)[0]
    print 'Best individual is %s, %s' % (best_ind, best_ind.fitness.values)


def main():
    instName = 'R101'

    unitCost = 8.0
    initCost = 60.0
    waitCost = 0.5
    delayCost = 1.5

    indSize = 25
    popSize = 80
    cxPb = 0.85
    mutPb = 0.01
    NGen = 100

    # instName = 'C204'

    # unitCost = 8.0
    # initCost = 100.0
    # waitCost = 1.0
    # delayCost = 1.5

    # indSize = 100
    # popSize = 400
    # cxPb = 0.85
    # mutPb = 0.02
    # NGen = 300

    gaVRPTW(instName, unitCost, initCost, waitCost, delayCost, indSize, popSize, cxPb, mutPb, NGen)


if __name__ == '__main__':
    # main()

    rootpath = ROOT_PATH
    jsonDataDir = os.path.join(rootpath,'data', 'json')

    instName = 'R101'
    jsonFile = os.path.join(jsonDataDir, '%s.js' % instName)
    with open(jsonFile) as f:
        instance = json.load(f)

    individual = range(1,11)
    route = ind2route(individual, instance)
    printRoute(route)