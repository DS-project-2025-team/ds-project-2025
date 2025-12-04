import pytest

from entities.sat_formula import SatFormula
from utils.task import get_interval


@pytest.mark.parametrize(
    ("formula", "expected"),
    [
        (SatFormula([(1, 2, 3), (3, 4, 5), (2, -5, -6)]), (0, 2**6)),
        (SatFormula([(1, 2, 3), (3, 4, 5), (2, 53, 6)]), (0, 2**53)),
    ],
)
def test_get_interval(formula, expected):
    assert get_interval(formula) == expected
