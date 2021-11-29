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
from node import Node


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
        found_tour = False
        count = 0
        bssf = None
        start_time = time.time()
        while not found_tour and time.time() - start_time < time_allowance:
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
                found_tour = True
        end_time = time.time()
        results["cost"] = bssf.cost if found_tour else math.inf
        results["time"] = end_time - start_time
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
        found_tour = False
        start_time = time.time()
        route = []

        # Loop through each city
        for start_city in cities:
            route = [start_city]  # Make new route with starting city

            # For each city, try to find a route
            while not found_tour and time.time() - start_time < time_allowance:

                cheapest_neighbor = route[
                    -1
                ]  # Initialize to start city so that costTo is inf
                for neighbor in cities:
                    if neighbor not in route and route[-1].costTo(neighbor) < route[
                        -1
                    ].costTo(cheapest_neighbor):
                        cheapest_neighbor = neighbor

                # If invalid route
                # break out of while loop, move onto next city (increment i)
                if route[-1].costTo(cheapest_neighbor) == math.inf:
                    break

                # Append cheapest neighbor
                route.append(cheapest_neighbor)

                # If valid route (includes all cities and last has edge back to first)
                if len(route) == len(cities) and route[-1].costTo(route[0]) < math.inf:
                    found_tour = True

            if found_tour:
                break

        solution = TSPSolution(route)

        end_time = time.time()
        results["cost"] = solution.cost if found_tour else math.inf
        results["time"] = end_time - start_time
        results["count"] = 1 if found_tour else 0  # Greedy only finds 1
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
        results = {}
        cities = self._scenario.getCities()
        num_cities = len(cities)

        # Make the upper bound be the greedy solution
        greedy_res = self.greedy(time_allowance)
        bssf = greedy_res["cost"]  # Initially set the bssf to be greedy's cost

        # Start timer
        start_time = time.time()

        # Make cost matrix
        matrix = np.zeros((num_cities, num_cities))
        for i in range(np.shape(matrix)[0]):  # Rows
            for j in range(np.shape(matrix)[1]):  # Cols
                matrix[i][j] = cities[i].costTo(cities[j])

        # Make Node class
        node = Node(0, matrix, [])

        # Reduce
        node.reduce_cost_matrix()

        # Make queue with all cities to start

        # q = cities
        # heapq.heapify(q)

        q = []

        START_CITY_ROW = 0  # Matrix costs will be pulled from first row (start city)
        for i in range(num_cities):
            heapq.heappush(
                q, (matrix[START_CITY_ROW][i], cities[i]._elevation, cities[i])
            )

        while len(q) > 0:
            cheapest_city = heapq.heappop(q)
            temp_lower_bound = cheapest_city.lower_bound
            temp_lower_bound = (
                lower_bound + cheapest_city[0]
            )  # Temp is lower before plus prospective cost
            # if temp_lower_bound < bssf:
            # helpers.add_path_and_update_matrix(
            #     matrix,
            # )

        # TEST RANDOM PSEUDO CODE
        # def branch_and_bound(P_O):
        #     q.put(P_O, "random")
        #     bssf = math.inf
        #     while not q.empty():
        #         P = q.get()
        #         if lower_bound(P) < bssf:
        #             T = expand(P)
        #             for i in range(len(T)):
        #                 if test(P[i]) < bssf:
        #                     bssf = test(P[i])
        #                 elif lower_bound(P[i]) < bssf:
        #                     q.put(P[i])
        #     q.put(1, 'first')
        #     q.put(2, 'second')
        #     q.put(4, 'last')
        #     print(q.get())

        # solution = TSPSolution(route)

        end_time = time.time()
        # results["cost"] = solution.cost
        results["time"] = end_time - start_time
        results["count"] = 999  # FIXME - How many times you hit bottom
        # results["soln"] = solution
        results["max"] = None
        results["total"] = None
        results["pruned"] = None
        return results

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
