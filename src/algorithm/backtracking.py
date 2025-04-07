def isConflict(KB, solution, index, empties_dict, empties_set):
    for clause in KB:
        clause_true = False
        for literal in clause:
            abs_literal = abs(literal)

            # Skip literals that are not empty cells.
            if abs_literal not in empties_set:
                continue

            # Check if the literal has already been assigned a value.
            pos = empties_dict[abs_literal]
            if pos >= index:
                clause_true = True
                break

            # Get the current value of the literal from the solution.
            literal_value = solution[pos]

            # Check if the literal satisfies the clause.
            if (literal > 0 and literal_value) or (literal < 0 and not literal_value):
                clause_true = True
                break

        if not clause_true:
            return True  # Return True if any clause is unsatisfied
    return False  # Return False if all clauses are satisfied


def solveBacktracking(KB, empties):
    length = len(empties)
    empties_list = list(empties)
    empties_dict = {
        empties_list[i]: i for i in range(length)
    }  # Fast lookup via dictionary
    empties_set = set(empties_list)

    def backtrack(solution, index):
        if index == length:
            return solution

        # Start with False
        solution[index] = False
        if not isConflict(KB, solution, index + 1, empties_dict, empties_set):
            result = backtrack(solution, index + 1)
            if result:
                return result

        # Then try True
        solution[index] = True
        if not isConflict(KB, solution, index + 1, empties_dict, empties_set):
            result = backtrack(solution, index + 1)
            if result:
                return result

        # If no solution is found, backtrack
        solution[index] = None
        return None

    solution = [None] * length
    solution = backtrack(solution, 0)

    if solution is None:
        return None  # Return None if no solution is found

    # Create the model from the solution
    model = [
        cell_position if solution[i] else -cell_position
        for i, cell_position in enumerate(empties_list)
    ]

    return model
