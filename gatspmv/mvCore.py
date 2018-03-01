import os
import random
import numpy
from json import load
from csv import DictWriter
from deap import base, creator, tools

SAMPLE_TSP_TOUR = [77, 64, 76, 134, 62, 102, 49, 32, 24, 22, 23, 118]
instName = 'F-n135-k7'
isCustomize = True

def distanceList(instance, individual):
    # Use the distance matrix and find the distances between all the
    # customers in the TSP tour
    # NOTE: this distance list has depot and first customer, but not the last
    # customer back to depot!
    distance = []
    lastCustomerID = 0
    for customerID in individual:
        distance.append(instance['distance_matrix'][lastCustomerID][customerID])
        lastCustomerID = customerID
    return distance

def demandList(instance, individual):
    # Use the distance matrix and find the demand of all the
    # customers in the TSP tour
    demand = []
    for customerID in individual:
        demand.append(instance['customer_%d' % customerID]['demand'])
    return demand

def culmulativeDistance(instance, individual, startIndex, endIndex):
    # Returns the distance between the start and end index of customers.
    # If the customer is at the beginning or end, includes the depot
    distList = distanceList(instance, individual)
    
    if endIndex < len(individual):
        distance = sum(distList[startIndex:endIndex+1])
    elif endIndex == len(individual):
        distance = sum(distList[startIndex:endIndex+1]) 
        distance += instance['distance_matrix'][individual[endIndex]][0]
    elif endIndex > len(individual):
        distance = 999999999999999999999
    return distance

def culmulativeDemand(instance, individual, startIndex, endIndex):
    # Returns the total demand of the start and end index of customers.
    dmdList = demandList(instance, individual)
    demand = sum(dmdList[startIndex:endIndex+1])
    return demand

def distanceBetweenCustomers(instance, fromCustomer, toCustomer):
    return instance['distance_matrix'][fromCustomer][toCustomer]

def splitLightCustomers(instance, individual, lightRange=100, lightCapacity=35):
    # The method takes in a TSP tour, the light resource's 
    # range and capacity constraint
    # Returns a list indicating customers that the light resource
    # is able to deliver to - [0, 0, 1, 1, 0, 0, 1, 1, 0, 0]
    # The range will include the rendezvous points
    # The capacity does not include the rendezvous points
    considerList = [False] * len(individual) #zero list with length of individual
    clusterList = [0] * len(individual) #zero list with length of individual

    # Determine the order of the distance list
    distList = distanceList(instance, individual)
    s = sorted(distList)
    sortedDistanceList = [s.index(x) for x in distList]

    # Start the cluster with the closest pair and add neighbouring customers until
    # the range or capacity constraint is reached. Then find the next closest pair 
    # not part of any cluster and repeat until all customers are considered
    for i in range(len(individual)):
        considerCustomer = sortedDistanceList.index(i)

        # Determine the neighbouring nodes of the considerCustomer
        if considerCustomer == 0:
            clusterEdgeLocation = [0, considerCustomer+1]
        elif considerCustomer == (len(individual)-1):
            clusterEdgeLocation = [considerCustomer-1, considerCustomer]
        else:  
            clusterEdgeLocation = [considerCustomer-1, considerCustomer+1]

        # Calculate the distance (include rendezvous) and demand of considerCustomer
        distance = culmulativeDistance(instance, individual, clusterEdgeLocation[0], clusterEdgeLocation[1])
        demand = culmulativeDemand(instance, individual, considerCustomer, considerCustomer)

        # First check if the customer is already considered, range feasibility and demand feasibility
        if any(considerList[clusterEdgeLocation[0]:clusterEdgeLocation[1]+1]) == True or distance > lightRange or demand > lightCapacity:
            continue       
        # Passes all tests, initialize considerCustomer as lightCluster
        else:
            considerList[clusterEdgeLocation[0]:clusterEdgeLocation[1]+1] = [True] * (clusterEdgeLocation[1]-clusterEdgeLocation[0]+1)
            clusterList[considerCustomer] = 1

            # Calculate the distance between considerCustomer and end of individual
            if considerCustomer <= len(individual)/2: 
                endList = considerCustomer
            elif considerCustomer > len(individual)/2:
                endList = len(individual) - considerCustomer - 1

            # Incrementally add the neighbouring customers
            # Check range feasibility
            # Check demand feasibility
            for j in range(0, endList):
                distanceForward = culmulativeDistance(instance, individual, clusterEdgeLocation[0], clusterEdgeLocation[1]+1)
                distanceBackward = culmulativeDistance(instance, individual, clusterEdgeLocation[0]-1, clusterEdgeLocation[1])
                demandForward =  culmulativeDemand(instance, individual, clusterEdgeLocation[0]+1, clusterEdgeLocation[1])
                demandBackward = culmulativeDemand(instance, individual, clusterEdgeLocation[0], clusterEdgeLocation[1]-1)

                # Greedy approach: look at the shortest distance neighbouring node to add to cluster
                # If neighbouring node succesfully pass the demand and range constraint
                # Update the cluster list and the consider list
                if distanceForward <= distanceBackward and distanceForward < lightRange and demandForward < lightCapacity:
                    considerList[clusterEdgeLocation[0]+1:clusterEdgeLocation[1]+1] = [True] * (clusterEdgeLocation[1]-clusterEdgeLocation[0])
                    clusterList[clusterEdgeLocation[0]+1:clusterEdgeLocation[1]+1] = [1] * (clusterEdgeLocation[1]-clusterEdgeLocation[0])
                    clusterEdgeLocation[1] = clusterEdgeLocation[1] + 1
                elif distanceForward > distanceBackward and distanceBackward < lightRange and demandBackward < lightCapacity:
                    considerList[clusterEdgeLocation[0]:clusterEdgeLocation[1]] = [True] * (clusterEdgeLocation[1]-clusterEdgeLocation[0])
                    clusterList[clusterEdgeLocation[0]:clusterEdgeLocation[1]] = [1] * (clusterEdgeLocation[1]-clusterEdgeLocation[0])              
                    clusterEdgeLocation[0] = clusterEdgeLocation[0] - 1
                else:
                    break
    return clusterList

