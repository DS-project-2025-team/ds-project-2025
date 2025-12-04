from entities.sat_formula import SatFormula


def get_interval(formula: SatFormula) -> tuple[int, int]:
    """
    Return the interval [begin, end) of all possible assignments for the given formula.
    """
    n = formula.max_variable()

    return (0, 2**n)
