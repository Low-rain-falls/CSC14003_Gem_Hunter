from pysat.formula import CNF
from pysat.solvers import Solver


def solveByPysat(KB):
    cnf = CNF(from_clauses=KB)
    with Solver(bootstrap_with=cnf) as solver:
        if solver.solve():
            return solver.get_model()
    return None
