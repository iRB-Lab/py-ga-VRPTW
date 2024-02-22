[![Build Status](https://img.shields.io/travis/com/iRB-Lab/py-ga-VRPTW?logo=travisci)][travis-ci]
[![Python](https://img.shields.io/badge/python-3.12-blue?logo=python)][python]
[![License](https://img.shields.io/github/license/iRB-Lab/py-ga-VRPTW)][license]
[![Last Commit](https://img.shields.io/github/last-commit/iRB-Lab/py-ga-VRPTW?logo=github)][commit]

# py-ga-VRPTW
A Python Implementation of a Genetic Algorithm-based Solution to Vehicle Routing Problem with Time Windows (VRPTW)

> [!IMPORTANT]
>
> ### Project Origin (Backstory)
>
> This project is originated from a university course project.
>
> In 2016, a friend of mine, majoring in logistic engineering, came to me to discuss his course work project. He wanted to solve VRPTW using genetic algorithm, which I happened to know. The discussion went well and my friend got what he needed.
>
> After that, I implemented the approach in Python. The first version of the this project came out that night.
>
> ### Performance Issue (Frequently Asked)
>
> I wrote this project on the spur of that moment. However, after running a few tests with several combinations of parameters and set-ups, I realized that implementing the idea is one thing, and tuning the algorithm to yield a converged result is another thing. The latter would definitely require much more effort.
>
> Therefore, I should say, **to be precise, the performances of the given examples are very poor.**
>
> Of course, tuning improvements of this algorithm and forks are always welcome.
>
> #### Some Outstanding Forks:
>
> - [paulliwali/**py-ga-VRPTW**](https://github.com/paulliwali/py-ga-VRPTW)

## Contents
- [Installation](#installation)
    - [Requirements](#requirements)
    - [Installing with Virtualenv](#installing-with-virtualenv)
- [Quick Start](#quick-start)
- [Problem Sets](#problem-sets)
    - [Solomon's VRPTW Benchmark Problems](#solomons-vrptw-benchmark-problems1)
    - [Instance Definitions](#instance-definitions)
        - [Text File Format](#text-file-format)
        - [JSON Format](#json-format)
        - [Use Customized Instance Data](#use-customized-instance-data)
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
- [Python 3.12][python]
- [Pip][pip]

### Installing with Virtualenv
On Unix, Linux, BSD, macOS, and Cygwin:

```sh
git clone https://github.com/iRB-Lab/py-ga-VRPTW.git
cd py-ga-VRPTW
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Quick Start
See [sample codes](#sample-codes).

## Problem Sets
### Solomon's VRPTW Benchmark Problems<sup>[1][solomon]</sup>
|Problem Set|Random|Clustered|Random & Clustered|
|:--|:--|:--|:--|
|Short Scheduling Horizon|R1-type|C1-type|RC1-type|
|Long Scheduling Horizon|R2-type|C2-type|RC2-type|

> [!NOTE]
>
> 1. Solomon generated six sets of problems. Their design highlights several factors that affect the behavior of routing and scheduling algorithms. They are:
>    - geographical data;
>    - the number of customers serviced by a vehicle;
>    - percent of time-constrained customers; and
>    - tightness and positioning of the time windows.
>
> 2. The geographical data are randomly generated in problem sets R1 and R2, clustered in problem sets C1 and C2, and a mix of random and clustered structures in problem sets by RC1 and RC2.
> 3. Problem sets R1, C1 and RC1 have a short scheduling horizon and allow only a few customers per route (approximately 5 to 10). In contrast, the sets R2, C2 and RC2 have a long scheduling horizon permitting many customers (more than 30) to be serviced by the same vehicle.
> 4. The customer coordinates are identical for all problems within one type (i.e., R, C and RC).
> 5. The problems differ with respect to the width of the time windows. Some have very tight time windows, while others have time windows which are hardly constraining. In terms of time window density, that is, the percentage of customers with time windows, I created problems with 25, 50, 75 and 100% time windows.
> 6. The larger problems are 100 customer euclidean problems where travel times equal the corresponding distances. For each such problem, smaller problems have been created by considering only the first 25 or 50 customers.

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

> [!NOTE]
>
> 1. All constants are integers.
> 2. `CUST NO.` 0 denotes the depot, where all vehicles must start and finish.
> 3. `K` is the maximum number of vehicles.
> 4. `Q` the capacity of each vehicle.
> 5. `READY TIME` is the earliest time at which service may start at the given customer/depot.
> 6. `DUE DATE` is the latest time at which service may start at the given customer/depot.
> 7. The value of time is equal to the value of distance.
> 8. As a backup, you can download a zip-file with the 100 customers instance definitions<sup>[2][100-customers]</sup> [here][100-customers-zip].

#### JSON Format
For the further convenience, a Python script named `text2json.py` is written to convert problem instances from the **text file format** to **JSON format** and stored under the `data/json/` directory. Like the text files, each JSON file is named with respect to its corresponding instance name, e.g.: the JSON file corresponding to problem instance **C101** is `C101.json`, and locates at `data/json/C101.json`.

Below is a description of the format of the JSON file that defines each problem instance (assuming 100 customers).

```js
{
    "instance_name" : "<Instance name>",
    "max_vehicle_number" : K,
    "vehicle_capacity" : Q,
    "depart" : {
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

> [!NOTE]
>
> 1. `dist1_1` denotes the distance between Customer 1 and Customer 1, which should be 0, obviously.
> 2. To obtain the distance value between Customer 1 and Customer 2 in Python can be done by using `<json_data>['distance_matrix'][1][2]`, where `<json_data>` denotes the name of a Python `dict` object.

#### Use Customized Instance Data
You can customize your own problem instances.

##### Supported File Format
The customized problem instance data file should be either **text file format** or **JSON format**, exactly the same as the above given examples.

##### Directory Set-up
Customized `*.txt` files should be put under the `data\text_customize\` directory, and customized `*.json` files should be put under the `data\json_customize\` directory.

##### Convert `*.txt` to `*.json`
Run the `text2json_customize.py` script to convert `*.txt` file containing customized problem instance data to `*.json` file.

```sh
python text2json_customize.py
```

##### GA Set-up
The `customize_data` flag of the `run_gavrptw()` method should be set to `True`. For further understanding, please refer to the sample codes section at the end of this document.

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

##### Parameters

- `individual` – An individual to be decoded.
- `instance` – A problem instance `dict` object, which can be loaded from a JSON format file.

##### Returns

- A list of decoded sub-routes corresponding to the input individual.

##### Definition

```python
def ind2route(individual, instance):
    route = []
    vehicle_capacity = instance['vehicle_capacity']
    depart_due_time = instance['depart']['due_time']
    # Initialize a sub-route
    sub_route = []
    vehicle_load = 0
    elapsed_time = 0
    last_customer_id = 0
    for customer_id in individual:
        # Update vehicle load
        demand = instance[f'customer_{customer_id}']['demand']
        updated_vehicle_load = vehicle_load + demand
        # Update elapsed time
        service_time = instance[f'customer_{customer_id}']['service_time']
        return_time = instance['distance_matrix'][customer_id][0]
        updated_elapsed_time = elapsed_time + \
            instance['distance_matrix'][last_customer_id][customer_id] + service_time + return_time
        # Validate vehicle load and elapsed time
        if (updated_vehicle_load <= vehicle_capacity) and (updated_elapsed_time <= depart_due_time):
            # Add to current sub-route
            sub_route.append(customer_id)
            vehicle_load = updated_vehicle_load
            elapsed_time = updated_elapsed_time - return_time
        else:
            # Save current sub-route
            route.append(sub_route)
            # Initialize a new sub-route and add to it
            sub_route = [customer_id]
            vehicle_load = demand
            elapsed_time = instance['distance_matrix'][0][customer_id] + service_time
        # Update last customer ID
        last_customer_id = customer_id
    if sub_route != []:
        # Save current sub-route before return if not empty
        route.append(sub_route)
    return route
```

#### Print Route
```python
print_route(route, merge=False)
```

prints sub-routes information to screen.

##### Parameters

- `route` – A `route` decoded by `ind2route(individual, instance)`.
- `merge` – If `Ture`, detailed sub-routes are displayed in a single line.

##### Returns

- None

##### Definition

```python
def print_route(route, merge=False):
    route_str = '0'
    sub_route_count = 0
    for sub_route in route:
        sub_route_count += 1
        sub_route_str = '0'
        for customer_id in sub_route:
            sub_route_str = f'{sub_route_str} - {customer_id}'
            route_str = f'{route_str} - {customer_id}'
        sub_route_str = f'{sub_route_str} - 0'
        if not merge:
            print(f'  Vehicle {sub_route_count}\'s route: {sub_route_str}')
        route_str = f'{route_str} - 0'
    if merge:
        print(route_str)
```

### Evaluation
```python
eval_vrptw(individual, instance, unit_cost=1.0, init_cost=0, wait_cost=0, delay_cost=0)
```

takes one individual as argument and returns its fitness as a Python `tuple` object.

##### Parameters

- `individual` - An individual to be evaluated.
- `instance` - A problem instance `dict` object, which can be loaded from a JSON format file.
- `unit_cost` - The transportation cost of one vehicle for a unit distance.
- `init_cost` - The start-up cost of a vehicle.
- `wait_cost` - Cost per unit time if the vehicle arrives early than the customer's ready time.
- `delay_cost` - Cost per unit time if the vehicle arrives later than the due time.

##### Returns

- A tuple of one fitness value of the evaluated individual.

##### Definition

```python
def eval_vrptw(individual, instance, unit_cost=1.0, init_cost=0, wait_cost=0, delay_cost=0):
    total_cost = 0
    route = ind2route(individual, instance)
    total_cost = 0
    for sub_route in route:
        sub_route_time_cost = 0
        sub_route_distance = 0
        elapsed_time = 0
        last_customer_id = 0
        for customer_id in sub_route:
            # Calculate section distance
            distance = instance['distance_matrix'][last_customer_id][customer_id]
            # Update sub-route distance
            sub_route_distance = sub_route_distance + distance
            # Calculate time cost
            arrival_time = elapsed_time + distance
            time_cost = wait_cost * max(instance[f'customer_{customer_id}']['ready_time'] - \
                arrival_time, 0) + delay_cost * max(arrival_time - \
                instance[f'customer_{customer_id}']['due_time'], 0)
            # Update sub-route time cost
            sub_route_time_cost = sub_route_time_cost + time_cost
            # Update elapsed time
            elapsed_time = arrival_time + instance[f'customer_{customer_id}']['service_time']
            # Update last customer ID
            last_customer_id = customer_id
        # Calculate transport cost
        sub_route_distance = sub_route_distance + instance['distance_matrix'][last_customer_id][0]
        sub_route_transport_cost = init_cost + unit_cost * sub_route_distance
        # Obtain sub-route cost
        sub_route_cost = sub_route_time_cost + sub_route_transport_cost
        # Update total cost
        total_cost = total_cost + sub_route_cost
    fitness = 1.0 / total_cost
    return (fitness, )
```

### Selection: Roulette Wheel Selection
```python
deap.tools.selRoulette(individuals, k)
```

selects `k` individuals from the input individuals using `k` spins of a roulette. The selection is made by looking only at the first objective of each individual. The list returned contains references to the input individuals.

##### Parameters

- `individuals` – A list of individuals to select from.
- `k` – The number of individuals to select.

##### Returns

- A list of selected individuals.

##### Definition

```python
def selRoulette(individuals, k):
    s_inds = sorted(individuals, key=attrgetter(fit_attr), reverse=True)
    sum_fits = sum(getattr(ind, fit_attr).values[0] for ind in individuals)
    chosen = []
    for i in range(k):
        u = random.random() * sum_fits
        sum_ = 0
        for ind in s_inds:
            sum_ += getattr(ind, fit_attr).values[0]
            if sum_ > u:
                chosen.append(ind)
                break
    return chosen
```

### Crossover: Partially Matched Crossover
```python
cx_partially_matched(ind1, ind2)
```

executes a partially matched crossover (PMX) on the input individuals. The two individuals are modified in place. This crossover expects sequence individuals of indexes, the result for any other type of individuals is unpredictable.

##### Parameters

- `ind1` – The first individual participating in the crossover.
- `ind2` – The second individual participating in the crossover.

##### Returns

- A tuple of two individuals.

##### Definition

```python
def cx_partially_matched(ind1, ind2):
    cxpoint1, cxpoint2 = sorted(random.sample(range(min(len(ind1), len(ind2))), 2))
    part1 = ind2[cxpoint1:cxpoint2+1]
    part2 = ind1[cxpoint1:cxpoint2+1]
    rule1to2 = list(zip(part1, part2))
    is_fully_merged = False
    while not is_fully_merged:
        rule1to2, is_fully_merged = merge_rules(rules=rule1to2)
    rule2to1 = {rule[1]: rule[0] for rule in rule1to2}
    rule1to2 = dict(rule1to2)
    ind1 = [gene if gene not in part2 else rule2to1[gene] for gene in ind1[:cxpoint1]] + part2 + \
        [gene if gene not in part2 else rule2to1[gene] for gene in ind1[cxpoint2+1:]]
    ind2 = [gene if gene not in part1 else rule1to2[gene] for gene in ind2[:cxpoint1]] + part1 + \
        [gene if gene not in part1 else rule1to2[gene] for gene in ind2[cxpoint2+1:]]
    return ind1, ind2
```

### Mutation: Inverse Operation
```python
mut_inverse_indexes(individual)
```

inverses the attributes between two random points of the input individual and return the mutant. This mutation expects sequence individuals of indexes, the result for any other type of individuals is unpredictable.

##### Parameters

- `individual` – Individual to be mutated.

##### Returns

- A tuple of one individual.

##### Definition

```python
def mut_inverse_indexes(individual):
    start, stop = sorted(random.sample(range(len(individual)), 2))
    temp = individual[start:stop+1]
    temp.reverse()
    individual[start:stop+1] = temp
    return (individual, )
```

### Algorithm
```python
run_gavrptw(instance_name, unit_cost, init_cost, wait_cost, delay_cost, ind_size, pop_size, \
    cx_pb, mut_pb, n_gen, export_csv=False, customize_data=False)
```

implements a genetic algorithm-based solution to vehicle routing problem with time windows (VRPTW).

##### Parameters

- `instance_name` - A problem instance name provided in Solomon's VRPTW benchmark problems.
- `unit_cost` - The transportation cost of one vehicle for a unit distance.
- `init_cost` - The start-up cost of a vehicle.
- `wait_cost` - Cost per unit time if the vehicle arrives early than the customer's ready time.
- `delay_cost` - Cost per unit time if the vehicle arrives later than the due time.
- `ind_size` - Size of an individual.
- `pop_size` - Size of a population.
- `cx_pb` - Probability of crossover.
- `mut_pb` - Probability of mutation.
- `n_gen` - Maximum number of generations to terminate evolution.
- `export_csv` - If `True`, a CSV format log file will be exported to the `results\` directory.
- `customize_data` - If `Ture`, customized JSON format problem instance file will be loaded from `data\json_customized\` directory.

##### Returns

- None

##### Definition

```python
def run_gavrptw(instance_name, unit_cost, init_cost, wait_cost, delay_cost, ind_size, pop_size, \
    cx_pb, mut_pb, n_gen, export_csv=False, customize_data=False):
    if customize_data:
        json_data_dir = os.path.join(BASE_DIR, 'data', 'json_customize')
    else:
        json_data_dir = os.path.join(BASE_DIR, 'data', 'json')
    json_file = os.path.join(json_data_dir, f'{instance_name}.json')
    instance = load_instance(json_file=json_file)
    if instance is None:
        return
    creator.create('FitnessMax', base.Fitness, weights=(1.0, ))
    creator.create('Individual', list, fitness=creator.FitnessMax)
    toolbox = base.Toolbox()
    # Attribute generator
    toolbox.register('indexes', random.sample, range(1, ind_size + 1), ind_size)
    # Structure initializers
    toolbox.register('individual', tools.initIterate, creator.Individual, toolbox.indexes)
    toolbox.register('population', tools.initRepeat, list, toolbox.individual)
    # Operator registering
    toolbox.register('evaluate', eval_vrptw, instance=instance, unit_cost=unit_cost, \
        init_cost=init_cost, wait_cost=wait_cost, delay_cost=delay_cost)
    toolbox.register('select', tools.selRoulette)
    toolbox.register('mate', cx_partially_matched)
    toolbox.register('mutate', mut_inverse_indexes)
    pop = toolbox.population(n=pop_size)
    # Results holders for exporting results to CSV file
    csv_data = []
    print('Start of evolution')
    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    print(f'  Evaluated {len(pop)} individuals')
    # Begin the evolution
    for gen in range(n_gen):
        print(f'-- Generation {gen} --')
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))
        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < cx_pb:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values
        for mutant in offspring:
            if random.random() < mut_pb:
                toolbox.mutate(mutant)
                del mutant.fitness.values
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        print(f'  Evaluated {len(invalid_ind)} individuals')
        # The population is entirely replaced by the offspring
        pop[:] = offspring
        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]
        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum([x**2 for x in fits])
        std = abs(sum2 / length - mean**2)**0.5
        print(f'  Min {min(fits)}')
        print(f'  Max {max(fits)}')
        print(f'  Avg {mean}')
        print(f'  Std {std}')
        # Write data to holders for exporting results to CSV file
        if export_csv:
            csv_row = {
                'generation': gen,
                'evaluated_individuals': len(invalid_ind),
                'min_fitness': min(fits),
                'max_fitness': max(fits),
                'avg_fitness': mean,
                'std_fitness': std,
            }
            csv_data.append(csv_row)
    print('-- End of (successful) evolution --')
    best_ind = tools.selBest(pop, 1)[0]
    print(f'Best individual: {best_ind}')
    print(f'Fitness: {best_ind.fitness.values[0]}')
    print_route(ind2route(best_ind, instance))
    print(f'Total cost: {1 / best_ind.fitness.values[0]}')
    if export_csv:
        csv_file_name = f'{instance_name}_uC{unit_cost}_iC{init_cost}_wC{wait_cost}' \
            f'_dC{delay_cost}_iS{ind_size}_pS{pop_size}_cP{cx_pb}_mP{mut_pb}_nG{n_gen}.csv'
        csv_file = os.path.join(BASE_DIR, 'results', csv_file_name)
        print(f'Write to file: {csv_file}')
        make_dirs_for_file(path=csv_file)
        if not exist(path=csv_file, overwrite=True):
            with io.open(csv_file, 'wt', newline='') as file_object:
                fieldnames = [
                    'generation',
                    'evaluated_individuals',
                    'min_fitness',
                    'max_fitness',
                    'avg_fitness',
                    'std_fitness',
                ]
                writer = DictWriter(file_object, fieldnames=fieldnames, dialect='excel')
                writer.writeheader()
                for csv_row in csv_data:
                    writer.writerow(csv_row)
```

### Sample Codes
#### Instance: R101
```python
# -*- coding: utf-8 -*-

'''sample_R101.py'''

import random
from gavrptw.core import run_gavrptw


def main():
    '''main()'''
    random.seed(64)

    instance_name = 'R101'

    unit_cost = 8.0
    init_cost = 60.0
    wait_cost = 0.5
    delay_cost = 1.5

    ind_size = 25
    pop_size = 80
    cx_pb = 0.85
    mut_pb = 0.01
    n_gen = 100

    export_csv = True

    run_gavrptw(instance_name=instance_name, unit_cost=unit_cost, init_cost=init_cost, \
        wait_cost=wait_cost, delay_cost=delay_cost, ind_size=ind_size, pop_size=pop_size, \
        cx_pb=cx_pb, mut_pb=mut_pb, n_gen=n_gen, export_csv=export_csv)


if __name__ == '__main__':
    main()
```

#### Instance: C204
```python
# -*- coding: utf-8 -*-

'''sample_C204.py'''

import random
from gavrptw.core import run_gavrptw


def main():
    '''main()'''
    random.seed(64)

    instance_name = 'C204'

    unit_cost = 8.0
    init_cost = 100.0
    wait_cost = 1.0
    delay_cost = 1.5

    ind_size = 100
    pop_size = 400
    cx_pb = 0.85
    mut_pb = 0.02
    n_gen = 300

    export_csv = True

    run_gavrptw(instance_name=instance_name, unit_cost=unit_cost, init_cost=init_cost, \
        wait_cost=wait_cost, delay_cost=delay_cost, ind_size=ind_size, pop_size=pop_size, \
        cx_pb=cx_pb, mut_pb=mut_pb, n_gen=n_gen, export_csv=export_csv)


if __name__ == '__main__':
    main()
```

#### Customized Instance
```python
# -*- coding: utf-8 -*-

'''sample_customized_data.py'''

import random
from gavrptw.core import run_gavrptw


def main():
    '''main()'''
    random.seed(64)

    instance_name = 'Customized_Data'

    unit_cost = 8.0
    init_cost = 100.0
    wait_cost = 1.0
    delay_cost = 1.5

    ind_size = 100
    pop_size = 400
    cx_pb = 0.85
    mut_pb = 0.02
    n_gen = 300

    export_csv = True
    customize_data = True

    run_gavrptw(instance_name=instance_name, unit_cost=unit_cost, init_cost=init_cost, \
        wait_cost=wait_cost, delay_cost=delay_cost, ind_size=ind_size, pop_size=pop_size, \
        cx_pb=cx_pb, mut_pb=mut_pb, n_gen=n_gen, export_csv=export_csv, \
        customize_data=customize_data)


if __name__ == '__main__':
    main()
```

#### View Logs
The sample codes will print logs on the screen. Meanwhile, a **CSV format** log file will be saved in the `results\` directory after running each sample code, which can be canceled by setting the `export_csv` flag to `False`, i.e.,

```python
# -*- coding: utf-8 -*-
# sample_R101.py

    ...
    export_csv = False

    run_gavrptw(instance_name=instance_name, unit_cost=unit_cost, init_cost=init_cost, \
        wait_cost=wait_cost, delay_cost=delay_cost, ind_size=ind_size, pop_size=pop_size, \
        cx_pb=cx_pb, mut_pb=mut_pb, n_gen=n_gen, export_csv=export_csv)
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
print_route(route, merge=False)
```
```python
eval_vrptw(individual, instance, unit_cost=1.0, init_cost=0, wait_cost=0, delay_cost=0)
```
```python
ind1, ind2 = cx_partially_matched(ind1, ind2)
```
```python
individual, = mut_inverse_indexes(individual)
```
```python
run_gavrptw(instance_name, unit_cost, init_cost, wait_cost, delay_cost, ind_size, pop_size, \
    cx_pb, mut_pb, n_gen, export_csv=False, customize_data=False)
```

### Module: `gavrptw.utils`
```python
make_dirs_for_file(path)
```
```python
guess_path_type(path)
```
```python
exist(path, overwrite=False, display_info=True)
```
```python
load_instance(json_file)
```
```python
merge_rules(rules)
```
```python
calculate_distance(customer1, customer2)
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
├── sample_customized_data.py
├── requirements.txt
├── README.md
├── LICENSE
├── .travis.yml
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

[repository]: https://github.com/iRB-Lab/py-ga-VRPTW "iRB-Lab/py-ga-VRPTW"
[license]: https://github.com/iRB-Lab/py-ga-VRPTW/blob/master/LICENSE "License"
[commit]: https://github.com/iRB-Lab/py-ga-VRPTW/commits/master "Last Commit"
[travis-ci]: https://app.travis-ci.com/github/iRB-Lab/py-ga-VRPTW "Travis CI"

[python]: https://docs.python.org/ "Python"
[pip]: https://pypi.python.org/pypi/pip "Pip"
[virtualenv]: https://virtualenv.pypa.io/en/stable/ "Virtualenv"

[solomon]: http://web.cba.neu.edu/~msolomon/problems.htm "Solomon's VRPTW Benchmark Problems"
[100-customers]: http://www.sintef.no/projectweb/top/vrptw/solomon-benchmark/100-customers/ "100 Customers Instance Definitions"
[100-customers-zip]: http://www.sintef.no/globalassets/project/top/vrptw/solomon/solomon-100.zip "100 Customers Instance Definitions (Zip)"

[deap-docs]: http://deap.readthedocs.org/ "Distributed Evolutionary Algorithms in Python (DEAP) Docs"
[deap-github]: https://github.com/deap/deap/ "Distributed Evolutionary Algorithms in Python (DEAP) GitHub"
[deap-pypi]: https://pypi.python.org/pypi/deap/ "Distributed Evolutionary Algorithms in Python (DEAP) PyPI"
