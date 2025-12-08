from collections.abc import Callable, Coroutine
from typing import Any, ParamSpec

P = ParamSpec("P")


def async_loop[**P](
    function: Callable[P, Coroutine],
) -> Callable[P, Coroutine[Any, Any, None]]:
    """
    Wraps an async function into an infinite loop.
    """

    async def decorated(*args: P.args, **kwargs: P.kwargs) -> None:
        while True:
            await function(*args, **kwargs)

    return decorated
