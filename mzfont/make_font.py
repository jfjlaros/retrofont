from typing import BinaryIO

from .suppress import suppress_output

with suppress_output():
    from fontforge import font as ff_font
from fontforge import open as ff_open
from psMat import scale


def _read_glyphs(handle: BinaryIO) -> list[bytes]:
    data = handle.read()
    return [data[i:i + 8] for i in range(0, len(data), 8)]


def _read_perm(handle: BinaryIO, offset: int) -> list[int]:
    handle.seek(offset)
    return list(handle.read(256))


class Font:
    def __init__(
            self, glyphs_handle: BinaryIO, perm_handle: BinaryIO,
            perm_offset: int, mirror: bool, base_font: str, font_name: str
            ) -> None:
        '''8-bit TrueType font generator.

        :arg glyphs_handle: File handle to character ROM file.
        :arg perm_handle: File handle to monitor ROM file.
        :arg base_font: File name of base font file.
        :arg font_name: Font name.
        '''
        self._glyphs = _read_glyphs(glyphs_handle)
        self._identity = list(range(256))
        self._perm = _read_perm(perm_handle, perm_offset) \
            if perm_handle else self._identity
        self._testbit = self._testbit_little_endian \
            if mirror else self._testbit_big_endian

        with suppress_output():
            self._font = ff_open(base_font)
        self._glyph_width = self._font['space'].width
        self._glyph_height = self._font.em + self._font.os2_typolinegap
        self._glyph_offset = -self._font.descent
        self._set_name(font_name)

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

    def make_charset(self, offset: int, charset: int, perm: bool) -> None:
        print(f'{offset:04x}  {charset} {perm}')
        glyph_offset = 0x100 * charset
        permutation = self._perm if perm else self._identity
        for code in range(0x100):
            self._make_character(
                offset + code,
                self._glyphs[glyph_offset + permutation[code]])

    #def _make_charsets(self) -> None:
    #    # Interchange character set.
    #    self._make_charset(0xe000, 0, self._perm)
    #    # Primary display character set.
    #    self._make_charset(0xe100, 0, self._identity)
    #    # Alternate display character set.
    #    self._make_charset(0xe200, 1, self._identity)

    #def _make_default_charset(self) -> None:
    #    for code in range(0x20, 0x5e):
    #        self._make_character(code, self._glyphs[self._perm[code]])
    #    for code in range(0x61, 0x7b):
    #        self._make_character(code, self._glyphs[0x20 + code])
    #    self._make_character(0x5e, self._glyphs[0xbe])
    #    self._make_character(0x5f, self._glyphs[0x3c])
    #    self._make_character(0x60, self._glyphs[0xa4])
    #    self._make_character(0x7b, self._glyphs[0xbc])
    #    self._make_character(0x7c, self._glyphs[0x35])
    #    self._make_character(0x7d, self._glyphs[0x40])
    #    self._make_character(0x7e, self._glyphs[0xa5])

    def make_font(self, ttf_font: str) -> None:
        '''Generate TrueType font file.

        :arg ttf_font: File name of output font file.
        '''
    #    self._make_charsets()
        self._font.generate(ttf_font)

    def make_default_font(self, ttf_font: str) -> None:
        '''Generate TrueType font file and modify default font.

        :arg ttf_font: File name of output font file.
        '''
        pass
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

    #    self._make_default_charset()
    #    self.make_font(ttf_font)
