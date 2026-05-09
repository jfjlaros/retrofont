from typing import Callable

from .font import Font


def doc_split(func: Callable) -> str:
    return func.__doc__.split('\n\n')[0]
