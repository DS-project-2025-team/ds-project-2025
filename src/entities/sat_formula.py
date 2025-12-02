from collections import UserList
from collections.abc import Iterable, Sequence
from typing import Self


class Clause(tuple):
    CLAUSE_LENGTH = 3

    def __new__(cls, literals: Sequence[int]) -> Self:
        if len(literals) != cls.CLAUSE_LENGTH:
            raise ValueError("Only 3-literal clauses are supported")

        return super().__new__(cls, tuple(literals))


class SatFormula(UserList):
    def __init__(self, clauses: Iterable[Sequence[int]]) -> None:
        super().__init__(Clause(clause) for clause in clauses)
