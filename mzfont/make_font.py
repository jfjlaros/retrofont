from typing import BinaryIO

from .math import make_matrix, pad
from .suppress import Suppress

with Suppress():
    from fontforge import font as ff_font
from fontforge import open as ff_open
from psMat import scale


def _read_cgrom(handle: BinaryIO) -> list[bytes]:
    data = handle.read()
    data += b'\x00' * pad(len(data), 256)
    return make_matrix(data, (256, 8))


def _read_firmware(handle: BinaryIO, offset: int) -> list[int]:
    handle.seek(offset)
    return list(handle.read(256))


class Font:
    def __init__(
            self, cgrom_handle: BinaryIO, base_font: str, font_name: str,
            firmware_handle: BinaryIO=None, firmware_offset: int=0,
            mirror: bool=False, default: list=[]) -> None:
        '''8-bit TrueType font generator.

        :arg cgrom_handle: File handle to character ROM file.
        :arg base_font: File name of base font file.
        :arg font_name: Font name.
        :arg firmware_handle: File handle to firmware ROM file.
        :arg firmware_offset: Location of the map in the firmware.
        :arg mirror: Mirror glyphs.
        :arg default: Generate default font.
        '''
        self._cgrom = _read_cgrom(cgrom_handle)

        self._firmware_map = b''
        if firmware_handle:
            self._firmware_map = _read_firmware(
                firmware_handle, firmware_offset)

        if mirror:
            self._testbit = self._testbit_little_endian
        else:
            self._testbit = self._testbit_big_endian

        self._char_offset = 0xe000

        with Suppress():
            self._font = ff_open(base_font)

        if default:
            self._config_default_font()
            self._make_default_charset(default)
        else:
            self._config_font()

        self._set_name(font_name)
        self.make_charsets()

    def _config_font(self) -> None:
        self._glyph_width = self._font['space'].width
        self._glyph_height = self._font.em + self._font.os2_typolinegap
        self._glyph_offset = -self._font.descent

    def _config_default_font(self) -> None:
        self._glyph_width = self._font.em
        self._glyph_height = self._font.em
        self._glyph_offset = 0

        self._font.ascent = self._font.em
        self._font.descent = 0

        self._font.os2_typoascent = self._font.ascent
        self._font.os2_typodescent = -self._font.descent
        self._font.os2_typolinegap = 0

        self._font.os2_winascent = self._font.ascent
        self._font.os2_windescent = self._font.descent

        self._font.hhea_ascent = self._font.ascent
        self._font.hhea_descent = -self._font.descent
        self._font.hhea_linegap = 0

    def _set_name(self, font_name: str) -> None:
        self._font.fontname = font_name
        self._font.familyname = font_name
        self._font.fullname = font_name

    def _draw_pixel(self, pen: object, x: int, y: int) -> None:
        width, height = self._glyph_width // 8, self._glyph_height // 8
        pen.moveTo((width * x, height * (8 - y) + self._glyph_offset))
        pen.lineTo((width * (x + 1), height * (8 - y) + self._glyph_offset))
        pen.lineTo((width * (x + 1), height * (7 - y) + self._glyph_offset))
        pen.lineTo((width * x, height * (7 - y) + self._glyph_offset))
        pen.closePath()

    def _testbit_big_endian(self, byte: int, position: int) -> bool:
        return byte & (1 << (7 - position))

    def _testbit_little_endian(self, byte: int, position: int) -> bool:
        return byte & (1 << position)

    def _make_character(self, code: int, glyph: list[bytes]) -> None:
        char = self._font.createChar(code)
        char.width = self._glyph_width

        pen = char.glyphPen()
        for y in range(8):
            for x in range(8):
                if self._testbit(glyph[y], x):
                    self._draw_pixel(pen, x, y)
        self._char_offset += 1  # Hmmm.

    def _ident(self, value: int) -> int:
        return value

    def _map(self, value: int) -> int:
        return self._firmware_map[value]

    def _make_charsets(self, f: callable) -> None:
        for charset in self._cgrom:
            for i, _ in enumerate(charset):
                self._make_character(self._char_offset, charset[f(i)])

    def make_charsets(self) -> None:
        self._char_offset = 0xe000
        if self._firmware_map:
            self._make_charsets(self._map)
        self._make_charsets(self._ident)

    def _map_default(self, item: dict, f: callable) -> None:
        charset = self._cgrom[0]

        if 'range' not in item:
            for src, dest in item['values']:
                self._make_character(src, charset[f(dest)])
            return

        offset = item.get('offset', 0)
        for code in range(*item['range']):
            self._make_character(code, charset[f(offset + code)])

    def _make_default_charset(self, default: list[dict]) -> None:
        for item in default:
            if item['source'] == 'map':
                self._map_default(item, self._map)
            else:
                self._map_default(item, self._ident)

    def make_font(self, ttf_font: str) -> None:
        '''Generate TrueType font file.

        :arg ttf_font: File name of output font file.
        '''
        self._font.generate(ttf_font)

    #def make_default_font(self, ttf_font: str, default: dict) -> None:
    #    '''Generate TrueType font file and modify default font.

    #    :arg ttf_font: File name of output font file.
    #    :arg devault: Default font mappings.
    #    '''
    #    self._glyph_width = self._font.em
    #    self._glyph_height = self._font.em
    #    self._glyph_offset = 0

    #    self._font.ascent = self._font.em
    #    self._font.descent = 0

    #    self._font.os2_typoascent = self._font.ascent
    #    self._font.os2_typodescent = -self._font.descent
    #    self._font.os2_typolinegap = 0

    #    self._font.os2_winascent = self._font.ascent
    #    self._font.os2_windescent = self._font.descent

    #    self._font.hhea_ascent = self._font.ascent
    #    self._font.hhea_descent = -self._font.descent
    #    self._font.hhea_linegap = 0

    #    self._make_default_charset(default)
    #    self.make_font(ttf_font)
