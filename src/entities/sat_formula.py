from collections import UserList
from collections.abc import Iterable, Sequence
from itertools import chain
from typing import Self


class Clause(tuple):
    CLAUSE_LENGTH = 3

    def __new__(cls, literals: Sequence[int]) -> Self:
        if len(literals) != cls.CLAUSE_LENGTH:
            raise ValueError("Only 3-literal clauses are supported")

        if 0 in literals:
            raise ValueError("Literal cannot be zero")

        return super().__new__(cls, tuple(literals))


class SatFormula(UserList):
    def __init__(self, clauses: Iterable[Sequence[int]]) -> None:
        super().__init__(map(Clause, clauses))

    def __repr__(self) -> str:
        return f"SatFormula({list(self.data)})"

    def __str__(self) -> str:
        return self.__repr__()

    def to_list(self) -> list[list[int]]:
        return [list(clause) for clause in self.data]

    def max_variable(self) -> int:
        """
        Return the maximum variable index.
        For example, the maximum index of [(1, -2, 3), (-1, 4, -5)] is 5.

        Returns:
            int: The maximum index of variables.
        """
        if not self.data:
            raise ValueError("Cannot compute max_variable for empty formula")

        return max(map(abs, chain.from_iterable(self.data)))
