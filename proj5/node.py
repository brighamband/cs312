"""
Helpers file for branch and bound algorithm
"""

from TSPClasses import TSPSolution
import numpy as np
import math
import copy


# Node containing state in the Branch and Bound Tree
class Node:
    def __init__(self, lower_bound, cost_matrix, route):
        self.lower_bound = lower_bound
        self.cost_matrix = copy.deepcopy(cost_matrix)
        self.route = copy.deepcopy(route)

    def __lt__(self, other):
        self_depth_left = np.shape(self.cost_matrix)[0] - len(self.route)
        other_depth_left = np.shape(other.cost_matrix)[0] - len(other.route)

        # If one node has to go 5 or less to go deeper than another
        if np.abs(self_depth_left - other_depth_left) >= 5:
            if other_depth_left < self_depth_left:
                return False  # Choose other
            return True  # Choose self

        # Else base it solely off lower bounds
        return self.lower_bound <= other.lower_bound

    # Returns a reduced cost matrix (0s in every row and col with the adjusted differences) for a given cost matrix
    def reduce_cost_matrix(self):
        # Find zero and difference for each row
        row_mins = self.cost_matrix.min(axis=1)

        for i in range(len(row_mins)):
            if row_mins[i] != math.inf:  # Skip over eliminated rows
                self.cost_matrix[i, :] -= row_mins[i]
                self.lower_bound += row_mins[i]

        # Find zero and difference for each col
        col_mins = self.cost_matrix.min(axis=0)

        for i in range(len(col_mins)):
            if col_mins[i] != math.inf:  # Skip over eliminated cols
                self.cost_matrix[:, i] -= col_mins[i]
                self.lower_bound += col_mins[i]

    def update_child_matrix(self, row_idx, col_idx):
        # Update parent bound to now have updated cost
        self.lower_bound += self.cost_matrix[row_idx, col_idx]

        # Eliminate chosen row (set to inf)
        self.cost_matrix[row_idx, :] = math.inf

        # Eliminate chosen col (set to inf)
        self.cost_matrix[:, col_idx] = math.inf

        # Eliminate the opposite cell (don't let it go back)
        last_path = len(self.route) == np.shape(
            self.cost_matrix[0]
        )  # FIXME - Add in logic that checks to see if all nodes have been visited and it can go back
        if not last_path:
            self.cost_matrix[col_idx][row_idx] = math.inf

        # Reduce cost matrix again
        self.reduce_cost_matrix()

    # Returns a queue of children nodes from a given parent
    def expand(self, cities):
        parent_city = self.route[-1]

        child_nodes = []

        # Get all children from parent (look through each column for parent row)
        for child_i in range(len(cities)):
            # Skip over own cities and any ones that you cannot access from own
            if self.cost_matrix[parent_city._index, child_i] == math.inf:
                continue

            # Initialize child as parent
            child_node = Node(self.lower_bound, self.cost_matrix, self.route)

            # Add city to route
            child_node.route.append(cities[child_i])

            # Infinity out row and col for current city and update lower bound
            child_node.update_child_matrix(parent_city._index, child_i)

            child_nodes.append(child_node)

        return child_nodes

    # Returns infinity if incomplete route, then returns the cost if complete
    def test_complete_route(self):
        # Complete if it includes all cities and last has edge back to first
        if (
            len(self.route) == np.shape(self.cost_matrix[0])
            and self.route[-1].costTo(self.route[0]) < math.inf
        ):
            return TSPSolution(self.route)
        return math.inf


# TESTING

# matrix = np.array(
#     [
#         [math.inf, 5, 4, 3],
#         [3, math.inf, 8, 2],
#         [5, 3, math.inf, 9],
#         [6, 4, 3, math.inf],
#     ]
# )

# lower_bound = 0


# node = Node(0, matrix, [])
# node.reduce_cost_matrix()
# node.add_path_and_update_matrix(0, 2)

# pass
