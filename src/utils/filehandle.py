import os


def readFileLines(filename):
    """Reads all lines from a file and returns them as a list."""
    abs_path = os.path.abspath(filename)

    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"Input file not found: {abs_path}")

    with open(filename, "r") as reader:
        return reader.readlines()


def parseCell(cell):
    """Parse a single cell value from the input file."""
    if cell == "_":
        return None
    elif cell == "T" or cell == "G":
        return cell
    elif cell.isnumeric():
        val = int(cell)
        if 1 <= val <= 8:
            return val
        else:
            raise ValueError("Out of range(1-8)!")
    else:
        raise ValueError("Invalid input")


def inputMatrix(filename="./testcases/input.txt"):
    """Reads and parses the input matrix from the file."""
    lines = readFileLines(filename)

    matrix = [[parseCell(cell.strip()) for cell in line.split(",")] for line in lines]
    return matrix


def writeMatrixToFile(matrix, filename):
    """Writes a matrix to the specified file."""
    with open(filename, "w") as writer:
        for row in matrix:
            writer.write(
                ", ".join([str(cell) if cell is not None else "_" for cell in row])
                + "\n"
            )


def outputMatrix(matrix, filename="./testcases/output.txt"):
    """Outputs the matrix to a file."""
    writeMatrixToFile(matrix, filename)


def outputCNFs(KB, filename="./testcases/CNFs.txt"):
    """Outputs the CNFs to a file."""
    with open(filename, "w") as writer:
        for clause in KB:
            writer.write(" ".join([str(x) for x in clause]) + "\n")


def printTwoMatrixes(matrix1, matrix2):
    """Returns a string representation of two matrices side by side."""
    result = ""

    if matrix2 is None:
        for row in matrix1:
            result += (
                ", ".join([str(x) if x is not None else "_" for x in row])
                + "  |  "
                + ", ".join(["_" for _ in row])
                + "\n"
            )
    else:
        for r1, r2 in zip(matrix1, matrix2):
            result += (
                ", ".join([str(x) if x is not None else "_" for x in r1])
                + "  |  "
                + ", ".join([str(x) if x is not None else "_" for x in r2])
                + "\n"
            )

    return result
