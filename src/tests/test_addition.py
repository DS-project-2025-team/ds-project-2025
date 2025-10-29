import pytest


@pytest.mark.parametrize(("a", "b", "expected"), [(1, 2, 3), (2, 3, 5), (3, 4, 7)])
def test_addition(a, b, expected):
    assert a + b == expected
