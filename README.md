# ds-project-2025

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

Dependencies for compiling Typst documentation:

1. Install cargo with a package manager or [rustup](https://rustup.rs/)

2. Install Typst and Typstyle formatter

   ```sh
   cargo install --locked typst-cli typstyle
   ```

The documentation can be compiled with

```sh
typst compile path/to/file.typ
```

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
