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


# Returns a reduced cost matrix (0s in every row and col with the adjusted differences) for a given cost matrix
def reduce_cost_matrix(matrix):
    # Find zero and difference for each row
    row_mins = matrix.min(axis=1)

    for i in range(len(row_mins)):
        matrix[i, :] -= row_mins[i]

    # Find zero and difference for each col
    col_mins = matrix.min(axis=0)

    for i in range(len(col_mins)):
        matrix[:, i] -= col_mins[i]

    return matrix


matrix = reduce_cost_matrix(matrix)

print(matrix)
