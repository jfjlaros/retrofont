from retrofont.trace import Tracer, get_lsb

from shared import test_glyph


def test_get_lsb():
    assert get_lsb([[(0, 5), (0, 6)], [(0, 3), (0, 4)]]) == 3


def test_load():
    tracer = Tracer()
    tracer.load(test_glyph)
    assert tracer.get_paths() == []


def test_trace():
    tracer = Tracer()
    tracer.load(test_glyph)
    tracer.trace()
    assert tracer.get_paths() == [
        [(0, 7), (0, 8), (1, 8), (1, 7)],
        [(1, 2), (1, 4), (2, 4), (2, 5), (3, 5), (3, 6),
         (4, 6), (4, 4), (3, 4), (3, 3), (2, 3), (2, 2)],
        [(1, 6), (1, 7), (2, 7), (2, 6)],
        [(5, 0), (5, 3), (8, 3), (8, 0)],
        [(5, 5), (5, 8), (8, 8), (8, 5)],
        [(7, 1), (7, 2), (6, 2), (6, 1)]]

