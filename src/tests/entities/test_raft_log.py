from collections import deque

from entities.leader_state import LeaderState
from entities.raft_log import RaftLog
from entities.sat_formula import SatFormula


def test_get_completed_tasks():
    leader_state = LeaderState(completed_tasks=[1, 2, 6, 10])

    log = RaftLog(leader_state=leader_state)
    log.leader_state.completed_tasks = [1, 2, 3]

    assert log.completed_tasks == [1, 2, 3]


def test_get_current_formula():
    formula1 = SatFormula([(1, 2, 3), (-1, -2, 3)])
    formula2 = SatFormula([(4, -5, 7), (-4, 5, 6)])
    formula3 = SatFormula([(4, -5, 7), (-4, 5, 6), (1, -3, 2)])

    formulas: deque[SatFormula] = deque(
        [
            formula1,
            formula2,
            formula3,
        ]
    )

    leader_state = LeaderState(formulas=formulas)
    log = RaftLog(leader_state=leader_state)

    assert log.current_formula == formula1
