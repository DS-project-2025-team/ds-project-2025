import asyncio
from time import perf_counter

from entities.sat_formula import SatFormula
from services.worker_service import WorkerService


async def benchmark_sat(formula: SatFormula) -> None:
    worker = WorkerService()

    begin = perf_counter()
    with worker:
        await worker.run_task(formula, 0, formula.max_variable())

    end = perf_counter()
    print(f"Benchmark completed in {end - begin:.2f} seconds.")


async def main() -> None:
    formula = SatFormula(
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

    await benchmark_sat(formula)


if __name__ == "__main__":
    asyncio.run(main())
