from tabulate import tabulate

from main import implement
from utils.helper import hashModel


def writeResult(result, file="statistic.txt"):
    """Writes the results to a specified file."""
    with open(file, "w") as writer:
        writer.write(result)


def shouldSkipBruteforce(algorithm, model, brute_force_limit):
    """Determines if the bruteforce algorithm should be skipped based on the model's hash."""
    if algorithm == "bruteforce" and model is not None and hashModel(model) is not None:
        return hashModel(model) >= brute_force_limit
    return False


def processTestCase(test_case, result):
    """Runs the algorithms on a test case and stores the results."""
    test_index = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
    test_count = 0
    for test_case in ["5x5", "11x11", "20x20"]:
        print("--------------------")
        print(f"\n{test_index[test_count]}. RUNNING TEST-CASE {test_case.upper()}")
        test_count += 1

        for algorithm in ["pysat", "backtracking", "bruteforce"]:
            print(f"\nRunning algorithm: {algorithm}")

            if shouldSkipBruteforce(algorithm, model, BRUTEFORCE_LIMIT):
                print("Bruteforce algorithm is too slow for this model. Skipping...\n")
                result.append(
                    [
                        test_case,
                        logging_info["CNFs"],
                        logging_info["empties"],
                        len([x for x in model if x > 0]),
                        algorithm,
                        "N/A",
                        hashModel(model),
                    ]
                )
                continue

            # Running the algorithm
            test, algorithm, elapsed_time, logging_info, model = implement(
                ["", algorithm, test_case], False
            )

            # Collect the results
            result.append(
                [
                    test_case,
                    logging_info["CNFs"],
                    logging_info["empties"],
                    len([x for x in model if x > 0]),
                    algorithm,
                    f"{elapsed_time:.4f} ms",
                    hashModel(model),
                ]
            )

            # Write the result to file
            table = tabulate(
                result,
                headers=[
                    "Test case",
                    "CNFs",
                    "Empty cells",
                    "Traps",
                    "Algorithm",
                    "Time",
                    "Model hash (binary)",
                ],
                tablefmt="orgtbl",
            )
            writeResult(table, "./src/statistic.txt")

        result.append(["-" for _ in range(7)])


def main():
    BRUTEFORCE_LIMIT = 4e9

    result = []
    test, algorithm, elapsed_time, logging_info, model = None, None, None, None, None

    processTestCase(test_case, result)

    print("--------------------")
    print("\nBenchmarking completed. Results are saved in benchmark.txt")
    print(table)


if __name__ == "__main__":
    main()
