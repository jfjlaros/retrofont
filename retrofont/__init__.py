from typing import Callable

from .ttf import TTF


def doc_split(func: Callable) -> str:
    return func.__doc__.split('\n\n')[0]
