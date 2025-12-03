from collections.abc import Awaitable, Callable


def async_loop(
    function: Callable[..., Awaitable],
) -> Callable[..., Awaitable]:
    """
    Runs given function in loop.

    Args:
        function (Callable[..., Awaitable]): Async function to run

    Returns:
        Callable[..., Awaitable]: Wrapped function
    """

    async def decorated(*args: tuple, **kwargs: dict) -> None:
        while True:
            await function(*args, **kwargs)

    return decorated
