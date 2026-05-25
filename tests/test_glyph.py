from retrofont.glyph import Pixel, traverse_glyph, decode_glyph, encode_glyph

from shared import test_glyph, test_text_glyph


def test_traverse_glyph():
    iterator = traverse_glyph(test_glyph)
    for c in range(7):
        assert next(iterator) == ((0, c), Pixel.empty)
    assert next(iterator) == ((0, 7), Pixel.filled)
    assert next(iterator) == ((1, 0), Pixel.empty)


def test_decode_glyph():
    assert decode_glyph(test_glyph) == test_text_glyph


def test_encode():
    assert encode_glyph(test_text_glyph) == test_glyph
