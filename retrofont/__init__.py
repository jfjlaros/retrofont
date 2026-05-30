from importlib.metadata import PackageNotFoundError, metadata
from re import split
from typing import Callable


def _extract(key, delim=r'[^\s\S]', index=0):
    try:
        value = metadata('retrofont').get(key, '')
    except PackageNotFoundError:
        return ''
    return split(delim, value)[index]


def doc_split(func: Callable) -> str:
    return func.__doc__.split('\n\n')[0]


_project = _extract('Name')
_version = _extract('Version')
_author = _extract('Author-email', r'"', 1)
_email = _extract('Author-email', r'<|>', 1)
_description = _extract('Summary')
_copyright = f'Copyright (c) 2026 by {_author} <{_email}>'
_url = _extract('Project-URL', ', ', 1)
_info = f'{_project} version {_version}\n\n{_copyright}\nHomepage: {_url}'
