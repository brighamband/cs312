"""
Helpers file for branch and bound algorithm
"""

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
        if other.lower_bound > self.lower_bound:
            return other
        return self

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

    def add_path_and_update_matrix(self, row_idx, col_idx):
        # Update parent bound to now have updated cost
        self.lower_bound += self.cost_matrix[row_idx, col_idx]

        # Eliminate chosen row (set to inf)
        self.cost_matrix[row_idx, :] = math.inf

        # Eliminate chosen col (set to inf)
        self.cost_matrix[:, col_idx] = math.inf

        # Eliminate the opposite cell (don't let it go back)
        last_path = len(self.cost_matrix[0]) == len(
            self.route
        )  # FIXME - Add in logic that checks to see if all nodes have been visited and it can go back
        if not last_path:
            self.cost_matrix[col_idx][row_idx] = math.inf

        # Reduce cost matrix again
        self.reduce_cost_matrix()


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
