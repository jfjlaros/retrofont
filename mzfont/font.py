from fontforge import open as ff_open

from .suppress import Suppress


class Font:
    def __init__(
            self, base_font: str, font_name: str, native: bool=False) -> None:
        """8-bit TrueType font generator.

        :arg base_font: File name of base font file.
        :arg font_name: Font name.
        """
        with Suppress():
            self._font = ff_open(base_font)

        self._offset = 0xe000
        self._set_name(font_name)

        if native:
            self._config_native()
        else:
            self._config()

    def _config(self) -> None:
        self._glyph_width = self._font['space'].width
        self._glyph_height = self._font.em + self._font.os2_typolinegap
        self._glyph_offset = -self._font.descent

    def _set_name(self, font_name: str) -> None:
        self._font.fontname = font_name
        self._font.familyname = font_name
        self._font.fullname = font_name

    def config_native(self) -> None:
        """Configure font to use 8-bit characters natively."""
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

    def _testbit(self, byte: int, position: int) -> bool:
        return byte & (1 << (7 - position))

    def _draw_pixel(self, pen: object, x: int, y: int) -> None:
        width, height = self._glyph_width // 8, self._glyph_height // 8
        pen.moveTo((width * x, height * (8 - y) + self._glyph_offset))
        pen.lineTo((width * (x + 1), height * (8 - y) + self._glyph_offset))
        pen.lineTo((width * (x + 1), height * (7 - y) + self._glyph_offset))
        pen.lineTo((width * x, height * (7 - y) + self._glyph_offset))
        pen.closePath()

    def _draw_glyph(self, code: int, glyph: list[bytes]) -> None:
        char = self._font.createChar(code)
        char.width = self._glyph_width

        pen = char.glyphPen()
        for y in range(8):
            for x in range(8):
                if self._testbit(glyph[y], x):
                    self._draw_pixel(pen, x, y)

    def add_charset(self, charset: list[...]) -> None:
        """Add a character set to the UTF-8 user area.

        :arg charset: Character set.
        """
        for glyph in charset:
            self._draw_glyph(self._offset, glyph)
            self._offset += 1

    def native_charset(self, charset: list[...]) -> None:
        """Set the native character set.

        :arg charset: Character set.
        """
        for index, glyph in enumerate(charset):
            self._draw_glyph(index, glyph)

    def make_font(self, ttf_font: str) -> None:
        """Generate font file.

        :arg ttf_font: Font file name.
        """
        self._font.generate(ttf_font)
