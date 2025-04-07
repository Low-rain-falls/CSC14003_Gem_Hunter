from pysat.formula import CNF
from pysat.solvers import Solver


# PySAT: https://pysathq.github.io/docs/html/index.html
def solveByPysat(KB):
    """
    Giải bài toán SAT bằng thư viện PySAT
    Input: KB - tập các mệnh đề CNF
    Output: model - một phán định của các biến trong KB
    """
    cnf = CNF(from_clauses=KB)
    with Solver(bootstrap_with=cnf) as solver:
        solver.solve()
        model = solver.get_model()
        return model