def initMVIndividuals(icls, lightList, individual):
    # Custom method to produce individuals for GA
    # individual = [[L], [L], ..., [H]]
    # [L] = [depart, delivery, delivery, ..., rejoin]
    genome = list()
    
    # Find the indicies of where lightList change from 0 to 1
    splitLocation = numpy.where(numpy.roll(lightList,1)!=lightList)[0]

    # Split the individual
    splitList = numpy.split(individual, splitLocation)

    # Flatten a list of odd elements from the splitList
    heavyGenome = ([item for sublist in splitList[0::2] for item in sublist])

    for i in range(2, len(splitList), 2):
        lightGenome = list()
        lightGenome.extend(random.sample(splitList[i-2], 1))
        lightGenome.extend(splitList[i-1])
        lightGenome.extend(random.sample(splitList[i], 1))
        genome.append(lightGenome)
    
    genome.append(heavyGenome)
    return icls(genome)
    
def evalTSPMS(MVindividual, instance, unitCost=1.0, initCost=0, waitCost=0, delayCost=0,
                                    lightUnitCost=1.0, lightInitCost=0, lightWaitCost=0, lightDelayCost=0):
    # Evaluate the cost of a MVIndividual, created by the initMVIndividual method
    # Includes: init cost, travel cost and delay cost of light and heavy resource
    # Expects the MSindividual to be [[L], [L], ..., [H]] format
    route = MVindividual
    totalCost = 0
    lightCost = 0
    heavyCost = 0

    # Dictionary to store the heavy arrival time at this customer
    heavyArrivalTime = dict()
    # Dictionary to store the heavy departure time at this customer
    heavyDepartureTime = dict()
    # Dictionary to store the delay time from the heavy POV at this customer
    # Updated as the light resource are rejoining at this customer
    # Calculated as light resource arrival time - heavy resource departure time
    # If value is positive then heavy resource was waiting
    # If value is negative then light resource was waiting
    resourceDelayTime = dict()

    # Update the heavyArrivalTime and heavyDepartureTime of
    # all heavy resource customers, and calculate the heavy travel cost
    lastCustomerID = 0
    heavyTravelTime = 0
    heavyServiceTime = 0
    heavyTimeCost = 0
    heavyStartTime = 0
    for customerID in route[-1]:
        heavyTravelTime = heavyTravelTime + instance['distance_matrix'][lastCustomerID][customerID]
        heavyServiceTime = heavyServiceTime + instance['customer_%d' % customerID]['service_time']
        heavyStartTime =  heavyStartTime + heavyTravelTime
        heavyFinishedTime = heavyStartTime + heavyServiceTime
        heavyTimeCost = heavyTimeCost + (waitCost * max(instance['customer_%d' % customerID]['ready_time'] - (heavyTravelTime + heavyStartTime), 0) 
                            + delayCost * max((heavyStartTime + heavyTravelTime) - instance['customer_%d' % customerID]['due_time'], 0))
        heavyArrivalTime[str(customerID)] = heavyStartTime
        heavyDepartureTime[str(customerID)] = heavyFinishedTime
    heavyCost = heavyTimeCost + (unitCost * heavyTravelTime)

    # Given the heavyArrivalTime, calculate the light travel time and cost
    # Update the resourceDelayTime accordingly
    for subLightRoute in route[:-1]:
        lightElapsedTime = 0
        lightTimeCost = 0
        lightTravelTime = 0
        lightServiceTime = 0
        lastCustomerID = subLightRoute[0]
        lightStartTime = heavyArrivalTime[str(subLightRoute[0])]
        for customerID in subLightRoute[1:]:
            lightTravelTime = lightTravelTime + instance['distance_matrix'][lastCustomerID][customerID]
            # Consider any delay or waiting time because the light resource is earlier than customer ready time
            # or later than customer due time
            lightTimeCost = lightTimeCost + (lightWaitCost * max(instance['customer_%d' % customerID]['ready_time'] - (lightElapsedTime + lightStartTime), 0) 
                            + lightDelayCost * max((lightStartTime + lightElapsedTime) - instance['customer_%d' % customerID]['due_time'], 0))
            lightServiceTime = lightServiceTime + instance['customer_%d' % customerID]['service_time']
            lightElapsedTime = lightElapsedTime + lightTravelTime + lightServiceTime
            lastCustomerID = customerID
        lightFinishTime = lightStartTime + lightElapsedTime
        lightCost = lightCost + (lightUnitCost * lightElapsedTime) + lightTimeCost
        # update the delayTime for the ending customer of the lightSubRoute
        resourceDelayTime[str(customerID)] = lightFinishTime - heavyDepartureTime[str(customerID)]

    # Calculate the waiting penalty given the resourceDelayTime
    for customerID in resourceDelayTime:
        if resourceDelayTime[customerID] <= 0:
            totalCost = totalCost + (lightWaitCost * resourceDelayTime[customerID])
        else:
            totalCost = totalCost + (waitCost * resourceDelayTime[customerID])
    
    return totalCost

# testing the code
random.seed(64)

# Customize data dir location
jsonDataDir = os.path.join('data', 'json_customize')
jsonFile = os.path.join(jsonDataDir, '%s.json' % instName)
with open(jsonFile) as f:
    instance = load(f)

d = splitLightCustomers(instance, SAMPLE_TSP_TOUR)
print d

testIndividual = [77, 64, 76, 134, 62, 102, 49, 32, 24, 22, 23, 118]

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)
toolbox = base.Toolbox()
toolbox.register('individual', initMVIndividuals, creator.Individual, d, testIndividual)

testIndividual = toolbox.individual()
print testIndividual
cost = evalTSPMS(testIndividual, instance)
print cost

#[13.341664064126334, 0.8, 2.220360331117452, 0.7280109889280518, 8.238931969618392, 
#4.707440918375928, 6.3150613615387785, 5.0990195135927845, 10.890362712049585, 
# 0.28284271247461973, 0.7000000000000011, 17.0484603410396]

# 51.0, 24.0, 28.0, 12.0, 24.0, 54.0, 83.0, 34.0, 36.0, 61.0, 71.0, 36.0

