from entities.sat_formula import SatFormula


class LeaderState:
    nodes: dict[str, dict] = {}
    completed_tasks: list[int] = []
    formula: SatFormula | None = None
