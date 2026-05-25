from retrofont.font import (
    rom_to_font, font_to_rom, map_font, keymap_to_permutation, yaml_to_font,
    font_to_yaml, map_charset, visualise_charset)

from shared import test_empty, test_glyph, test_yaml_font, test_text_glyph


_charset = [test_empty, test_glyph] + [test_empty] * 254
_font = [[test_empty] * 256, _charset]
_permutation = list(range(10, 256)) + list(range(10))


def test_rom_to_font():
    font = rom_to_font(test_glyph)
    assert len(font[0]) == 256
    assert font[0][0] == test_glyph
    assert font[0][1] == test_empty


def test_font_to_rom():
    rom = font_to_rom(_font)
    assert len(rom) == 4096
    assert rom[2048:2056] == test_empty
    assert rom[2056:2064] == test_glyph


def test_yaml_to_font():
    font = yaml_to_font(test_yaml_font)
    assert font[2][0] == test_empty
    assert font[2][1] == test_glyph


def test_font_to_yaml():
    yaml_font = font_to_yaml(_font)
    assert len(yaml_font) == 2
    assert yaml_font[1][0]['data'] == test_text_glyph
    assert yaml_font[1][0]['offset'] == 1


def test_keymap_to_permutation():
    permutation = keymap_to_permutation({})
    assert permutation[0] == 0
    assert permutation[0xff] == 0xff
    permutation = keymap_to_permutation(
        {'character_blocks': [[0x20, [0x00, 0x40]]]})
    assert permutation[0x1f] == 0x00
    assert permutation[0x20] == 0x00
    assert permutation[0x5f] == 0x3f
    assert permutation[0x60] == 0x00
    permutation = keymap_to_permutation({'characters': [[0x20, 0x40]]})
    assert permutation[0x1f] == 0x00
    assert permutation[0x20] == 0x40
    assert permutation[0x21] == 0x00


def test_map_charset():
    charset = map_charset(_charset, _permutation)
    assert charset[247] == test_glyph


def test_map_font():
    font = map_font(_font, _permutation)
    assert font[1][247] == test_glyph


def test_visualise_charset():
    visualisation = visualise_charset(0)
    assert len(visualisation) == 18
    assert visualisation[0][6] == '1'
    assert visualisation[6][0] == '4'
    assert visualisation[6][6] == 'A'
