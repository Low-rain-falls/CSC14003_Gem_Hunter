import timeit

from algorithm.backtracking import solveBacktracking
from algorithm.bruteforce import solveBruteForce
from algorithm.CNF import getCNFClause
from algorithm.pysat import solveByPysat
from utils.helper import paddingMatrix, to_1D


def solveGemHunter(matrix, algorithm="pysat", measure_time=True):
    KB = getCNFClause(matrix)
    KB_copy = [clause.copy() for clause in KB]

    padded_matrix = paddingMatrix(matrix)
    n, m = len(padded_matrix), len(padded_matrix[0])

    empties = {
        to_1D((i - 1, j - 1), m - 2)
        for i in range(1, n - 1)
        for j in range(1, m - 1)
        if padded_matrix[i][j] is None
    }

    numbers = {
        (i - 1, j - 1): padded_matrix[i][j]
        for i in range(1, n - 1)
        for j in range(1, m - 1)
        if isinstance(padded_matrix[i][j], int)
    }

    logging_info = {
        "algorithm": algorithm,
        "CNFs": len(KB),
        "empties": len(empties),
    }

    if algorithm == "pysat":
        solver = solveByPysat
        args = [KB]
    elif algorithm == "backtracking":
        solver = solveBacktracking
        args = [KB, empties]
    elif algorithm == "bruteforce":
        solver = solveBruteForce
        args = [KB, empties, numbers]
    else:
        raise ValueError("Invalid algorithm selected!")

    start_time, end_time = 0, 0

    if measure_time:
        start_time = timeit.default_timer()
        model = solver(*args)
        end_time = timeit.default_timer()
        elapsed_time = (end_time - start_time) * 1000
    else:
        model = solver(*args)
        elapsed_time = 0

    if model is not None:
        model = [x for x in model if x in empties or -x in empties]
        for empty in empties:
            if empty not in model:
                model.append(-empty)

        model = sorted(set(model), key=lambda x: abs(x))
        logging_info["traps"] = len([x for x in model if x > 0])

        return model, logging_info, KB_copy, elapsed_time

    return None, logging_info, KB_copy, elapsed_time
