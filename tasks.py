from pathlib import Path
import sys
from uuid import uuid4
from invoke.context import Context
from invoke.tasks import task

sys.path.append(str(Path(__file__).parent / "src"))

from config import KAFKA_CLUSTER_ID, KAFKA_PATH, ROOT_DIR, SOURCE_DIR


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


@task
def start(
    ctx: Context,
    role: str | None = None,
    server: str | None = None,
    port: int | None = None,
    log_level: int | None = None,
) -> None:
    command = " ".join(
        [
            f"uv run python {SOURCE_DIR}/main.py",
            f"--role {role}" if role else "",
            f"--server {server}" if server else "",
            f"--port {port}" if port else "",
            f"--log-level {log_level}" if log_level else "",
        ]
    )

    ctx.run(command)


@task
def start_client(
    ctx: Context,
    server: str | None = None,
    port: int | None = None,
) -> None:
    command = " ".join(
        [
            f"uv run python {SOURCE_DIR}/client.py",
            f"--server {server}" if server else "",
            f"--port {port}" if port else "",
        ]
    )

    ctx.run(command)


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
