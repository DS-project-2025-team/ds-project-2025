import pytest

from sat import (
    check_clause,
    check_cnf_formula,
    check_cnf_formula_with_interval,
    check_literal,
)


@pytest.mark.parametrize(
    ("literal", "assignment", "expected"),
    [
        (1, 0b1110, False),
        (3, 0b1011, False),
        (3, 0b0100, True),
        (-1, 0b1111, False),
        (-1, 0b1110, True),
        (-1, 0b0000, True),
    ],
)
def test_check_literal(literal, assignment, expected):
    assert check_literal(literal, assignment) == expected


def test_check_literal_with_zero_fails():
    with pytest.raises(ValueError, match=r"zero"):
        check_literal(0, 0b1010)


@pytest.mark.parametrize(
    ("clause", "assignment", "expected"),
    [
        ((1, 2, 3), 0b100, True),
        ((1, 2, 3), 0b111, True),
        ((1, 2, 3), 0b000, False),
    ],
)
def test_check_clause_with_positive_literals(clause, assignment, expected):
    assert check_clause(clause, assignment) == expected


@pytest.mark.parametrize(
    ("clause", "assignment", "expected"),
    [
        ((-1, 2, -3), 0b111, True),
        ((-1, 2, -3), 0b101, False),
        ((-1, -2, -3), 0b100, True),
        ((-1, -2, -3), 0b000, True),
    ],
)
def test_check_clause_with_negative_literals(clause, assignment, expected):
    assert check_clause(clause, assignment) == expected


@pytest.mark.parametrize(
    ("formula", "assignment", "expected"),
    [
        ([(-1, 2, -3)], 0b111, True),
        ([(-1, 2, -3), (1, 2, 3)], 0b010, True),
        ([(-1, 2, -3), (1, 2, 3)], 0b000, False),
        ([(-1, 2, -3), (2, 3, 5), (1, -4, 5)], 0b000000, False),
    ],
)
def test_check_cnf_formula(formula, assignment, expected):
    assert check_cnf_formula(formula, assignment) == expected


@pytest.mark.parametrize(
    ("formula", "begin", "end", "expected"),
    [
        ([(-1, 2, -3)], 0b000, 0b111, True),
        ([(-1, 2, -3), (1, 2, 3)], 0b000, 0b111, True),
        ([(1, 2), (1, -2), (-1, 2), (-1, -2)], 0b00, 0b11, False),
    ],
)
def test_check_cnf_formula_with_interval(formula, begin, end, expected):
    assert check_cnf_formula_with_interval(formula, begin, end) == expected
