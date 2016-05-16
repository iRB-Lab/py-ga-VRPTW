# py-ga-VRPSTW
A Python Implementation of a Genetic Algorithm-based Solution to Vehicle Routing Problem with Soft Time Windows (VRPSTW)

## Solomon's VRPTW Benchmark Problems
> R1-type|C1-type|RC1-type|R2-type|C2-type|RC2-type
> -------|-------|--------|-------|-------|--------
> I generated six sets of problems. Their design highlights several factors that affect the behavior of routing and scheduling algorithms. They are:
> 
> * geographical data;
> * the number of customers serviced by a vehicle;
> * percent of time-constrained customers; and
> * tightness and positioning of the time windows.
> 
> The geographical data are randomly generated in problem sets R1 and R2, clustered in problem sets C1 and C2, and a mix of random and clustered structures in problem sets by RC1 and RC2. Problem sets R1, C1 and RC1 have a short scheduling horizon and allow only a few customers per route (approximately 5 to 10). In contrast, the sets R2, C2 and RC2 have a long scheduling horizon permitting many customers (more than 30) to be serviced by the same vehicle.
> 
> The customer coordinates are identical for all problems within one type (i.e., R, C and RC). The problems differ with respect to the width of the time windows. Some have very tight time windows, while others have time windows which are hardly constraining. In terms of time window density, that is, the percentage of customers with time windows, I created problems with 25, 50, 75 and 100% time windows.
> 
> The larger problems are 100 customer euclidean problems where travel times equal the corresponding distances. For each such problem, smaller problems have been created by considering only the first 25 or 50 customers.
> 
> (Source: [Solomon's web page](http://web.cba.neu.edu/~msolomon/problems.htm))

### Instance Definitions
See [Solomon's web page](http://web.cba.neu.edu/~msolomon/problems.htm).  
As a backup, you will find a zip-file with the 100 instance definitions [here](http://www.sintef.no/globalassets/project/top/vrptw/solomon/solomon-100.zip).

**Below is a description of the format of the text file that defines each problem instance (assuming 100 customers).**

* All constants are integers.
* `CUST NO.` 0 denotes the depot, where all vehicles must start and finish.
* `K` is the maximum number of vehicles.  
* `Q` the capacity of each vehicle.
* `READY TIME` is the earliest time at which service may start at the given customer/depot.
* `DUE DATE` is the latest time at which service may start at the given customer/depot.
* The value of time is equal to the value of distance.

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
  ...     ...        ...        ...        ...         ...           ...  
  100     x100      y100       q100       e100        l100          s100
```

## GA Implementation
**Distributed Evolutionary Algorithms in Python (DEAP)**

* Docs: [http://deap.readthedocs.org/](http://deap.readthedocs.org/)
* GitHub: [https://github.com/deap/deap/](https://github.com/deap/deap/)
* PyPI: [https://pypi.python.org/pypi/deap/](https://pypi.python.org/pypi/deap/)

```
Sample code coming soon...
```

## References
1. [Solomon's VRPTW Benchmark Problems](http://web.cba.neu.edu/~msolomon/problems.htm)
2. [100 Customers Instance Definitions](http://www.sintef.no/projectweb/top/vrptw/solomon-benchmark/100-customers/)
3. [Distributed Evolutionary Algorithms in Python (DEAP)](https://pypi.python.org/pypi/deap/)
