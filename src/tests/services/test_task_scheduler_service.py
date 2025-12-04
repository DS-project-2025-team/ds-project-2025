import pytest
from entities.sat_formula import SatFormula
from services.task_scheduler_service import TaskSchedulerService


def test_completed_tasks_initialized_correctly():
    formula = SatFormula([(1, -2, 6), (-1, 3, 4)])

    scheduler = TaskSchedulerService(formula, exponent=2)

    assert scheduler._TaskSchedulerService__completed_tasks == [False] * (2**4)


def test_tasks_initialized_correctly():
    formula = SatFormula([(1, -2, 6), (-1, 3, 4)])

    scheduler = TaskSchedulerService(formula, exponent=2)

    expected = list(range(0, 16))

    assert len(scheduler._TaskSchedulerService__tasks) == len(expected)
    assert list(scheduler._TaskSchedulerService__tasks) == expected


def test_next_task_does_not_remove_before_complete():
    formula = SatFormula([(1, -2, 6), (-1, 3, 4), (-1, 3, -6)])

    scheduler = TaskSchedulerService(formula, exponent=2)
    total_tasks = len(scheduler._TaskSchedulerService__tasks)

    scheduler.next_task()
    scheduler.next_task()
    scheduler.next_task()

    assert len(scheduler._TaskSchedulerService__tasks) == total_tasks


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

    scheduler = TaskSchedulerService(formula, exponent=2, tasks=tasks)

    initial = scheduler.complete_task(task, result)

    for _ in range(2 * n):
        assert scheduler.complete_task(task, result) == initial


def test_complete_task_gives_false_when_all_tasks_false():
    formula = SatFormula([(1, -2, 6), (-1, 3, 4)])
    n = 3
    tasks = range(n)

    scheduler = TaskSchedulerService(formula, exponent=2, tasks=tasks)

    assert not scheduler.complete_task(1, False)
    assert not scheduler.complete_task(2, False)
    assert not scheduler.complete_task(3, False)


def test_complete_task_gives_true_when_any_task_true():
    formula = SatFormula([(1, -2, 6), (-1, 3, 4)])
    n = 3
    tasks = range(n)

    scheduler = TaskSchedulerService(formula, exponent=2, tasks=tasks)

    assert not scheduler.complete_task(1, False)
    assert scheduler.complete_task(2, True)
