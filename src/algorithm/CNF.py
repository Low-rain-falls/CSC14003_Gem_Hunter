from utils.helper import getNeighbors, paddingMatrix, subsets_of, to_1D


def generateExactTrapsClauses(cells, k):
    """
    Generate CNF clauses to represent exactly k traps within the given cells.

    Args:
        cells (List[int]): List of cell IDs.
        k (int): Number of traps.

    Returns:
        List[List[int]]: CNF clauses.
    """
    clauses = []

    # At most k traps: For every subset of size k+1,
    # at least one cell must not be a trap.
    if k < len(cells):
        for subset in subsets_of(cells, k + 1):
            clauses.append([-x for x in subset])

    # At least k traps: For every subset of size n-k+1,
    # at least one cell must be a trap.
    if k > 0:
        n = len(cells)
        for subset in subsets_of(cells, n - k + 1):
            clauses.append(subset)

    return clauses


def getCNFClause(matrix):
    """
    Generate CNF clauses from the input matrix.

    Args:
        matrix (List[List[Union[int, str, None]]]): The game map.

    Returns:
        List[List[int]]: CNF clauses.
    """
    if not matrix or not matrix[0]:
        return []

    padded_matrix = paddingMatrix(matrix)
    clauses = []
    n_rows, n_cols = len(padded_matrix), len(padded_matrix[0])
    original_cols = len(matrix[0])

    for i in range(1, n_rows - 1):
        for j in range(1, n_cols - 1):
            value = padded_matrix[i][j]

            # Only generate clauses for number cells
            if isinstance(value, int):
                known_traps = getNeighbors(padded_matrix, [i, j], lambda x: x == "T")
                unknown_cells = getNeighbors(padded_matrix, [i, j], lambda x: x is None)

                remaining_traps = value - len(known_traps)

                unknown_ids = [
                    to_1D((x - 1, y - 1), original_cols) for x, y in unknown_cells
                ]

                if unknown_ids:
                    clauses.extend(
                        generateExactTrapsClauses(unknown_ids, remaining_traps)
                    )

    # Remove duplicates and sort clauses
    unique_clauses = set(tuple(clause) for clause in clauses)
    sorted_clauses = [list(clause) for clause in unique_clauses]
    sorted_clauses.sort(key=lambda x: (len(x), x))

    return sorted_clauses
