import os
import sys
import traceback

from algorithm.solvers import solveGemHunter
from utils.filehandle import (inputMatrix, outputCNFs, outputMatrix,
                              printTwoMatrixes)
from utils.helper import hashModel, updateMatrix

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
        print(f"Algorithm '{algorithm}' not found")
        print(f"Available algorithms: {algorithms}")
        return None, None

    if testcase not in _TEST_CASES:
        print(f"Test case '{testcase}' not found")
        print(f"Available test cases: {testcases}")
        return None, None

    return algorithm, testcase


def implement(argv, print_matrix=True):
    algorithm, testcase = readArgs(argv)
    if testcase is None or algorithm is None:
        return

    print("\n" + "=" * 50)
    print(f"{'GEM HUNTER - AI LAB':^50}")
    print("=" * 50)

    input_file = os.path.join(_TEST_CASES[testcase], "input.txt")
    output_file = os.path.join(_TEST_CASES[testcase], "output.txt")
    output_CNFs_file = os.path.join(_TEST_CASES[testcase], "CNFs.txt")

    matrix = inputMatrix(input_file)
    original_matrix = [row.copy() for row in matrix]

    model, logging_info, CNFs, elapsed_time = solveGemHunter(matrix, algorithm)
    solution = updateMatrix(matrix, model)

    if CNFs is not None:
        outputCNFs(CNFs, output_CNFs_file)

    if solution is not None:
        outputMatrix(solution, output_file)
    else:
        outputMatrix([[""]], output_file)

    if print_matrix:
        print("\nInput vs Output Matrix:")
        print("-" * 50)
        print(printTwoMatrixes(original_matrix, solution))
        print("-" * 50)

    print(f"{'Test case':15}: {testcase}")
    print(f"{'Algorithm':15}: {algorithm.upper()}")
    print(f"{'Total CNFs':15}: {logging_info['CNFs']}")
    print(f"{'Empty cells':15}: {logging_info['empties']}")

    if model is None:
        print(f"{'Result':15}: No solution found!")
    else:
        num_traps = len([x for x in model if x > 0])
        print(f"{'Result hash':15}: #{hashModel(model)}")
        print(f"{'Total traps':15}: {num_traps}")

    print(f"{'Elapsed time':15}: {elapsed_time:.4f} ms")

    print("=" * 50)
    print("Terminating...")

    return testcase, algorithm, elapsed_time, logging_info, model


if __name__ == "__main__":
    try:
        implement(sys.argv)
    except Exception as error:
        print(f"Error: {error}")
        print("Traceback:")
        traceback.print_exc()
