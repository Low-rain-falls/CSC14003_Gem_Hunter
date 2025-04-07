import os
import sys
import traceback

from algorithm.solvers import solveGemHunter
from utils.filehandle import (inputMatrix, outputCNFs, outputMatrix,
                              printTwoMatrixes)
from utils.helper import hashModel, updateMatrix

# Get the project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_ALGORITHM = {
    "pysat": "pysat",
    "backtracking": "backtracking",
    "bruteforce": "bruteforce",
}

_TEST_CASES = {
    "5x5": os.path.join(PROJECT_ROOT, "testcases", "5x5"),
    "11x11": os.path.join(PROJECT_ROOT, "testcases", "11x11"),
    "20x20": os.path.join(PROJECT_ROOT, "testcases", "20x20"),
}


def readArgs(argv):
    algorithms = ", ".join(_ALGORITHM.keys())
    testcases = ", ".join(_TEST_CASES.keys())

    if len(argv) < 3:
        print("\nUsage: python main.py <algorithm> <test_case>")
        print(f"- algorithm: {algorithms}")
        print(f"- test_case: {testcases}")
        return None, None

    algorithm = argv[1]
    testcase = argv[2]

    if algorithm not in _ALGORITHM:
        print(f"Algorithm {algorithm} not found")
        print(f"Available: {algorithms}")
        return None, None, None

    if testcase not in _TEST_CASES:
        print(f"Test case {testcase} not found")
        print(f"Available: {testcases}")
        return None, None, None

    return algorithm, testcase


def implement(argv, print_matrix=True):
    algorithm, testcase = readArgs(argv)
    if testcase is None or algorithm is None:
        return

    # Đọc file input và output.
    input_file = os.path.join(_TEST_CASES[testcase], "input.txt")
    output_file = os.path.join(_TEST_CASES[testcase], "output.txt")
    output_CNFs_file = os.path.join(_TEST_CASES[testcase], "CNFs.txt")

    matrix = inputMatrix(input_file)
    original_matrix = [row.copy() for row in matrix]

    # Giải bài toán.
    model, logging_info, CNFs, elapsed_time = solveGemHunter(matrix, algorithm)
    solution = updateMatrix(matrix, model)

    # Xuất kết quả.
    if CNFs is not None:
        outputCNFs(CNFs, output_CNFs_file)

    if solution is not None:
        outputMatrix(solution, output_file)
    else:
        outputMatrix([[""]], output_file)

    # In input và output ra console
    print(f"\n{printTwoMatrixes(original_matrix, solution)}") if print_matrix else None

    # In thông tin ra console
    print(
        f"Test {testcase.lower()}: {logging_info['CNFs']} CNFs - {logging_info['empties']} empty cells"
    )
    if model is None:
        print("No solution found!.")
    else:
        print(
            f"Result hash: #{hashModel(model)} - {len([x for x in model if x > 0])} traps."
        )
    print(f"Algorithm: {algorithm.upper()} - {elapsed_time:.4f} ms. Terminating...")

    return testcase, algorithm, elapsed_time, logging_info, model


if __name__ == "__main__":
    try:
        implement(sys.argv)
    except Exception as error:
        print(f"Error: {error}")
        print("Traceback:")
        traceback.print_exc()
