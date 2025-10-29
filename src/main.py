def hello(name: str) -> str:
    return f"Hello {name}!"


def hello_world() -> None:
    print(hello("world"))


if __name__ == "__main__":
    hello_world()
