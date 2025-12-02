import pytest

from utils.hash_sat_formula import hash_sat_formula


@pytest.mark.parametrize(
    ("sat_formula"),
    [
        ((1, -2), (-1, 3)),
        [(1, -2), (-3, 4), (-1, 3)],
        {(1, -2), (-3, 4), (-1, 3)},
    ],
)
def test_hash(sat_formula):
    assert hash_sat_formula(sat_formula) == hash(frozenset(sat_formula))
