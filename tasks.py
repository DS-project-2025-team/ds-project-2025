import asyncio
from pathlib import Path
import sys

from invoke.context import Context
from invoke.tasks import task

sys.path.append(str(Path(__file__).parent / "src"))

from config import KAFKA_CLUSTER_ID, KAFKA_PATH, ROOT_DIR, SOURCE_DIR
from client import run_client
from entities.sat_formula import SatFormula
from entities.server_address import ServerAddress
from main import main
from raft.roles.role import Role
from services.logger_service import logger


@task
def format(ctx: Context) -> None:
    with ctx.cd(ROOT_DIR):
        ctx.run("ruff format")


@task
def lint(ctx: Context) -> None:
    with ctx.cd(ROOT_DIR):
        ctx.run("ruff check")


@task
def lint_fix(ctx: Context) -> None:
    with ctx.cd(ROOT_DIR):
        ctx.run("ruff check --fix")


@task
def test(ctx: Context) -> None:
    with ctx.cd(ROOT_DIR):
        ctx.run("python -m pytest --color=yes -n auto", pty=True)


@task
def coverage(ctx: Context) -> None:
    with ctx.cd(ROOT_DIR):
        ctx.run("pytest --cov --cov-branch --cov-report xml -n auto", pty=True)


@task
def coverage_html(ctx: Context) -> None:
    with ctx.cd(ROOT_DIR):
        ctx.run("pytest --cov --cov-branch --cov-report html -n auto", pty=True)


@task(
    help={
        "role": "Node role [follower | candidate | leader]. Defaults to follower",
        "server": 'Kafka server. Defaults to "localhost"',
        "port": "Kafka server port. Defaults to 9092",
        "log_level": "Logging level [DEBUG | INFO | WARNING | ERROR | CRITICAL]. Defaults to INFO",
    }
)
def start(
    _: Context,
    role: Role = Role.FOLLOWER,
    server: str = "localhost",
    port: int = 9092,
    log_level: str = "INFO",
) -> None:
    """
    Starts a node.
    """
    server_address = ServerAddress(server, port)

    asyncio.run(main(role=role, server=server_address, log_level=log_level))


@task(
    help={
        "server": 'Kafka server. Defaults to "localhost"',
        "port": "Kafka server port. Defaults to 9092",
    }
)
def start_client(
    _,
    server: str = "localhost",
    port: int = 9092,
) -> None:
    """
    Starts client and sends input to the system.
    """

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

    server_address = ServerAddress(server, port)

    asyncio.run(run_client(formula, server_address))


@task
def install_kafka(ctx: Context) -> None:
    ctx.run(f"uv run python {SOURCE_DIR}/install_kafka.py")

    ctx.run(
        f"{KAFKA_PATH}/bin/kafka-storage.sh format --standalone -t {KAFKA_CLUSTER_ID} -c kafka-config/server.properties"
    )


@task
def start_kafka(ctx: Context) -> None:
    with ctx.cd(ROOT_DIR):
        ctx.run(
            f"{KAFKA_PATH}/bin/kafka-server-start.sh kafka-config/server.properties"
        )


@task
def stop_kafka(ctx: Context) -> None:
    ctx.run(f"{KAFKA_PATH}/bin/kafka-server-stop.sh")
