import pytest

from sat import check_literal


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
