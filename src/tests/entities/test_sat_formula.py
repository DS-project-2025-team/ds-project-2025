import pytest

from entities.sat_formula import Clause, SatFormula


@pytest.mark.parametrize(
    "clause",
    [
        (1, 2, 3, 5),
        (-1, -2, -3, 1),
        (2, 7),
        (10,),
    ],
)
def test_clause_length_not_three_throws_error(clause):
    with pytest.raises(ValueError, match=r"3-literal"):
        Clause(clause)


@pytest.mark.parametrize(
    "clause",
    [
        (1, 2, 3),
        (-1, -3, 1),
        (2, 7, 29),
        (10, 99, -134),
    ],
)
def test_clause_length_with_three_can_be_initialized(clause):
    Clause(clause)


@pytest.mark.parametrize(
    "clause",
    [
        (1, 2, 0),
        (-1, -3, 0),
        (2, 0, 29),
        (10, 0, -134),
    ],
)
def test_clause_with_zero_causes_error(clause):
    with pytest.raises(ValueError, match=r"zero"):
        Clause(clause)


@pytest.mark.parametrize(
    "formula",
    [
        [(1, 2, 3), (-1, -2, 4), (-3, -4, -5)],
        [(-1, -3, 1), (2, 7, 29), (10, 99, -134)],
    ],
)
def test_initializing_sat_formula(formula):
    SatFormula(formula)


@pytest.mark.parametrize(
    ("formula", "expected"),
    [
        ([(1, 2, 3), (-1, -2, 4), (-3, -4, 5)], 5),
        ([(-1, -3, 1), (2, 7, 29), (10, 99, -134)], 134),
    ],
)
def test_max_variable(formula, expected):
    assert SatFormula(formula).max_variable() == expected
