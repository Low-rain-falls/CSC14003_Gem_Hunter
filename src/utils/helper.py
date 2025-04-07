from itertools import combinations


def paddingMatrix(matrix):
    if not matrix:
        return []

    char = "*"
    m = len(matrix[0])
    padded_matrix = [[char] * (m + 2)]  # Top padding row

    for row in matrix:
        padded_matrix.append([char] + row + [char])  # Add left and right padding

    padded_matrix.append([char] * (m + 2))  # Bottom padding row

    return padded_matrix


def getNeighbors(matrix, position, condition=None):
    r, c = position
    neighbors = [
        [r + i, c + j]
        for i in range(-1, 2)
        for j in range(-1, 2)
        if not (i == 0 and j == 0)  # Skip the current cell
        and (condition is None or condition(matrix[r + i][c + j]))
    ]
    return neighbors


def to_1D(position, numCols):
    return position[0] * numCols + position[1] + 1


def subsets_of(arr, k):
    arr = sorted(set(arr))  # Remove duplicates and sort
    return [list(combo) for combo in combinations(arr, k)]


def updateMatrix(matrix, model):
    if not model:
        return None

    n_rows, n_cols = len(matrix), len(matrix[0])
    for i in range(n_rows):
        for j in range(n_cols):
            if matrix[i][j] is None:
                index = i * n_cols + j + 1
                matrix[i][j] = "T" if index in model else "G"

    return matrix


def hashModel(model):
    if not model:
        return None
    return sum(
        1 << i for i in range(len(model)) if model[i] > 0
    )  # Efficient bitwise sum
