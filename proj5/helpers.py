import numpy as np
import math

matrix = np.array(
    [
        [math.inf, 5, 4, 3],
        [3, math.inf, 8, 2],
        [5, 3, math.inf, 9],
        [6, 4, 3, math.inf],
    ]
)

lower_bound = 0

# Returns a reduced cost matrix (0s in every row and col with the adjusted differences) for a given cost matrix
def reduce_cost_matrix(matrix, lower_bound):
    # Find zero and difference for each row
    row_mins = matrix.min(axis=1)

    for i in range(len(row_mins)):
        if row_mins[i] != math.inf:  # Skip over eliminated rows
            matrix[i, :] -= row_mins[i]
            lower_bound += row_mins[i]

    # Find zero and difference for each col
    col_mins = matrix.min(axis=0)

    for i in range(len(col_mins)):
        if col_mins[i] != math.inf:  # Skip over eliminated cols
            matrix[:, i] -= col_mins[i]
            lower_bound += col_mins[i]

    return matrix, lower_bound


matrix, lower_bound = reduce_cost_matrix(matrix, lower_bound)

print(matrix, lower_bound)


def add_path_and_update_matrix(matrix, row_idx, col_idx, parent_bound):
    # Update parent bound to now have updated cost
    parent_bound += matrix[row_idx, col_idx]

    # Eliminate chosen row (set to inf)
    matrix[row_idx, :] = math.inf

    # Eliminate chosen col (set to inf)
    matrix[:, col_idx] = math.inf

    # Eliminate the opposite cell (don't let it go back)
    last_path = False  # FIXME - Add in logic that checks to see if all nodes have been visited and it can go back
    if not last_path:
        matrix[col_idx][row_idx] = math.inf

    # Reduce cost matrix again
    matrix, parent_bound = reduce_cost_matrix(matrix, parent_bound)

    return matrix, parent_bound


# FIXME - NEED TO ACCOUNT FOR FACT THAT NAMES DO NOT CORRESPOND WITH INDICES
matrix, lower_bound = add_path_and_update_matrix(matrix, 0, 2, lower_bound)

print(matrix, lower_bound)

from queue import PriorityQueue
q = PriorityQueue()

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
    
# branch_and_bound(0)