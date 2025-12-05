# ds-project-2025

[![CI](https://github.com/DS-project-2025-team/ds-project-2025/actions/workflows/ci.yml/badge.svg)](https://github.com/DS-project-2025-team/ds-project-2025/actions/workflows/ci.yml)
[![codecov](https://codecov.io/github/DS-project-2025-team/ds-project-2025/graph/badge.svg?token=TRAX0PX9BL)](https://codecov.io/github/DS-project-2025-team/ds-project-2025)

## Installation

1. Install [uv](https://docs.astral.sh/uv/)

    ```sh
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

1. Clone repository

   ```sh
   git clone git@github.com:DS-project-2025-team/ds-project-2025.git
   ```

1. Install and initialize Kafka

    ```sh
    uv run invoke install-kafka
    ```

## Running the program

1. Start Kafka server

   ```sh
    uv run invoke start-kafka
   ```

1. Start node.
   Repeat at least twice, for example in different terminal tabs.

    ```sh
    uv run invoke start
    ```

    Parameters:
    - `--role`: optional, defaults to `follower`
    - `--server`: optional, defaults to `localhost`
    - `--port`: optional, defaults to `9092`
    - `--log-level`: optional, defaults to `INFO`

1. Start client to send inputs to the system

    ```sh
    uv run invoke start-client
    ```

    Parameters:
    - `--server`: optional, defaults to `localhost`
    - `--port`: optional, defaults to `9092`

    Edit `start_client()` in [`tasks.py`](/tasks.py) to change input.

> [TIP]
> Use `--help` to get more information about invoke task parameters.
>
> ```sh
> uv run invoke start --help
> ```

## Documentation

- [Architecture](/docs/architecture.md)

## Tasks

See [`tasks.py`](/tasks.py) for other tasks:

```sh
uv run invoke task-name-kebab-case
```

## Commit message

[Conventional commits](https://www.conventionalcommits.org/en/v1.0.0/)
