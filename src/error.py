from dataclasses import dataclass


class LeaderExistsError(Exception):
    def __str__(self) -> str:
        return "Detected existing leader"


@dataclass
class OutDatedTermError(Exception):
    current_term: int
    new_term: int

    def __str__(self) -> str:
        return f"Outdated term: {self.current_term} < {self.new_term}"
