def isValid(KB, assignment, length):

    # Có chứa một clause nào mà không thoả mãn thì trả về False
    # Clause không thoả mãn khi tất cả các literal đều False

    literal_cache = {}

    for clause in KB:
        clause_satisfied = False

        for literal in clause:
            var = abs(literal)
            if var not in assignment:
                continue

            # Kiểm tra cache trước
            cache_key = (literal, assignment[var])
            if cache_key in literal_cache:
                clause_satisfied = literal_cache[cache_key]
                if clause_satisfied:
                    break
                continue

            # Tính giá trị và lưu vào cache
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
    empties_list = sorted(list(empties))  # Sắp xếp để đảm bảo thứ tự nhất quán

    # Tính toán giới hạn số bẫy
    sum_numbers = sum(numbers.values())
    min_traps = max(1, sum_numbers // 8)  # Đảm bảo ít nhất 1 bẫy.
    max_traps = min(sum_numbers, length)

    print(f" - Bruteforcing {2**length} cases for {length} empty cells...")
    print(f" - Trap constraints: min={min_traps}, max={max_traps}")

    def generate_assignments(index=0, current_assignment=None, trap_count=0):
        """
        Hàm đệ quy tạo và kiểm tra tất cả các cách gán giá trị có thể.
        """
        if current_assignment is None:
            current_assignment = {}

        # Kiểm tra sớm về số lượng bẫy.
        remaining_cells = length - index
        min_possible_traps = trap_count
        max_possible_traps = trap_count + remaining_cells

        if max_possible_traps < min_traps or min_possible_traps > max_traps:
            return None

        if index == length:
            if min_traps <= trap_count <= max_traps:
                if isValid(KB, current_assignment, length):
                    return [
                        (
                            empties_list[i]
                            if current_assignment[empties_list[i]]
                            else -empties_list[i]
                        )
                        for i in range(length)
                    ]
            return None

        # In tiến độ.
        if index % 24 == 0 and index > 0:
            print(f"  + Processing at depth {index}/{length}...")

        var = empties_list[index]

        # Thử False trước vì thường có ít bẫy hơn.
        current_assignment[var] = False
        result = generate_assignments(index + 1, current_assignment, trap_count)
        if result:
            return result

        # Nếu False không được, thử True.
        current_assignment[var] = True
        result = generate_assignments(index + 1, current_assignment, trap_count + 1)
        if result:
            return result

        del current_assignment[var]
        return None

    return generate_assignments()
