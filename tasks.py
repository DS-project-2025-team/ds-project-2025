from pathlib import Path
from uuid import uuid4

from invoke.context import Context
from invoke.tasks import task

ROOT_DIR = Path(__file__).parent
SOURCE_DIR = ROOT_DIR / "src"
KAFKA_DIR = ROOT_DIR / "bin" / "kafka"
KAFKA_CLUSTER_ID = "e54a5213-2e0f-49d6-8339-978aae554a11"


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
def start(ctx: Context) -> None:
    ctx.run(f"uv run python {SOURCE_DIR}/main.py")


@task
def install_kafka(ctx: Context) -> None:
    ctx.run(f"uv run python {SOURCE_DIR}/install_kafka.py")

    ctx.run(
        f"{KAFKA_DIR}/bin/kafka-storage.sh format --standalone -t {KAFKA_CLUSTER_ID} -c kafka-config/server.properties"
    )


@task
def start_kafka(ctx: Context) -> None:
    ctx.run(f"{KAFKA_DIR}/bin/kafka-server-start.sh kafka-config/server.properties")


@task
def stop_kafka(ctx: Context) -> None:
    ctx.run(f"{KAFKA_DIR}/bin/kafka-server-stop.sh")
