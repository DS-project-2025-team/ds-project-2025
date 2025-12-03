from collections.abc import Callable
from types import CoroutineType


def async_loop(
    function: Callable[..., CoroutineType],
) -> Callable[..., CoroutineType]:
    """
    Wraps an async function into a loop.
    """

    async def decorated(*args: tuple, **kwargs: dict) -> None:
        while True:
            await function(*args, **kwargs)

    return decorated
