import time


def isValid(KB, assignment, length):
    literal_cache = {}

    for clause in KB:
        clause_satisfied = False

        for literal in clause:
            var = abs(literal)
            if var not in assignment:
                continue

            cache_key = (literal, assignment[var])
            if cache_key in literal_cache:
                clause_satisfied = literal_cache[cache_key]
                if clause_satisfied:
                    break
                continue

            is_satisfied = (literal > 0 and assignment[var]) or (
                literal < 0 and not assignment[var]
            )
            literal_cache[cache_key] = is_satisfied

            if is_satisfied:
                clause_satisfied = True
                break

        if not clause_satisfied:
            return False

    return True


def solveBruteForce(KB, empties, numbers):
    length = len(empties)
    empties_list = sorted(list(empties))

    sum_numbers = sum(numbers.values())
    min_traps = max(1, sum_numbers // 8)
    max_traps = min(sum_numbers, length)

    print("=" * 50)
    print(f"[INFO] Starting Brute-Force Solver")
    print(f"[INFO] Empty cells: {length}")
    print(f"[INFO] Trap constraints: min = {min_traps}, max = {max_traps}")
    print(f"[INFO] Max assignments to check: {2 ** length}")
    print("=" * 50)

    start_time = time.time()

    def generate_assignments(index=0, current_assignment=None, trap_count=0):
        if current_assignment is None:
            current_assignment = {}

        remaining_cells = length - index
        min_possible_traps = trap_count
        max_possible_traps = trap_count + remaining_cells

        if max_possible_traps < min_traps or min_possible_traps > max_traps:
            return None

        if index == length:
            if min_traps <= trap_count <= max_traps:
                if isValid(KB, current_assignment, length):
                    elapsed = time.time() - start_time
                    print(f"[SUCCESS] Valid assignment found after {elapsed:.2f}s")
                    return [
                        (
                            empties_list[i]
                            if current_assignment[empties_list[i]]
                            else -empties_list[i]
                        )
                        for i in range(length)
                    ]
            return None

        # In tiến độ sau mỗi 5% hoặc mỗi 500 bước
        if index % max(1, length // 20) == 0 and index > 0:
            percent = (index / length) * 100
            elapsed = time.time() - start_time
            print(
                f"  > Progress: {index}/{length} ({percent:.1f}%) - Elapsed: {elapsed:.2f}s"
            )

        var = empties_list[index]

        current_assignment[var] = False
        result = generate_assignments(index + 1, current_assignment, trap_count)
        if result:
            return result

        current_assignment[var] = True
        result = generate_assignments(index + 1, current_assignment, trap_count + 1)
        if result:
            return result

        del current_assignment[var]
        return None

    result = generate_assignments()

    elapsed = time.time() - start_time
    print("=" * 50)
    if result:
        print(f"[INFO] Brute-Force completed in {elapsed:.2f}s")
    else:
        print(f"[WARNING] No valid assignment found after {elapsed:.2f}s")
    print("=" * 50)

    return result
