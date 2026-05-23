from .glyph import Pixel, decode, encode, traverse


def add(p1: tuple[int], p2: tuple[int]) -> tuple[int]:
    """
    """
    r1, c1 = p1
    r2, c2 = p2
    return (r1 + r2, c1 + c2)


def rotate_cw(p: tuple[int]) -> tuple[int]:
    """
    """
    r, c = p
    return (c, -r)


def rotate_ccw(p: tuple[int]) -> tuple[int]:
    """
    """
    r, c = p
    return (-c, r)


class Tracer:
    """
    """
    def __init__(self):
        self._glyph = [[Pixel.empty] * 18 for _ in range(18)]
        self._paths = []

    def _get(self, p):
        r, c = p
        return self._glyph[r][c]

    def _load_pixel(self, p, pixel):
        r, c = p
        for dr, dc in [(0, 0), (1, 0), (0, 1), (1, 1)]:
            self._glyph[2 * r + dr + 1][2 * c + dc + 1] = pixel

    def _is_start(self, p):
        return (
            self._get(p) == Pixel.filled and
            self._get(add(p, (-1, 0))) == Pixel.empty)

    def _find_start(self):
        for r in range(1, 17):
            for c in range(1, 17):
                if self._is_start((r, c)):
                    yield (r, c)

    def _visit(self, p, d):
        r, c = p
        self._glyph[r][c] = Pixel.visited

    def _step(self, p, d):
        self._visit(p, d)
        return add(p, d)

    def _path_append(self, p):
        r, c = p
        self._paths[-1].append((r // 2, c // 2))

    def _navigate(self, p, d):
        if self._get(add(p, d)) == Pixel.empty:
            self._path_append(p)
            return (p, rotate_cw(d))
        _d = rotate_ccw(d)
        if self._get(add(p, _d)) != Pixel.empty:
            self._path_append(p)
            return (self._step(p, _d), _d)
        return (self._step(p, d), d)

    def _prepend_inner(self, p):
        _p = add(p, (0, -1))
        if self._get(_p) == Pixel.filled:
            self._visit(add(p, (0, -1)), (0, 1))

    def _trace(self, p, d):
        _p, _d = p, d
        self._prepend_inner(p)
        while self._get(_p) == Pixel.filled:
            _p, _d = self._navigate(_p, _d)

    def load(self, binary_glyph: bytes) -> None:
        """
        """
        for p, pixel in traverse(binary_glyph):
            self._load_pixel(p, pixel)
        self._paths = []

    def trace(self) -> None:
        """
        """
        for p in self._find_start():
            self._paths.append([])
            self._path_append(p)
            self._trace(p, (0, 1))

    def paths(self) -> None:
        """
        """
        return self._paths
