def isConflict(KB, solution, index, empties_dict, empties_set):
    # Có chứa một clause nào mà không thõa mãn thì trả về True.
    # Clause không thõa mãn khi tất cả các literal đều False.

    for clause in KB:
        clause_true = False
        for literal in clause:
            abs_literal = abs(literal)

            # Nếu literal không phải là ô trống thì bỏ qua.
            if abs_literal not in empties_set:
                continue

            # Nếu literal là ô trống và chưa tới lượt gán giá trị thì bỏ qua clause.
            pos = empties_dict[abs_literal]
            if pos >= index:
                clause_true = True
                break

            # Lấy giá trị hiện tại của literal từ solution.
            literal_value = solution[pos]

            # Kiểm tra xem literal có làm clause true không.
            if (literal > 0 and literal_value) or (literal < 0 and not literal_value):
                clause_true = True
                break

        if not clause_true:
            return True
    return False


def solveBacktracking(KB, empties):

    length = len(empties)
    empties_list = list(empties)

    # Tra cứu vị trí nhanh thông qua 1 dictionary.
    empties_dict = {}
    for i in range(length):
        position = empties_list[i]
        empties_dict[position] = i

    empties_set = set(empties_list)

    def backtrack(solution, index):
        if index == length:
            return solution

        # Bắt đầu với False.
        solution[index] = False
        if not isConflict(KB, solution, index + 1, empties_dict, empties_set):
            result = backtrack(solution, index + 1)
            if result is not None:
                return result

        # Kế tiếp là True.
        solution[index] = True
        if not isConflict(KB, solution, index + 1, empties_dict, empties_set):
            result = backtrack(solution, index + 1)
            if result is not None:
                return result

        # Nếu không tìm được lời giải, reset lại giá trị và backtrack.
        solution[index] = None
        return None

    solution = [None] * length
    solution = backtrack(solution, 0)

    if solution is None:
        return None

    # Tạo mô hình kết quả
    # Nếu giá trị là True, thêm vị trí dưới dạng số dương
    # Nếu giá trị là False, thêm vị trí dưới dạng số âm
    model = []
    for i in range(length):
        cell_position = empties_list[i]
        if solution[i]:
            model.append(cell_position)  # Literal > 0
        else:
            model.append(-cell_position)  # Literal < 0

    return model
