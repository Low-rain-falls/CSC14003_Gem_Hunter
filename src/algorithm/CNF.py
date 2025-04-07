from utils.helper import getNeighbors, paddingMatrix, subsets_of, to_1D


def generateExactTrapsClauses(cells, k):
    at_most_clauses = []
    if k < len(cells):
        subsets = subsets_of(cells, k + 1)

        # Đối với mỗi tập con có k + 1 phần tử, tạo mệnh đề "it nhất một ô không phải bẫy".
        for subset in subsets:
            at_most_clauses.append(
                [-x for x in subset]
            )  # Phủ định để biểu diễn "không phải bẫy".

    # "Có ít nhất k ô bẫy trong n ô" <=> "Với mỗi n - k + 1 ô, có ít nhất một ô là bẫy".
    at_least_clauses = []
    if k > 0:
        n = len(cells)
        subsets = subsets_of(cells, n - k + 1)

        # Mệnh đề "ít nhất một ô là bẫy" không cần phủ định.
        at_least_clauses = subsets

    return at_most_clauses + at_least_clauses


def getCNFClause(matrix):
    # Kiểm tra ma trận đầu vào
    if not matrix or not matrix[0]:
        return []

    padded_matrix = paddingMatrix(matrix)
    clauses = []
    n_rows = len(padded_matrix)
    n_cols = len(padded_matrix[0])
    original_cols = len(matrix[0])

    for i in range(1, n_rows - 1):
        for j in range(1, n_cols - 1):
            cell_value = padded_matrix[i][j]

            if isinstance(cell_value, int):

                traps = getNeighbors(padded_matrix, [i, j], lambda x: x == "T")

                remaining_traps = cell_value - len(traps)

                unknown_cells = getNeighbors(padded_matrix, [i, j], lambda x: x is None)

                unknown_ids = [
                    to_1D((position[0] - 1, position[1] - 1), original_cols)
                    for position in unknown_cells
                ]

                if unknown_ids:
                    cnf_clauses = generateExactTrapsClauses(
                        unknown_ids, remaining_traps
                    )
                    clauses.extend(cnf_clauses)

    unique_clauses = set(tuple(clause) for clause in clauses)
    sorted_clauses = [list(clause) for clause in unique_clauses]

    # Sắp xếp theo độ dài mệnh đề (ngắn trước) và giá trị
    sorted_clauses.sort(key=lambda x: (len(x), x))

    return sorted_clauses
