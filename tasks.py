from pathlib import Path

from invoke.context import Context
from invoke.tasks import task

ROOT_DIR = Path(__file__).parent
SOURCE_DIR = ROOT_DIR / "src"


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
def coverage_html(ctx: Context) -> None:
    with ctx.cd(ROOT_DIR):
        ctx.run("pytest --cov --cov-report html -n auto", pty=True)


@task
def start(ctx: Context) -> None:
    with ctx.cd(ROOT_DIR):
        ctx.run(f"uv run python {SOURCE_DIR}/main.py")
