from multiprocessing.pool import Pool

from entities.sat_formula import SatFormula
from utils.check_sat import check_sat_formula
from utils.task import get_subinterval


def __compute(formula: SatFormula, task: int, exponent: int) -> bool:
    begin, end = get_subinterval(2**exponent, task)
    return check_sat_formula(formula, begin, end)


def main() -> None:
    with Pool(8) as pool:
        formula = SatFormula([(1, 2, 3), (-1, -2, 4), (-3, -4, -5)])
        task = 6
        exponent = 0

        pool.apply_async(
            __compute,
            (formula, task, exponent),
            callback=lambda result: print(result),
        )


if __name__ == "__main__":
    main()
