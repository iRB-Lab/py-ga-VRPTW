# py-ga-VRPMV

Forked from iRB-Lab to implement a GA solution to solve Vehicle Routing Problem with Movement Synchronization (VRPMV).

- Implemented a fix to the PMX function
- Implemented a more efficient selection process to improve the overall GA process
- Enabled multi-processing with the appropriate functions from the `DEAP` library using the `multiprocessing` module
- Solved VRP with movement synchronization involving the teamwork of heavy and light resource

## Reference to py-ga-VRPTW

- see iRB-Lab's [repository](https://github.com/iRB-Lab/py-ga-VRPTW)

## Contents for VRPMV

- [Modifications to the GA Implementation](#modifications-to-the-GA-implementation-for-VRPTW)
  - [Selection: Elite Selection](#Selection:-Elite-Selection)
  - [Partially Matched Crossover Method](#partially-matched-crossover-method)
  - [Multiprocessing](#Multiprocessing)
- [GA Implementation of Movement Synchronization](#GA-implementation-of-movement-synchronization)
  - [Individual with MV](#individual-with-movement-synchronization-(Chromosomes))
    - [Decode Individual with MV](#decode-individual-with-movement-synchronization)
    - [Create Individuals with MV](#create-individuals-with-movement-synchronization)
  - [Evaluation of Individual with MV](#evaluation-of-individuals-with-movement-synchronization)
  - [Crossover of Individual with MV](#crossover-of-individuals-with-movement-synchronization)

## Modifications to the GA Implementation for VRPTW

Several modifications are made to improve the performance of the iRB-lab's GA implementation.

### Selection: Elite Selection

Instead of solely relying on the roulette selection process to pick the individuals for crossover and mutation, select one elite `individual` to keep past the crossover and mutation step, select the top 10% of the current generation and roulette select the other 90%. The selection methods are using built-in `deap` tools

```python
elite = deal.tools.selBest(individuals, 1)
deap.tools.selBest(individuals, j)
deap.tools.selRoulette(individuals, k)
```

### Partially Matched Crossover Method

The partially matched crossover (PMX) method originally coded is based on a paper by Goldberg [(1985)][goldberg-1985]. The method was not working as intended, and I replaced it with the built-in version from `deap` with a small modification to account for the depot naming convention.

PMX is suited for problems where the optimal values and locations of the chromosomes matter. PMX works by randomly selecting a range of customers to swap between the routes. As each customer is swapped between the two routes, the duplicates are also swapped. For example if there are two `individuals`.

```python
A = [9, 8, 4, 5, 6, 7, 1, 3, 2, 10]
B = [8, 7, 1, 2, 3, 10, 9, 5, 4, 6]
```

PMX first randomly choose a range called the "mapping section".

```python
A = [9, 8, 4, 5, 6, 7, 1, 3, 2, 10]
             ^        ^
B = [8, 7, 1, 2, 3, 10, 9, 5, 4, 6]
             ^         ^
```
Then the first pair (5 - 2) is swapped, followed by a check to see where the duplicated customers are and swapped accordingly.

```python
A_swapped = [9, 8, 4, 2, 6, 7, 1, 3, 5, 10]
                     ^        ^
B_swapped = [8, 7, 1, 5, 3, 10, 9, 2, 4, 6]
                     ^         ^
```
Then it moves to the next pair (6 - 3) until all the pairs are exhausted in the mapping section.
```python
A_swapped = [9, 8, 4, 2, 3, 10, 1, 6, 5, 7]
                     ^         ^
B_swapped = [8, 10, 1, 5, 6, 7, 9, 2, 4, 3]
                      ^        ^
```

### Multiprocessing

Python is by default locked from using multiple processors on a given machine due to the Global Interpreter Lock (GIL). In order to circumvent this, the [`multiprocessing` module][multiprocessing] is used. However to take advantage of this, much of code has to be refactored so it is exposed in the global scope.

There are some on-going discussions and work done with this issue. For more information, reference [here](https://github.com/DEAP/deap/pull/76).

## GA Implementation of Movement Synchronization

### Individual (Chromosomes)

Recall the `individual` used in the GA process from the `py-ga-VRPTW` stage is coded in the following manner. If the sub-routes of the individual is the following:

```python
Sub-route 1: 0 - 5 - 3 - 2 - 0
Sub-route 2: 0 - 7 - 1 - 6 - 9 - 0
Sub-route 3: 0 - 8 - 4 - 0
```

then the `individual` is coded as a list of:

```python
individual = [5, 3, 2, 7, 1, 6, 9, 8, 4]
```

The process that decodes the `individual` into the sub-route representation is using a basic split procedure based on the capacity constraint of the vehicle. Each sub-route is split at the point which the addition of another customer will violate the capacity constraint.

### Individual with Movement Synchronization (Chromosomes)

For the purpose of representing both light and heavy resource sub-routes, a new representation is created based on the best individual from the `py-ga-VRPTW` stage. Using the same example as above, except this individual can be solely served by two sub-routes instead of one.

```python
bestIndividual = [5, 3, 2, 7, 1, 6, 9, 8, 4]
```

which is decoded into two sub-routes served by heavy resources

```python
heavy-sub-route 1: 0 - 5 - 2 - 7 - 1 - 6 - 9 - 0
heavy-sub-route 2: 0 - 8 - 4 - 0
```

#### Decode Individual with Movement Synchronization

```python
splitLightCustomers(instance, heavy-sub-route, lightRange, lightCapacity)
```

This method selects the customers in the `heavy-sub-route` based on their distance and demand and clusters them into potential customer groups for the light resource to deliver to.

##### Parameters

- `instance` – A problem instance dict object, which can be loaded from a JSON format file.
- `heavy-sub-route` – A heavy resource served sub-route from the individual.
- `lightRange` - A constant representing the maximum distance the light resource is able to travel.
- `lightCapacity` - A constant representing the maximum capacity the light resource is able to hold for each delivery.

##### Returns

- A binary list representing the customers which the light resource will deliver to.

```python
light-list-sub-route-1 = [0, 0, 1, 1, 0, 0]
light-list-sub-route-2 = [0, 0]
```

This example indicates that the light resource is expected to deliver to customer 7 and 1 in sub-route 1 and not deliver in sub-route 2.

#### Create Individuals with Movement Synchronization

Since the `indidivual` created for the `py-ga-VRPTW` stage is a list of floats representing the customers. The initialization process for the `py-ga-VRPTW` stage uses the `creator()` tool from the standard toolbox of the `deap` library.

The initialization for the `individual-mv` (with movement synchronization) requires a custom function:

```python
initMVIndividuals(icls, light-list-sub-route, sub-route)
```

This method creates a custom `individual` to represent where the light resource will separate and join the heavy resource for its delivery, the actual light resource delivery, and the heavy resource delivery. 

##### Parameters

- `icls` - The class representing the `individual`.
- `light-list-sub-route` - The corresponding binary list indicating which customers are light deliverable in the sub-route.
- `sub-route` - A sub-route from the best individual of `py-ga-VRPTW` stage.

##### Returns

- A properly classed `individual` ready to be used with the `deap` operators and algorithms.

### Evaluation of Individuals with Movement Synchronization

```python
evalTSPMS(MVIndividual, instance, unitCost=1.0, initCost=0, waitCost=0, delayCost=0, lightUnitCost=0.1, lightInitCost=0, lightWaitCost=0, lightDelayCost=0)
```

takes in the customized `individual` and the associated cost variables as parameters and calculates the total cost of `individual`. It incorporates wait costs of the resources accordingly. For example, if the light resource arrives at the rendezvous customer before the heavy resource, then there is a wait cost associated with the time the light resource spends waiting, and vice versa.

#### Parameters

- `MVIndividual` - A customized `individual` representing a route with both light and heavy resource.
- `instance` - A problem instance dict object, which can be loaded from a JSON format file.
- `unitCost` - The cost per unit distance for the heavy resource
- `initCost` - The one time initialization cost of the heavy resource
- `waitCost` - The cost per unit time when the heavy resource has to wait to make the delivery or for the light resource to arrive
- `delayCost` - The cost per unit time when the heavy resource is late to make the delivery
- `lightUnitCost` - the cost per unit distance for the light resource
- `lightInitCost` - The one time initialization cost for the light resource
- `lightWaitCost` - The cost per unit time when the light resource has to wait to make the delivery or for the heavy resource to arrive
- `lightDelayCost` - The cost per unit time when the light resource is late to make the delivery

#### Returns

- A tuple containing the fitness value of the `individual`.

### Crossover of Individuals with Movement Synchronization

```python
cxSinglePointSwap(ind1, ind2)
```

executes a single point crossover between rendezvous customers of light sub-routes of the two `individuals` based on probability. 

#### Parameters

- `ind` - A customized `individual` representing a route with both light and heavy resource

#### Returns

- Two individuals with randomly swapped rendezvous points for the light resource sub-routes

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
├── gatspmv/
│   ├── __init__.py
│   ├── mvcore.py
├── gavrptw/
│   ├── __init__.py
│   ├── core.py
│   └── utils.py
├── instance_run_scripts/
|   ├── __init__.py
|   ├── <instance name>.py
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

[repository]: https://github.com/paulliwali/py-ga-VRPTW "paulliwali/py-ga-VRPTW"
[license]: https://github.com/paulliwali/py-ga-VRPTW/blob/master/LICENSE "License"

[multiprocessing]: https://docs.python.org/2/library/multiprocessing.html "multiprocessing"

[solomon]: http://web.cba.neu.edu/~msolomon/problems.htm "Solomon's VRPTW Benchmark Problems"
[100-customers]: http://www.sintef.no/projectweb/top/vrptw/solomon-benchmark/100-customers/ "100 Customers Instance Definitions"
[100-customers-zip]: http://www.sintef.no/globalassets/project/top/vrptw/solomon/solomon-100.zip "100 Customers Instance Definitions (Zip)"

[deap-docs]: http://deap.readthedocs.org/ "Distributed Evolutionary Algorithms in Python (DEAP) Docs"
[deap-github]: https://github.com/deap/deap/ "Distributed Evolutionary Algorithms in Python (DEAP) GitHub"
[deap-pypi]: https://pypi.python.org/pypi/deap/ "Distributed Evolutionary Algorithms in Python (DEAP) PyPI"

[goldberg-1985]: https://books.google.ca/books?hl=en&lr=&id=lI17AgAAQBAJ&oi=fnd&pg=PA154&dq=Alleles,+loci,+and+the+traveling+salesman+problem&ots=0LkXa9L20z&sig=Q7f4TPgLODK_h9uSF0dLUvkgn5M#v=onepage&q=Alleles%2C%20loci%2C%20and%20the%20traveling%20salesman%20problem&f=false "Alleles Loci and the Traveling Salesman Problem"