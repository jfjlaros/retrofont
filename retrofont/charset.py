from typing import BinaryIO, TextIO

from .math import make_matrix, pad, reverse


def read_rom(handle: BinaryIO, mirror: bool=False) -> list[...]:
    """Read the content of a character ROM.

    :arg handle: Handle to character ROM file.
    :arg mirror: Reverse bit order.

    :return: Character sets.
    """
    data = handle.read()

    if mirror:
        data = bytes(map(reverse, data))
    data += b'\x00' * pad(len(data), 256)

    return make_matrix(data, (256, 8))


def read_map(handle: BinaryIO, offset: int) -> list[int]:
    """Read a map from a firmware ROM.

    :arg handle: Handle to firmware ROM file.
    :arg offset: Location of the map in the firmware.

    :return: Map.
    """
    handle.seek(offset)
    return list(handle.read(256))


def map_charset(charset: list[bytes], permutation: list[int]) -> list[bytes]:
    """Permuta a character set.

    :arg charset: Character set.
    :arg permutation: Permutation.

    :return: Permuted character set.
    """
    return [charset[index] for index in permutation]


def map_charsets(charsets: list[...], permutation: list[int]) -> list[...]:
    """Permuta a list of character sets.

    :arg charsets: List of character sets.
    :arg permutation: Permutation.

    :return: List of permuted character sets.
    """
    return [map_charset(charset, permutation) for charset in charsets]


def print_glyph(handle: TextIO, glyph: list[bytes]) -> None:
    """Print a glyph.

    :arg handle: Handle to a stream.
    :arg glyph: Glyph data.
    """
    for line in glyph:
        for i in range(7, -1, -1):
            handle.write('#' if (line >> i) & 1 else ' ')
        handle.write('\n')
