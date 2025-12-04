from cProfile import Profile
from pstats import Stats

from entities.sat_formula import SatFormula
from utils.check_sat import check_sat_formula
from utils.task import get_interval


def benchmark_sat(formula: SatFormula) -> None:
    with Profile() as profile:
        begin, end = get_interval(formula)

        check_sat_formula(formula, begin, end)

        Stats(profile).sort_stats("tottime").print_stats(10)


if __name__ == "__main__":
    benchmark_sat(
        SatFormula(
            [
                (1, 2, 3),
                (1, 2, -3),
                (1, -2, 3),
                (1, -2, -3),
                (-1, 2, 3),
                (-1, 2, -3),
                (-1, -2, 3),
                (-1, -2, -3),
                (-5, 6, 10),
                (1, 14, -15),
                (-15, 14, -13),
            ]
        )
    )

    benchmark_sat(
        SatFormula(
            [
                (1, 2, 3),
                (1, 2, -3),
                (1, -2, 3),
                (1, -2, -3),
                (-1, 2, 3),
                (-1, 2, -3),
                (-1, -2, 3),
                (-1, -2, -3),
                (-5, 6, 10),
                (1, 17, -17),
                (-17, 16, -16),
            ]
        )
    )

    benchmark_sat(
        SatFormula(
            [
                (1, 2, 3),
                (1, 2, -3),
                (1, -2, 3),
                (1, -2, -3),
                (-1, 2, 3),
                (-1, 2, -3),
                (-1, -2, 3),
                (-1, -2, -3),
                (-5, 6, 10),
                (1, 19, -20),
                (-20, 18, -19),
            ]
        )
    )
