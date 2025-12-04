import asyncio
from argparse import ArgumentParser

from entities.sat_formula import SatFormula
from entities.server_address import ServerAddress
from network.client import Client
from services.logger_service import logger


def init_parser() -> ArgumentParser:
    parser = ArgumentParser()

    parser.add_argument(
        "--server",
        "-s",
        type=str,
        help="Kafka server",
        default="localhost",
    )

    parser.add_argument(
        "--port",
        "-p",
        type=int,
        help="Kafka server port",
        default=9092,
    )

    return parser


async def main(formula: SatFormula) -> None:
    parser = init_parser()
    args = parser.parse_args()

    server = ServerAddress(host=args.server, port=args.port)

    async with Client(server) as client:
        result = await client.input(formula)
        logger.info(f"SAT formula {formula} is satisfiable: {result}")


if __name__ == "__main__":
    formula = SatFormula([(1, 2, 3), (-1, -2, 4), (-3, -4, -5)])

    asyncio.run(main(formula))
