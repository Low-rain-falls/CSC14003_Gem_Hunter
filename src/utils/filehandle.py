import os


def inputMatrix(filename="./testcases/input.txt"):

    abs_path = os.path.abspath(filename)

    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"Input file not found: {abs_path}")

    with open(filename, "r") as reader:
        lines = reader.readlines()

        matrix = []
        for line in lines:
            row = []
            for cell in line.split(","):
                cell = cell.strip()
                if cell == "_":
                    row.append(None)
                elif cell == "T":
                    row.append("T")
                elif cell == "G":
                    row.append("G")
                elif cell.isnumeric():
                    cell = int(cell)
                    if cell < 1 or cell > 8:
                        raise ValueError("Out of range(1-8)!.")
                    row.append(int(cell))
                else:
                    raise ValueError("Invalid input")
            matrix.append(row)
        return matrix


def outputMatrix(matrix, filename="./testcases/output.txt"):

    with open(filename, "w") as writer:
        for row in matrix:
            writer.write(
                ", ".join([str(cell) if cell is not None else "_" for cell in row])
                + "\n"
            )


def outputCNFs(KB, filename="./testcases/CNFs.txt"):

    with open(filename, "w") as writer:
        for clause in KB:
            writer.write(" ".join([str(x) for x in clause]) + "\n")


def printTwoMatrixes(matrix1, matrix2):
    str_matrix = ""
    if matrix2 is None:
        for r1 in matrix1:
            str_matrix += (
                ", ".join([str(x) if x is not None else "_" for x in r1])
                + "  |  "
                + ", ".join(["_" for _ in range(len(r1))])
                + "\n"
            )
        return str_matrix
    else:
        for r1, r2 in zip(matrix1, matrix2):
            str_matrix += (
                ", ".join([str(x) if x is not None else "_" for x in r1])
                + "  |  "
                + ", ".join([str(x) if x is not None else "_" for x in r2])
                + "\n"
            )
        return str_matrix
