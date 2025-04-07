from itertools import combinations


def paddingMatrix(matrix):
    """
    Thêm viền quanh ma trận để dễ xử lý. Ví dụ:
                                * * * * *
        1 2 3                   * 1 2 3 *
        4 5 6   sẽ trở thành    * 4 5 6 *
        7 8 9                   * 7 8 9 *
                                * * * * *
    """
    if not matrix or not matrix[0]:
        return []

    char = "*"
    m = len(matrix[0])
    padded_matrix = [[char for _ in range(m + 2)]]

    for row in matrix:
        padded_row = [char] + row + [char]
        padded_matrix.append(padded_row)

    padded_matrix.append([char for _ in range(m + 2)])

    return padded_matrix


def getNeighbors(matrix, position, condition=None):
    """
    Lấy các ô xung quanh ô tại vị trí pos mà thỏa mãn điều kiện.

    Tham số:
    - matrix: ma trận đầu vào
    - pos: vị trí [row, col] của ô cần xét
    - condition: hàm điều kiện để lọc các ô, nếu None thì lấy tất cả các ô

    Trả về:
    - Danh sách các vị trí [row, col] của các ô xung quanh thỏa mãn điều kiện
    """
    [r, c] = position
    neighbor = []

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if condition(matrix[r + i][c + j]) or condition is None:
                neighbor.append([r + i, c + j])

    return neighbor


def to_1D(position, numCols):
    """
    Chuyển từ vị trí (row, col) trong ma trận 2 chiều thành chỉ số trong mảng 1 chiều.

    Tham số:
    - pos: tuple (row, col) chỉ vị trí trong ma trận 2D
    - num_cols: số cột của ma trận 2D gốc (không tính viền)

    Trả về:
    - Chỉ số tương ứng trong mảng 1D, bắt đầu từ 1
    """

    return position[0] * numCols + position[1] + 1


def subsets_of(arr, k):

    arr = list(set(arr))
    arr.sort()

    subsets = []
    for combo in combinations(arr, k):
        subsets.append(list(combo))

    return subsets


def updateMatrix(matrix, model):
    """
    Cập nhật ma trận với kết quả từ model SAT Solver.

    Tham số:
    - matrix: ma trận đầu vào với các ô chưa biết (None)
    - model: kết quả từ SAT Solver, dạng danh sách các biến đúng (dương) và sai (âm)

    Trả về:
    - Ma trận đã được cập nhật, ô nào True thì là "T" (bẫy), False thì là "G" (an toàn)
    """
    if model is None:
        return None
    n_rows = len(matrix)
    n_cols = len(matrix[0])
    for i in range(n_rows):
        for j in range(n_cols):
            if matrix[i][j] is None:
                index = i * n_cols + j + 1
                matrix[i][j] = "T" if index in model else "G"

    return matrix


def hashModel(model):
    """
    Chuyển đổi model thành một số nguyên để dễ lưu trữ/so sánh.

    Tham số:
    - model: kết quả từ SAT Solver, danh sách các literal

    Trả về:
    - Giá trị số nguyên đại diện cho model
    """

    if model is None:
        return None
    num = 0
    for i in range(len(model)):
        if model[i] > 0:
            num |= 1 << i

    return num
