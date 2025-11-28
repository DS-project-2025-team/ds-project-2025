from dataclasses import dataclass

from entities.sat_formula import SatFormula


@dataclass
class LeaderState:
    nodes: dict[str, dict] = {}
    tasks: dict[str, str] = {}
    uncompleted_tasks: set[str] = set()
    formula: SatFormula | None = None
