import pytest

from entities.sat_formula import SatFormula
from entities.task_queue import TaskQueue


def test_completed_tasks_initialized_correctly():
    formula = SatFormula([(1, -2, 6), (-1, 3, 4)])

    scheduler = TaskQueue(formula, exponent=2)

    assert scheduler._TaskQueue__completed_tasks == [False] * (2**4)


def test_tasks_initialized_correctly():
    formula = SatFormula([(1, -2, 6), (-1, 3, 4)])

    scheduler = TaskQueue(formula, exponent=2)

    expected = list(range(0, 16))

    assert len(scheduler._TaskQueue__tasks) == len(expected)
    assert list(scheduler._TaskQueue__tasks) == expected


def test_next_task_does_not_remove_before_complete():
    formula = SatFormula([(1, -2, 6), (-1, 3, 4), (-1, 3, -6)])

    scheduler = TaskQueue(formula, exponent=2)
    total_tasks = len(scheduler._TaskQueue__tasks)

    scheduler.next_task()
    scheduler.next_task()
    scheduler.next_task()

    assert len(scheduler._TaskQueue__tasks) == total_tasks


@pytest.mark.parametrize(
    ("task", "result"),
    [
        (0, True),
        (0, False),
        (1, True),
        (1, False),
        (3, True),
        (6, False),
    ],
)
def test_complete_task_is_idempotent(task, result):
    formula = SatFormula([(1, -2, 6), (-1, 3, 4)])
    n = 7
    tasks = range(n)

    scheduler = TaskQueue(formula, exponent=2, tasks=tasks)

    for _ in range(2 * n):
        scheduler.complete_task(task)

        assert scheduler._TaskQueue__tasks_remaining == n - 1
        assert scheduler._TaskQueue__completed_tasks[task]


def test_complete_task_gives_false_when_all_tasks_false():
    formula = SatFormula([(1, -2, 6), (-1, 3, 4)])
    n = 3
    tasks = range(n)

    scheduler = TaskQueue(formula, exponent=2, tasks=tasks)

    assert not scheduler.complete_task(0)
    assert not scheduler.complete_task(1)
    assert not scheduler.complete_task(2)
