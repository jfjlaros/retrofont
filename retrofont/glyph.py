from enum import Enum
from typing import Iterator


class Pixel(Enum):
    """Pixel values."""
    empty = 0    #: :meta hide-value:
    filled = 1   #: :meta hide-value:
    visited = 2


def traverse_glyph(glyph: bytes) -> Iterator[tuple[tuple, object]]:
    """Traverse all pixels of a glyph.

    :arg glyph: Glyph.

    :return: Iterator for position and pixel value pairs.
    """
    for r, byte in enumerate(glyph):
        for c in range(8):
            yield (r, c), Pixel(byte >> (7 - c) & 1)


def decode_glyph(glyph: bytes) -> list[str]:
    """Convert a glyph to its text representation.

    :arg glyph: Glyph.

    :return: Text representation of `glyph`.
    """
    text_glyph = [''] * 8
    for (r, c), bit in traverse_glyph(glyph):
        text_glyph[r] += '#' if bit == Pixel.filled else ' '
    return text_glyph


def encode_glyph(text_glyph: list[str]) -> bytes:
    """Convert a glyph from its text representation.

    :arg text_glyph: Text representation of a glyph.

    :return: Glyph.
    """
    glyph = [0] * 8
    for r, line in enumerate(text_glyph):
        for c, pixel in enumerate(line):
            glyph[r] |= 1 << (7 - c) if pixel == '#' else 0
    return bytes(glyph)
