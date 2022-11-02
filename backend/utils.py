import functools
import time
from typing import Any, Callable


def time_exec(f) -> Callable[..., tuple[Any, float]]:
    functools.wraps(f)

    def wrapper():
        start = time.time_ns()
        res = f()
        end = time.time_ns()
        return end - start, res

    return wrapper
