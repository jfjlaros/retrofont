from .glyph import decode_glyph, encode_glyph
from .math import flatten_matrix, make_matrix, pad_block, reverse_byte


def rom_to_font(data: bytes, mirror: bool=False) -> list[list[bytes]]:
    """Deserialise ROM content to a font.

    :arg data: Character ROM content.
    :arg mirror: Reverse bit order.

    :return: Font.
    """
    if mirror:
        data = bytes(map(reverse_byte, data))
    data += b'\x00' * pad_block(len(data), 2048)

    return make_matrix(data, (256, 8))


def font_to_rom(font: list[list[bytes]]) -> bytes:
    """Serialise a front to ROM content.

    :arg font: Font.

    :return: Character ROM content.
    """
    return b''.join(flatten_matrix(font))


def yaml_to_font(yaml_font: list[dict]) -> list[list[bytes]]:
    """Convert a font from its YAML representation.

    :arg yaml_font: YAML representation of a font.

    :return: Font.
    """
    font = []
    for yaml_charset in yaml_font:
        charset = [b'\x00' * 8 for _ in range(256)]
        for yaml_glyph in yaml_charset:
            charset[yaml_glyph['offset']] = encode_glyph(yaml_glyph['data'])
        font.append(charset)
    return font


def font_to_yaml(font: list[list[bytes]]) -> list[dict]:
    """Convert a font to its YAML representation.

    :arg font: Font.

    :return: YAML representation of `font`.
    """
    yaml_font = []
    for charset in font:
        yaml_charset = []
        for i, glyph in enumerate(charset):
            if glyph != b'\x00\x00\x00\x00\x00\x00\x00\x00':
                yaml_charset.append(
                    {'offset': i, 'data': decode_glyph(glyph)})
        yaml_font.append(yaml_charset)
    return yaml_font


def keymap_to_permutation(keymap: dict) -> list:
    """Convert a key mapping table to a character set permutation.

    :arg keymap: Key mapping table.

    :return: Permutation table.
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
    :arg permutation: Permutation table.

    :return: Permuted character set.
    """
    return [charset[index] for index in permutation]


def map_font(
        font: list[list[bytes]], permutation: list[int]) -> list[list[bytes]]:
    """Permute a list of character sets.

    :arg font: List of character sets.
    :arg permutation: Permutation.

    :return: List of permuted character sets.
    """
    return [map_charset(charset, permutation) for charset in font]


def _printable(character: bytes) -> str:
    if character < 0x20:
        return ' '
    if character > 0x7e and character < 0xa0:
        return ' '
    return chr(character)


def visualise_charset(offset: int) -> list[str]:
    """Visualise a character set.

    :arg offset: Start address of the character set.

    :return: Visualition of the character set.
    """
    charset = []
    charset.append('  | ' + ' '.join([f'{i:x}' for i in range(0x10)]))
    charset.append(f'--+{"--" * 0x10}')
    for i in range(0x10):
        charset.append(f'{i:x} |')
        for j in range(0x10):
            charset[-1] += f' {_printable(offset + (i << 4 | j))}'
    return charset
