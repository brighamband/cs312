#!/usr/bin/python3

from which_pyqt import PYQT_VER

if PYQT_VER == "PYQT5":
    from PyQt5.QtCore import QLineF, QPointF
elif PYQT_VER == "PYQT4":
    from PyQt4.QtCore import QLineF, QPointF
else:
    raise Exception("Unsupported Version of PyQt: {}".format(PYQT_VER))


import time
import numpy as np
from TSPClasses import *
import heapq
import itertools


class TSPSolver:
    def __init__(self, gui_view):
        self._scenario = None

    def setupWithScenario(self, scenario):
        self._scenario = scenario

    """ <summary>
		This is the entry point for the default solver
		which just finds a valid random tour.  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of solution, 
		time spent to find solution, number of permutations tried during search, the 
		solution found, and three null values for fields not used for this 
		algorithm</returns> 
	"""

    def defaultRandomTour(self, time_allowance=60.0):
        results = {}
        cities = self._scenario.getCities()
        ncities = len(cities)
        foundTour = False
        count = 0
        bssf = None
        startTime = time.time()
        while not foundTour and time.time() - startTime < time_allowance:
            # create a random permutation
            perm = np.random.permutation(ncities)
            route = []
            # Now build the route using the random permutation
            for i in range(ncities):
                route.append(cities[perm[i]])
            bssf = TSPSolution(route)
            count += 1
            if bssf.cost < np.inf:
                # Found a valid route
                foundTour = True
        end_time = time.time()
        results["cost"] = bssf.cost if foundTour else math.inf
        results["time"] = end_time - startTime
        results["count"] = count
        results["soln"] = bssf
        results["max"] = None
        results["total"] = None
        results["pruned"] = None
        return results

    """ <summary>
		This is the entry point for the greedy solver, which you must implement for 
		the group project (but it is probably a good idea to just do it for the branch-and
		bound project as a way to get your feet wet).  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution, 
		time spent to find best solution, total number of solutions found, the best
		solution found, and three null values for fields not used for this 
		algorithm</returns> 
	"""

    def greedy(self, time_allowance=60.0):
        results = {}
        cities = self._scenario.getCities()
        num_cities = len(cities)
        foundTour = False
        startTime = time.time()
        route = []

        # Loop through each city
        for startCity in cities:
            route = [startCity]  # Make new route with starting city

            # For each city, try to find a route
            while not foundTour and time.time() - startTime < time_allowance:

                cheapestNeighbor = route[
                    -1
                ]  # Initialize to start city so that costTo is inf
                for neighbor in cities:
                    if neighbor not in route and route[-1].costTo(neighbor) < route[
                        -1
                    ].costTo(cheapestNeighbor):
                        cheapestNeighbor = neighbor

                # If invalid route
                # break out of while loop, move onto next city (increment i)
                if route[-1].costTo(cheapestNeighbor) == math.inf:
                    break

                # Append cheapest neighbor
                route.append(cheapestNeighbor)

                # If valid route (includes all cities and last has edge back to first)
                if len(route) == num_cities and route[-1].costTo(route[0]) < math.inf:
                    foundTour = True

            if foundTour:
                break

        solution = TSPSolution(route)

        end_time = time.time()
        results["cost"] = solution.cost if foundTour else math.inf
        results["time"] = end_time - startTime
        results["count"] = 1 if foundTour else None  # Greedy only finds 1
        results["soln"] = solution
        results["max"] = None
        results["total"] = None
        results["pruned"] = None
        return results

    """ <summary>
		This is the entry point for the branch-and-bound algorithm that you will implement
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution, 
		time spent to find best solution, total number solutions found during search (does
		not include the initial BSSF), the best solution found, and three more ints: 
		max queue size, total number of states created, and number of pruned states.</returns> 
	"""

    def branchAndBound(self, time_allowance=60.0):
        # Make the upper bound be the greedy solution
        greedy_res = self.greedy(time_allowance)
        initial_bssf = greedy_res["cost"]
        pass

    """ <summary>
		This is the entry point for the algorithm you'll write for your group project.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution, 
		time spent to find best solution, total number of solutions found during search, the 
		best solution found.  You may use the other three field however you like.
		algorithm</returns> 
	"""

    def fancy(self, time_allowance=60.0):
        pass
