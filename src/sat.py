from collections.abc import Iterable


def check_cnf_formula_with_interval(
    clauses: Iterable[Iterable[int]], begin: int, end: int
) -> bool:
    """
    Check the CNF formula with all assignments in [begin, end).

    Args:
        clauses (Iterable[Iterable[int]]):
            List of clauses in the form [(1, -2), (-1, 3)].
            For example, the clause (1, -2) represents (x1 OR NOT x2).
        begin (int): start of the interval (inclusive).
        end (int): end of the interval (exclusive).

    Returns:
        bool: Satisfiability of the CNF formula in the given interval
    """

    return any(
        check_cnf_formula(clauses, assignment) for assignment in range(begin, end)
    )


def check_cnf_formula(clauses: Iterable[Iterable[int]], assignment: int) -> bool:
    return all(check_clause(clause, assignment) for clause in clauses)


def check_clause(literals: Iterable[int], assignment: int) -> bool:
    return any(check_literal(literal, assignment) for literal in literals)


def check_literal(literal: int, assignment: int) -> bool:
    if literal == 0:
        raise ValueError("Literal cannot be zero")

    i = 1 << (abs(literal) - 1)
    value = assignment & i

    if literal < 0:
        return value == 0

    return value > 0
