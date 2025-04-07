from main import implement
from tabulate import tabulate
from utils.helper import hashModel


def writeResult(result, file="statistic.txt"):
    with open(file, "w") as writer:
        writer.write(result)


if __name__ == "__main__":
    BRUTEFORCE_LIMIT = 4e9

    result = []
    test, algorithm, elapsed_time, logging_info, model = None, None, None, None, None

    test_index = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
    test_count = 0

    for test_case in ["5x5", "11x11", "20x20"]:
        print("--------------------")
        print(f"\n{test_index[test_count]}. RUNNING TEST-CASE {test_case.upper()}")
        test_count += 1

        alg_count = 0
        for algorithm in ["pysat", "backtracking", "bruteforce"]:
            print(f"\n{alg_count + 1}. Running algorithm {algorithm}")
            alg_count += 1

            if (
                algorithm == "bruteforce"
                and model is not None
                and hashModel(model) is not None
                and hashModel(model) >= BRUTEFORCE_LIMIT
            ):
                print("Bruteforce algorithm is too slow for this model. Skipping...\n")
                result += [
                    [
                        test_case,
                        logging_info["CNFs"],
                        logging_info["empties"],
                        len([x for x in model if x > 0]),
                        algorithm,
                        "N/A",
                        hashModel(model),
                    ]
                ]

            else:
                print(f"Running {algorithm} on test-case {test_case}...")
                test, algorithm, elapsed_time, logging_info, model = implement(
                    ["", algorithm, test_case], False
                )
                result += [
                    [
                        test_case,
                        logging_info["CNFs"],
                        logging_info["empties"],
                        len([x for x in model if x > 0]),
                        algorithm,
                        f"{elapsed_time:.4f} ms",
                        hashModel(model),
                    ]
                ]

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

        result += [["-" for _ in range(7)]]

    print("--------------------")
    print("\nBenchmarking completed. Results are saved in benchmark.txt")
    print(table)
