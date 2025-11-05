from collections.abc import Iterable


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
