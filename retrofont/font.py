from copy import copy

from .glyph import decode, encode
from .math import flatten_matrix, make_matrix, pad, reverse


def yaml_to_font(yaml_font: list[dict]) -> list[...]:
    """
    """
    font = []
    for yaml_charset in yaml_font:
        charset = [b'\x00' * 8 for _ in range(256)]
        for yaml_glyph in yaml_charset:
            charset[yaml_glyph['offset']] = encode(yaml_glyph['data'])
        font.append(charset)
    return font


def font_to_yaml(font: list[...]) -> list[dict]:
    """
    """
    yaml_font = []
    for charset in font:
        yaml_charset = []
        for i, glyph in enumerate(charset):
            if glyph != b'\x00\x00\x00\x00\x00\x00\x00\x00':
                yaml_charset.append(
                    {'offset': i, 'data': decode(glyph)})
        yaml_font.append(yaml_charset)
    return yaml_font


def rom_to_font(data: bytes, mirror: bool=False) -> list[...]:
    """Read the content of a character ROM.

    :arg data: Character ROM content.
    :arg mirror: Reverse bit order.

    :return: Character sets.
    """
    if mirror:
        data = bytes(map(reverse, data))
    data += b'\x00' * pad(len(data), 2048)

    return make_matrix(data, (256, 8))


def font_to_rom(font: list[...]) -> bytes:
    """
    """
    return b''.join(flatten_matrix(font))


def keymap_to_permutation(keymap: dict) -> list[...]:
    """
    """
    if not keymap:
        return [i for i in range(0x100)]

    permutation = [0x00 for _ in range(0x100)]
    for character_block in keymap.get('character_blocks', []):
        shift = character_block[0] - character_block[1][0]
        for i in range(*character_block[1]):
            permutation[i + shift] = i
    for character in keymap.get('characters', []):
        permutation[character[0]] = character[1]
    return permutation


def map_charset(charset: list[bytes], permutation: list[int]) -> list[bytes]:
    """Permute a character set.

    :arg charset: Character set.
    :arg permutation: Permutation.

    :return: Permuted character set.
    """
    return [charset[index] for index in permutation]


def map_font(font: list[...], permutation: list[int]) -> list[...]:
    """Permute a list of character sets.

    :arg font: List of character sets.
    :arg permutation: Permutation.

    :return: List of permuted character sets.
    """
    return [map_charset(charset, permutation) for charset in font]


def _printable(character):
    if character < 0x20:
        return ' '
    if character > 0x7e and character < 0xa0:
        return ' '
    return chr(character)


def visualise(offset: int) -> list[str]:
    """
    """
    charset = []
    charset.append('  | ' + ' '.join([f'{i:x}' for i in range(0x10)]))
    charset.append(f'--+{"--" * 0x10}')
    for i in range(0x10):
        charset.append(f'{i:x} |')
        for j in range(0x10):
            charset[-1] += f' {_printable(offset + (i << 4 | j))}'
    return charset
