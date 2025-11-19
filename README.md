# ds-project-2025

[![CI](https://github.com/DS-project-2025-team/ds-project-2025/actions/workflows/ci.yml/badge.svg)](https://github.com/DS-project-2025-team/ds-project-2025/actions/workflows/ci.yml)
[![codecov](https://codecov.io/github/DS-project-2025-team/ds-project-2025/graph/badge.svg?token=TRAX0PX9BL)](https://codecov.io/github/DS-project-2025-team/ds-project-2025)

## Installation

1. Install [uv](https://docs.astral.sh/uv/)

    ```sh
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

2. Clone repository

   ```sh
   git clone git@github.com:DS-project-2025-team/ds-project-2025.git
   ```

## Documentation

- [Architecture](/docs/architecture.md)

## Invoke tasks

Start program

```sh
uv run invoke start
```

See `tasks.py` for other tasks:

```sh
uv run invoke task-name-kebab-case
```

## Commit message

[Conventional commits](https://www.conventionalcommits.org/en/v1.0.0/)
