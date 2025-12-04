from entities.sat_formula import SatFormula


def get_interval(formula: SatFormula) -> tuple[int, int]:
    """
    Return the interval [begin, end) of all possible assignments for the given formula.
    """
    n = formula.max_variable()

    return (0, 2**n)


def get_subinterval(interval_size: int, i: int) -> tuple[int, int]:
    """
    Return the i-th subinterval of size interval_size.
    The whole interval is assume to be [0, interval_size * n) for some n.

    Args:
        interval_size (int): Size of each subinterval
        i (int): Subinterval index, starting from 0

    Returns:
        tuple[int, int]: Subinterval as [begin, end)
    """

    begin = i * interval_size
    end = (i + 1) * interval_size

    return (begin, end)
