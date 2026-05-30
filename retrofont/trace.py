from typing import Iterator

from .glyph import Pixel, traverse_glyph
from .math import (
    add_tuples, flatten_matrix, rotate_tuple_cw, rotate_tuple_ccw)


def get_lsb(paths: list[list[tuple[int, int]]]) -> int:
    """Find the left-side border of a glyph.

    :arg paths: Glyph outlines.

    :return: Left-side border of the glyph.
    """
    if not paths:
        return 0
    return min(point[1] for point in flatten_matrix(paths))


class Tracer:
    """Glyph tracer."""
    def __init__(self):
        self._glyph = [[Pixel.empty] * 18 for _ in range(18)]
        self._paths = []

    def _get(self, p: tuple[int]) -> object:
        r, c = p
        return self._glyph[r][c]

    def _load_pixel(self, p: tuple[int], pixel) -> None:
        r, c = p
        for dr, dc in [(0, 0), (1, 0), (0, 1), (1, 1)]:
            self._glyph[2 * r + dr + 1][2 * c + dc + 1] = pixel

    def _is_start(self, p: tuple[int]) -> bool:
        return (
            self._get(p) == Pixel.filled and
            self._get(add_tuples(p, (-1, 0))) == Pixel.empty)

    def _find_start(self) -> Iterator[tuple[int]]:
        for r in range(1, 17):
            for c in range(1, 17):
                if self._is_start((r, c)):
                    yield (r, c)

    def _visit(self, p: tuple[int], d: tuple[int]) -> None:
        r, c = p
        self._glyph[r][c] = Pixel.visited

    def _step(self, p: tuple[int], d: tuple[int]) -> tuple[int]:
        self._visit(p, d)
        return add_tuples(p, d)

    def _path_append(self, p: tuple[int]) -> None:
        r, c = p
        self._paths[-1].append((r // 2, c // 2))

    def _navigate(self, p: tuple[int], d: tuple[int]) -> tuple[tuple[int]]:
        if self._get(add_tuples(p, d)) == Pixel.empty:
            self._path_append(p)
            return (p, rotate_tuple_cw(d))
        _d = rotate_tuple_ccw(d)
        if self._get(add_tuples(p, _d)) != Pixel.empty:
            self._path_append(p)
            return (self._step(p, _d), _d)
        return (self._step(p, d), d)

    def _prepend_inner(self, p: tuple[int]) -> None:
        _p = add_tuples(p, (0, -1))
        if self._get(_p) == Pixel.filled:
            self._visit(add_tuples(p, (0, -1)), (0, 1))

    def _trace(self, p: tuple[int], d: tuple[int]) -> None:
        _p, _d = p, d
        self._prepend_inner(p)
        while self._get(_p) == Pixel.filled:
            _p, _d = self._navigate(_p, _d)

    def load(self, glyph: bytes) -> None:
        """Load a glyph.

        :arg glyph: A glyph.
        """
        for p, pixel in traverse_glyph(glyph):
            self._load_pixel(p, pixel)
        self._paths = []

    def trace(self) -> None:
        """Trace the loaded glyph."""
        for p in self._find_start():
            self._paths.append([])
            self._path_append(p)
            self._trace(p, (0, 1))

    def get_paths(self) -> list[list[tuple[int, int]]]:
        """Get the result of the traced glyph.

        :returns: Traced glyph paths.
        """
        return self._paths
