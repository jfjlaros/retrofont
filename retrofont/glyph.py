from enum import Enum


class Pixel(Enum):
    empty = 0
    filled = 1
    visited = 2


def traverse(glyph: bytes) -> tuple[tuple, object]:
    """
    """
    for r, byte in enumerate(glyph):
        for c in range(8):
            yield (r, c), Pixel(byte >> (7 - c) & 1)


def decode(glyph: bytes) -> list[str]:
    """
    """
    text_glyph = [''] * 8
    for (r, c), bit in traverse(glyph):
        text_glyph[r] += '#' if bit == Pixel.filled else ' '
    return text_glyph


def encode(text_glyph: list[str]) -> bytes:
    """
    """
    glyph = [0] * 8
    for r, line in enumerate(text_glyph):
        for c, pixel in enumerate(line):
            glyph[r] |= 1 << (7 - c) if pixel == '#' else 0
    return bytes(glyph)
