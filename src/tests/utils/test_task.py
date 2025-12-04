import pytest

from entities.sat_formula import SatFormula
from utils.task import get_interval, get_subinterval


@pytest.mark.parametrize(
    ("formula", "expected"),
    [
        (SatFormula([(1, 2, 3), (3, 4, 5), (2, -5, -6)]), (0, 2**6)),
        (SatFormula([(1, 2, 3), (3, 4, 5), (2, 53, 6)]), (0, 2**53)),
    ],
)
def test_get_interval(formula, expected):
    assert get_interval(formula) == expected


@pytest.mark.parametrize(
    ("interval_size", "i", "expected"),
    [
        (4, 0, (0, 4)),
        (2**6, 8, (8 * 2**6, 8 * 2**6 + 2**6)),
        (0, 0, (0, 0)),
        (1, 38, (38, 39)),
    ],
)
def test_get_subinterval(interval_size, i, expected):
    assert get_subinterval(interval_size, i) == expected
