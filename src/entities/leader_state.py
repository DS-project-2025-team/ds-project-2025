from entities.sat_formula import SatFormula


class LeaderState:
    def __init__(
        self,
        nodes: dict[str, dict] | None = None,
        completed_tasks: list[int] | None = None,
        sat_formula: SatFormula | None = None,
    ) -> None:
        self.nodes: dict[str, dict] = nodes or {}
        self.completed_tasks: list[int] = completed_tasks or []
        self.formula: SatFormula | None = sat_formula
