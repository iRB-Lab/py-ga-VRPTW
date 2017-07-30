[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)][repository]
[![Python](https://img.shields.io/badge/Python-2.7-blue.svg)][python]
[![Release](https://img.shields.io/github/release/iROCKBUNNY/py-ga-VRPTW.svg)][release]
[![License](https://img.shields.io/github/license/iROCKBUNNY/py-ga-VRPTW.svg)][license]
[![Watchers](https://img.shields.io/github/watchers/iROCKBUNNY/py-ga-VRPTW.svg?style=social&label=Watch)][watch]
[![Stargazers](https://img.shields.io/github/stars/iROCKBUNNY/py-ga-VRPTW.svg?style=social&label=Star)][star]
[![Forks](https://img.shields.io/github/forks/iROCKBUNNY/py-ga-VRPTW.svg?style=social&label=Fork)][fork]

# py-ga-VRPTW
A Python Implementation of a Genetic Algorithm-based Solution to Vehicle Routing Problem with Time Windows (VRPTW)

## Contents
- [Installation](#installation)
    - [Requirements](#requirements)
    - [Installing with Virtualenv](#installing-with-virtualenv)
    - [Python 3 Support](#python-3-support)
- [Quick Start](#quick-start)
- [Problem Sets](#problem-sets)
    - [Solomon's VRPTW Benchmark Problems](#solomons-vrptw-benchmark-problems1)
    - [Instance Definitions](#instance-definitions)
        - [Text File Format](#text-file-format)
        - [JSON Format](#json-format) 
        - [Use Cusomized Instance Data](#use-cusomized-instance-data)
            - [Supported File Format](#supported-file-format)
            - [Directory Set-up](#directory-set-up)
            - [Convert `*.txt` to `*.json`](#convert-txt-to-json)
            - [GA Set-up](#ga-set-up)
- [GA Implementation](#ga-implementation)
    - [Individual (Chromosome)](#individual-chromosome)
        - [Individual Coding](#individual-coding)
        - [Individual Decoding](#individual-decoding)
        - [Print Route](#print-route)
    - [Evaluation](#evaluation)
    - [Selection: Roulette Wheel Selection](#selection-roulette-wheel-selection)
    - [Crossover: Partially Matched Crossover](#crossover-partially-matched-crossover)
    - [Mutation: Inverse Operation](#mutation-inverse-operation)
    - [Algorithm](#algorithm)
    - [Sample Codes](#sample-codes)
        - [Instance: R101](#instance-r101)
        - [Instance: C204](#instance-c204)
        - [Customized Instance](#customized-instance)
        - [View Logs](#view-logs)
- [API Reference](#api-reference)
    - [Module: `gavrptw`](#module-gavrptw)
    - [Module: `gavrptw.core`](#module-gavrptwcore)
    - [Module: `gavrptw.utils`](#module-gavrptwutils)
- [File Structure](#file-structure)
- [Further Reading](#further-reading)
- [References](#references)
- [License](#license)

## Installation
### Requirements
- [macOS][macos] (Recommended)
- [Python 2.7][python]
- [Pip][pip]
- [Virtualenv][virtualenv]

### Installing with Virtualenv
On Unix, Linux, BSD, macOS, and Cygwin:

```sh
git clone https://github.com/iROCKBUNNY/py-ga-VRPTW.git
cd py-ga-VRPTW
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Python 3 Support
See **[@yingriyanlong][yingriyanlong-github]**'s fork: [yingriyanlong/py-ga-VRPTW][yingriyanlong-verison].

## Quick Start
See [sample codes](#sample-codes).

## Problem Sets
### Solomon's VRPTW Benchmark Problems<sup>[1][solomon]</sup>
|Problem Set|Random|Clustered|Random & Clustered|
|:--|:--|:--|:--|
|Short Scheduling Horizon|R1-type|C1-type|RC1-type|
|Long Scheduling Horizon|R2-type|C2-type|RC2-type|

**Remarks:**

1. Solomon generated six sets of problems. Their design highlights several factors that affect the behavior of routing and scheduling algorithms. They are:
    - geographical data;
    - the number of customers serviced by a vehicle;
    - percent of time-constrained customers; and
    - tightness and positioning of the time windows.
2. The geographical data are randomly generated in problem sets R1 and R2, clustered in problem sets C1 and C2, and a mix of random and clustered structures in problem sets by RC1 and RC2.
3. Problem sets R1, C1 and RC1 have a short scheduling horizon and allow only a few customers per route (approximately 5 to 10). In contrast, the sets R2, C2 and RC2 have a long scheduling horizon permitting many customers (more than 30) to be serviced by the same vehicle.
3. The customer coordinates are identical for all problems within one type (i.e., R, C and RC).
4. The problems differ with respect to the width of the time windows. Some have very tight time windows, while others have time windows which are hardly constraining. In terms of time window density, that is, the percentage of customers with time windows, I created problems with 25, 50, 75 and 100% time windows.
4. The larger problems are 100 customer euclidean problems where travel times equal the corresponding distances. For each such problem, smaller problems have been created by considering only the first 25 or 50 customers.

### Instance Definitions
See [Solomon's website][solomon].

#### Text File Format
The text files corresponding to the problem instances can be found under the `data/text/` directory. Each text file is named with respect to its corresponding instance name, e.g.: the text file corresponding to problem instance **C101** is `C101.txt`, and locates at `data/text/C101.txt`.

Below is a description of the format of the text file that defines each problem instance (assuming 100 customers).

```
<Instance name>
<empty line>
VEHICLE
NUMBER     CAPACITY
  K           Q
<empty line>
CUSTOMER
CUST NO.  XCOORD.   YCOORD.    DEMAND   READY TIME  DUE DATE   SERVICE TIME
<empty line>
    0       x0        y1         q0         e0          l0            s0
    1       x1        y2         q1         e1          l1            s1
  ...      ...       ...        ...        ...         ...           ...
  100     x100      y100       q100       e100        l100          s100
```

**Remarks:**

1. All constants are integers.
2. `CUST NO.` 0 denotes the depot, where all vehicles must start and finish.
3. `K` is the maximum number of vehicles.
4. `Q` the capacity of each vehicle.
5. `READY TIME` is the earliest time at which service may start at the given customer/depot.
6. `DUE DATE` is the latest time at which service may start at the given customer/depot.
7. The value of time is equal to the value of distance.
8. As a backup, you can download a zip-file with the 100 customers instance definitions<sup>[2][100-customers]</sup> [here][100-customers-zip].

#### JSON Format
For the further convenience, a Python script named `text2json.py` is writen to convert problem instances from the **text file format** to **JSON format** and stored under the `data/json/` directory. Like the text files, each JSON file is named with respect to its corresponding instance name, e.g.: the JSON file corresponding to problem instance **C101** is `C101.json`, and locates at `data/json/C101.json`.

Below is a description of the format of the JSON file that defines each problem instance (assuming 100 customers).

```js
{
    "instance_name" : "<Instance name>",
    "max_vehicle_number" : K,
    "vehicle_capacity" : Q,
    "deport" : {
        "coordinates" : {
            "x" : x0,
            "y" : y0
        },
        "demand" : q0,
        "ready_time" : e0,
        "due_time" : l0,
        "service_time" : s0
    },
    "customer_1" : {
        "coordinates" : {
            "x" : x1,
            "y" : y2
        },
        "demand" : q1,
        "ready_time" : e1,
        "due_time" : l1,
        "service_time" : s1
    },
    ...
    "customer_100" : {
        "coordinates" : {
            "x" : x100,
            "y" : y100
        },
        "demand" : q100,
        "ready_time" : e100,
        "due_time" : l100,
        "service_time" : s100
    },
    "distance_matrix" : [
        [dist0_0, dist0_1, ..., dist0_100],
        [dist1_0, dist1_1, ..., dist1_100],
        ...
        [dist100_0, dist100_1, ..., dist0_0]
    ]
}
```

**Remarks:**

1. `dist1_1` denotes the distance between Customer 1 and Customer 1, which should be 0, obviously.
2. To obtain the distance value between Customer 1 and Customer 2 in Python can be done by using `<jsonData>['distance_matrix'][1][2]`, where `<jsonData>` denotes the name of a Python `dict` object.

#### Use Cusomized Instance Data
You can customize your own problem instances.

##### Supported File Format
The customized problem instance data file should be either **text file format** or **JSON format**, exactly the same as the above given examples.

##### Directory Set-up
Customized `*.txt` files should be put under the `data\text_customize\` directory and customized `*.json` files should be put under the `data\json_customize\` directory.

##### Convert `*.txt` to `*.json`
Run the `text2json.py` script to convert `*.txt` file to `*.json` file.

```python
# -*- coding: utf-8 -*-
# text2json_customize.py

from gavrptw.utils import text2json


def main():
    text2json(customize=True)


if __name__ == '__main__':
    main()
```

##### GA Set-up
The `customizeData` flag of the `gaVRPTW()` method should be set to `True`. For further understanding, please refer to the sample codes section at the end of this document.

## GA Implementation
### Individual (Chromosome)
#### Individual Coding
All visited customers of a route (including several sub-routes) are coded into an `individual` in turn. For example, the following route

```
Sub-route 1: 0 - 5 - 3 - 2 - 0
Sub-route 2: 0 - 7 - 1 - 6 - 9 - 0
Sub-route 3: 0 - 8 - 4 - 0
```
are coded as `5 3 2 7 1 6 9 8 4`, which can be stored in a Python `list` object, i.e., `[5, 3, 2, 7, 1, 6, 9, 8, 4]`.

#### Individual Decoding
```python
ind2route(individual, instance)
```
decodes `individual` to `route` representation. To show the difference between an `individual` and a `route`, an example is given below.

```python
# individual
[5, 3, 2, 7, 1, 6, 9, 8, 4]

# route
[[5, 3, 2], [7, 1, 6, 9], [8, 4]]
```

**Parameters:**

- `individual` – An individual to be decoded.
- `instance` – A problem instance `dict` object, which can be loaded from a JSON format file.

**Returns:**

- A list of decoded sub-routes corresponding to the input individual.

**Definition:**

```python
def ind2route(individual, instance):
    route = []
    vehicleCapacity = instance['vehicle_capacity']
    deportDueTime =  instance['deport']['due_time']
    # Initialize a sub-route
    subRoute = []
    vehicleLoad = 0
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
        # Update last customer ID
        lastCustomerID = customerID
    if subRoute != []:
        # Save current sub-route before return if not empty
        route.append(subRoute)
    return route
```

#### Print Route
```python
printRoute(route, merge=False)
```

prints sub-routes information to screen.

**Parameters:**

- `route` – A `route` decoded by `ind2route(individual, instance)`.
- `merge` – If `Ture`, detailed sub-routes are displayed in a single line.

**Returns:**

- None

**Definition:**

```python
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
            print '  Vehicle %d\'s route: %s' % (subRouteCount, subRouteStr)
        routeStr = routeStr + ' - 0'
    if merge:
        print routeStr
    return
```

### Evaluation
```python
evalVRPTW(individual, instance, unitCost=1.0, initCost=0, waitCost=0, delayCost=0)
```

takes one individual as argument and returns its fitness as a Python `tuple` object.

**Parameters:**

- `individual` - An individual to be evaluated.
- `instance` - A problem instance `dict` object, which can be loaded from a JSON format file.
- `unitCost` - The transportation cost of one vehicle for a unit distance.
- `initCost` - The start-up cost of a vehicle.
- `waitCost` - Cost per unit time if the vehicle arrives early than the customer's ready time.
- `delayCost` - Cost per unit time if the vehicle arrives later than the due time.

**Returns:**

- A tuple of one fitness value of the evaluated individual.

**Definition:**

```python
def evalVRPTW(individual, instance, unitCost=1.0, initCost=0, waitCost=0, delayCost=0):
    totalCost = 0
    route = ind2route(individual, instance)
    totalCost = 0
    for subRoute in route:
        subRouteTimeCost = 0
        subRouteDistance = 0
        elapsedTime = 0
        lastCustomerID = 0
        for customerID in subRoute:
            # Calculate section distance
            distance = instance['distance_matrix'][lastCustomerID][customerID]
            # Update sub-route distance
            subRouteDistance = subRouteDistance + distance
            # Calculate time cost
            arrivalTime = elapsedTime + distance
            timeCost = waitCost * max(instance['customer_%d' % customerID]['ready_time'] - arrivalTime, 0) + delayCost * max(arrivalTime - instance['customer_%d' % customerID]['due_time'], 0)
            # Update sub-route time cost
            subRouteTimeCost = subRouteTimeCost + timeCost
            # Update elapsed time
            elapsedTime = arrivalTime + instance['customer_%d' % customerID]['service_time']
            # Update last customer ID
            lastCustomerID = customerID
        # Calculate transport cost
        subRouteDistance = subRouteDistance + instance['distance_matrix'][lastCustomerID][0]
        subRouteTranCost = initCost + unitCost * subRouteDistance
        # Obtain sub-route cost
        subRouteCost = subRouteTimeCost + subRouteTranCost
        # Update total cost
        totalCost = totalCost + subRouteCost
    fitness = 1.0 / totalCost
    return fitness,
```

### Selection: Roulette Wheel Selection
```python
deap.tools.selRoulette(individuals, k)
```

selects `k` individuals from the input individuals using `k` spins of a roulette. The selection is made by looking only at the first objective of each individual. The list returned contains references to the input individuals.

**Parameters:**

- `individuals` – A list of individuals to select from.
- `k` – The number of individuals to select.

**Returns:**

- A list of selected individuals.

**Definition:**

```python
def selRoulette(individuals, k):
    s_inds = sorted(individuals, key=attrgetter("fitness"), reverse=True)
    sum_fits = sum(ind.fitness.values[0] for ind in individuals)
    chosen = []
    for i in xrange(k):
        u = random.random() * sum_fits
        sum_ = 0
        for ind in s_inds:
            sum_ += ind.fitness.values[0]
            if sum_ > u:
                chosen.append(ind)
                break
    return chosen
```

### Crossover: Partially Matched Crossover
```python
cxPartialyMatched(ind1, ind2)
```

executes a partially matched crossover (PMX) on the input individuals. The two individuals are modified in place. This crossover expects sequence individuals of indexes, the result for any other type of individuals is unpredictable.

**Parameters:**

- `ind1` – The first individual participating in the crossover.
- `ind2` – The second individual participating in the crossover.

**Returns:**

- A tuple of two individuals.

**Definition:**

```python
def cxPartialyMatched(ind1, ind2):
    size = min(len(ind1), len(ind2))
    cxpoint1, cxpoint2 = sorted(random.sample(range(size), 2))
    temp1 = ind1[cxpoint1:cxpoint2+1] + ind2
    temp2 = ind1[cxpoint1:cxpoint2+1] + ind1
    ind1 = []
    for x in temp1:
        if x not in ind1:
            ind1.append(x)
    ind2 = []
    for x in temp2:
        if x not in ind2:
            ind2.append(x)
    return ind1, ind2
```

### Mutation: Inverse Operation
```python
mutInverseIndexes(individual)
```

inverses the attributes between two random points of the input individual and return the mutant. This mutation expects sequence individuals of indexes, the result for any other type of individuals is unpredictable.

**Parameters:**

- `individual` – Individual to be mutated.

**Returns:**

- A tuple of one individual.

**Definition:**

```python
def mutInverseIndexes(individual):
    start, stop = sorted(random.sample(range(len(individual)), 2))
    individual = individual[:start] + individual[stop:start-1:-1] + individual[stop+1:]
    return individual,
```

### Algorithm
```python
gaVRPTW(
    instName,
    unitCost,
    initCost,
    waitCost,
    delayCost,
    indSize,
    popSize,
    cxPb,
    mutPb,
    NGen,
    exportCSV=False,
    customizeData=False
)
```

implements a genetic algorithm-based solution to vehicle routing problem with time windows (VRPTW).

**Parameters:**

- `instName` - A problem instance name provided in Solomon's VRPTW benchmark problems.
- `unitCost` - The transportation cost of one vehicle for a unit distance.
- `initCost` - The start-up cost of a vehicle.
- `waitCost` - Cost per unit time if the vehicle arrives early than the customer's ready time.
- `delayCost` - Cost per unit time if the vehicle arrives later than the due time.
- `indSize` - Size of an individual.
- `popSize` - Size of a population.
- `cxPb` - Probability of crossover.
- `mutPb` - Probability of mutation.
- `NGen` - Maximum number of generations to terminate evolution.
- `exportCSV` - If `True`, a CSV format log file will be exported to the `results\` directory.
- `customizeData` - If `Ture`, customized JSON format problem instance file will be loaded from `data\json_customized\` directory.

**Returns:**

- None

**Definition:**

```python
def gaVRPTW(instName, unitCost, initCost, waitCost, delayCost, indSize, popSize, cxPb, mutPb, NGen, exportCSV=False, customizeData=False):
    if customizeData:
        jsonDataDir = os.path.join(BASE_DIR,'data', 'json_customize')
    else:
        jsonDataDir = os.path.join(BASE_DIR,'data', 'json')
    jsonFile = os.path.join(jsonDataDir, '%s.json' % instName)
    with open(jsonFile) as f:
        instance = load(f)
    creator.create('FitnessMax', base.Fitness, weights=(1.0,))
    creator.create('Individual', list, fitness=creator.FitnessMax)
    toolbox = base.Toolbox()
    # Attribute generator
    toolbox.register('indexes', random.sample, range(1, indSize + 1), indSize)
    # Structure initializers
    toolbox.register('individual', tools.initIterate, creator.Individual, toolbox.indexes)
    toolbox.register('population', tools.initRepeat, list, toolbox.individual)
    # Operator registering
    toolbox.register('evaluate', evalVRPTW, instance=instance, unitCost=unitCost, initCost=initCost, waitCost=waitCost, delayCost=delayCost)
    toolbox.register('select', tools.selRoulette)
    toolbox.register('mate', cxPartialyMatched)
    toolbox.register('mutate', mutInverseIndexes)
    pop = toolbox.population(n=popSize)
    # Results holders for exporting results to CSV file
    csvData = []
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
        invalidInd = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalidInd)
        for ind, fit in zip(invalidInd, fitnesses):
            ind.fitness.values = fit
        print '  Evaluated %d individuals' % len(invalidInd)
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
        # Write data to holders for exporting results to CSV file
        if exportCSV:
            csvRow = {
                'generation': g,
                'evaluated_individuals': len(invalidInd),
                'min_fitness': min(fits),
                'max_fitness': max(fits),
                'avg_fitness': mean,
                'std_fitness': std,
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
        csvPathname = os.path.join(BASE_DIR, 'results', csvFilename)
        print 'Write to file: %s' % csvPathname
        makeDirsForFile(pathname=csvPathname)
        if not exist(pathname=csvPathname, overwrite=True):
            with open(csvPathname, 'w') as f:
                fieldnames = ['generation', 'evaluated_individuals', 'min_fitness', 'max_fitness', 'avg_fitness', 'std_fitness']
                writer = DictWriter(f, fieldnames=fieldnames, dialect='excel')
                writer.writeheader()
                for csvRow in csvData:
                    writer.writerow(csvRow)
```

### Sample Codes
#### Instance: R101
```python
# -*- coding: utf-8 -*-
# sample_R101.py

import random
from gavrptw.core import gaVRPTW


def main():
    random.seed(64)

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

    exportCSV = True

    gaVRPTW(
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
        exportCSV=exportCSV
    )


if __name__ == '__main__':
    main()
```

#### Instance: C204
```python
# -*- coding: utf-8 -*-
# sample_C204.py

import random
from gavrptw.core import gaVRPTW


def main():
    random.seed(64)

    instName = 'C204'

    unitCost = 8.0
    initCost = 100.0
    waitCost = 1.0
    delayCost = 1.5

    indSize = 100
    popSize = 400
    cxPb = 0.85
    mutPb = 0.02
    NGen = 300

    exportCSV = True

    gaVRPTW(
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
        exportCSV=exportCSV
    )


if __name__ == '__main__':
    main()
```

#### Customized Instance
```python
# -*- coding: utf-8 -*-
# sample_Customized_Data.py

import random
from gavrptw.core import gaVRPTW


def main():
    random.seed(64)

    instName = 'Customized_Data'

    unitCost = 8.0
    initCost = 100.0
    waitCost = 1.0
    delayCost = 1.5

    indSize = 100
    popSize = 400
    cxPb = 0.85
    mutPb = 0.02
    NGen = 300

    exportCSV = True
    customizeData = True

    gaVRPTW(
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
    main()
```

#### View Logs
The sample codes will print logs on the screen. Meanwhile, a **CSV format** log file will be saved in the `results\` directory after running each sample code, which can be canceled by setting the `exportCSV` flag to `False`, i.e.,

```python
# -*- coding: utf-8 -*-
# sample_R101.py

    ...
    exportCSV = False

    gaVRPTW(
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
        exportCSV=exportCSV
    )
    ...
```

## API Reference
### Module: `gavrptw`
Excerpt from `gavrptw/__init__.py`:

```python
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
```

### Module: `gavrptw.core`
```python
route = ind2route(individual, instance)
```
```python
printRoute(route, merge=False)
```
```python
evalVRPTW(individual, instance, unitCost=1.0, initCost=0, waitCost=0, delayCost=0)
```
```python
ind1, ind2 = cxPartialyMatched(ind1, ind2)
```
```python
individual, = mutInverseIndexes(individual)
```
```python
gaVRPTW(
    instName,
    unitCost,
    initCost,
    waitCost,
    delayCost,
    indSize,
    popSize,
    cxPb,
    mutPb,
    NGen,
    exportCSV=False,
    customizeData=False
)
```

### Module: `gavrptw.utils`
```python
makeDirsForFile(pathname)
```
```python
exist(pathname, overwrite=False, displayInfo=True)
```
```python
text2json(customize=False)
```

## File Structure
```
├── data/
│   ├── json/
│   │   ├── <Instance name>.json
│   │   └── ...
│   ├── json_customize/
│   │   ├── <Customized instance name>.json
│   │   └── ...
│   ├── text/
│   │   ├── <Instance name>.txt
│   │   └── ...
│   └── text_customize/
│       ├── <Customized instance name>.txt
│       └── ...
├── results/
│   └── ...
├── gavrptw/
│   ├── __init__.py
│   ├── core.py
│   └── utils.py
├── text2json.py
├── text2json_customize.py
├── sample_R101.py
├── sample_C204.py
├── sample_Customized_Data.py
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

## Further Reading
**Distributed Evolutionary Algorithms in Python (DEAP)**

- [Docs][deap-docs]
- [GitHub][deap-github]
- [PyPI][deap-pypi]

## References
1. [Solomon's VRPTW Benchmark Problems][solomon]
2. [100 Customers Instance Definitions][100-customers]
3. [Distributed Evolutionary Algorithms in Python (DEAP)][deap-pypi]

## License
[MIT License][license]

[repository]: https://github.com/iROCKBUNNY/py-ga-VRPTW "iROCKBUNNY/py-ga-VRPTW"
[release]: https://github.com/iROCKBUNNY/py-ga-VRPTW/releases/latest "Latest Release"
[license]: https://github.com/iROCKBUNNY/py-ga-VRPTW/LICENSE "License"
[watch]: https://github.com/iROCKBUNNY/py-ga-VRPTW/watchers "Watchers"
[star]: https://github.com/iROCKBUNNY/py-ga-VRPTW/stargazers "Stargazers"
[fork]: https://github.com/iROCKBUNNY/py-ga-VRPTW/network "Forks"

[macos]: https://www.apple.com/macos/ "macOS"
[python]: https://docs.python.org/2/ "Python 2.7"
[pip]: https://pypi.python.org/pypi/pip "Pip"
[virtualenv]: https://virtualenv.pypa.io/en/stable/ "Virtualenv"
[yingriyanlong-github]: https://github.com/yingriyanlong "@yingriyanlong"
[yingriyanlong-verison]: https://github.com/yingriyanlong/py-ga-VRPTW "yingriyanlong/py-ga-VRPTW"

[solomon]: http://web.cba.neu.edu/~msolomon/problems.htm "Solomon's VRPTW Benchmark Problems"
[100-customers]: http://www.sintef.no/projectweb/top/vrptw/solomon-benchmark/100-customers/ "100 Customers Instance Definitions"
[100-customers-zip]: http://www.sintef.no/globalassets/project/top/vrptw/solomon/solomon-100.zip "100 Customers Instance Definitions (Zip)"

[deap-docs]: http://deap.readthedocs.org/ "Distributed Evolutionary Algorithms in Python (DEAP) Docs"
[deap-github]: https://github.com/deap/deap/ "Distributed Evolutionary Algorithms in Python (DEAP) GirHub"
[deap-pypi]: https://pypi.python.org/pypi/deap/ "Distributed Evolutionary Algorithms in Python (DEAP) PyPI"
