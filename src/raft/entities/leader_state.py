from collections import deque
from collections.abc import Iterable
from dataclasses import dataclass
from uuid import UUID

from entities.sat_formula import SatFormula
from entities.server_address import ServerAddress


@dataclass
class LeaderState:
    def __init__(
        self,
        nodes: list[tuple[UUID, ServerAddress, int]] | None = None,
        completed_tasks: Iterable[bool] | None = None,
        formulas: Iterable[SatFormula] | None = None,
    ) -> None:
        self.nodes: list[tuple[UUID, ServerAddress, int]] = []
        self.completed_tasks: list[bool] = list(completed_tasks or [])
        self.formulas: deque[SatFormula] = deque(formulas or [])

    def __repr__(self) -> str:
        return (
            f"LeaderState(nodes={self.nodes},"
            f"completed_tasks={self.completed_tasks}, formulas={list(self.formulas)})"
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "completed_tasks": self.completed_tasks,
            "formulas": [formula.to_list() for formula in self.formulas],
        }

    @staticmethod
    def from_dict(data: dict[str, object]) -> "LeaderState":
        formulas_data: list[list[list[int]]] = data["formulas"]  # type: ignore
        completed_tasks: list[bool] = data["completed_tasks"]  # type: ignore

        formulas = [SatFormula(formula) for formula in formulas_data]

        return LeaderState([], completed_tasks, formulas)

    def get_nodes(self) -> list:
        return self.nodes

    """
    Copy tuples from nodelist to LeaderState.nodes with
    initial value -1 for last_acked_index
    """
    def set_nodes(self, nodelist: list) -> None:
        self.nodes = [(uuid, server, -1) for uuid, server in nodelist]
