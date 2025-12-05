from entities.sat_formula import SatFormula
from entities.server_address import ServerAddress
from network.client import Client
from services.logger_service import logger


async def run_client(formula: SatFormula, server: ServerAddress) -> None:
    async with Client(server) as client:
        result = await client.input(formula)
        logger.info(f"SAT formula {formula} is satisfiable: {result}")
