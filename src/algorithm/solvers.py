import timeit

from algorithm.backtracking import solveBacktracking
from algorithm.bruteforce import solveBruteForce
from algorithm.CNF import getCNFClause
from algorithm.pysat import solveByPysat
from utils.helper import paddingMatrix, to_1D


def solveGemHunter(matrix, algorithm="pysat", measure_time=True):

    KB = getCNFClause(matrix)
    KB_reversed = [clause.copy() for clause in KB]

    padded_matrix = paddingMatrix(matrix)
    n = len(padded_matrix)
    m = len(padded_matrix[0])

    # Tìm các ô trống (None).
    empties = set()
    for i in range(1, n - 1):
        for j in range(1, m - 1):
            if padded_matrix[i][j] == None:
                empties.add(to_1D((i - 1, j - 1), m - 2))

    # Tìm các ô chứa số (1-9).
    numbers = {}
    for i in range(1, n - 1):
        for j in range(1, m - 1):
            if type(padded_matrix[i][j]) is int:
                numbers[(i - 1, j - 1)] = padded_matrix[i][j]

    logging_info = {
        "algorithm": algorithm,
        "CNFs": len(KB),
        "empties": len(empties),
    }

    func, args = None, None
    if algorithm == "pysat":
        func = solveByPysat
        args = [KB]
    elif algorithm == "backtracking":
        func = solveBacktracking
        args = [KB, empties]
    elif algorithm == "bruteforce":
        func = solveBruteForce
        args = [KB, empties, numbers]
    else:
        raise ValueError("Invalid Algorithm!\n")

    start, end, measured_time = 0, 0, 0

    if measure_time:
        start = timeit.default_timer()
        model = func(*args)
        end = timeit.default_timer()
        measured_time = (end - start) * 1000
    else:
        model = func(*args)

    if model is not None:
        model = [x for x in model if x in empties or -x in empties]
        for empty in empties:
            if empty not in model:
                model.append(-empty)

        model = list(set(model))
        model.sort(key=lambda x: abs(x))
        logging_info["traps"] = len([x for x in model if x > 0])
        return model, logging_info, KB_reversed, measured_time

    return None, logging_info, KB_reversed, measured_time
