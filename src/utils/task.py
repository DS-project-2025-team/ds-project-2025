from entities.sat_formula import SatFormula


def get_interval(formula: SatFormula) -> tuple[int, int]:
    """
    Return the interval of all possible assignments for the given formula.

    Args:
        formula (SatFormula): SAT formula

    Returns:
        tuple[int, int]: Interval as [begin, end)
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


def get_tasks_from_formula(formula: SatFormula, power: int) -> list[int]:
    """
    Wrapper for get_tasks that takes a formula instead of max_variable.
    """

    return get_tasks(formula.max_variable(), power)


def get_tasks(max_variable: int, power: int) -> list[int]:
    """
    Splits the assignment interval into subintervals of size 2**power.

    Args:
        variables (int): The maximum index of variables in a formula.
        power (int): log(interval_size)

    Returns:
        list[int]: The tasks as indexes of subintervals.
    """

    intervals = max_variable - power

    return list(range(0, 2**intervals))
