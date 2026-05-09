from .suppress import Suppress

with Suppress():
    from fontforge import open as ff_open

from .trace import Tracer


class Font:
    def __init__(self, base_font: str, font_name: str) -> None:
        """8-bit TrueType font generator.

        :arg base_font: File name of base font file.
        :arg font_name: Font name.
        """
        with Suppress():
            self._font = ff_open(base_font)

        self._offset = 0xe000
        self._config()
        self._set_name(font_name)

        self._tracer = Tracer()

    def _config(self) -> None:
        self._glyph_width = self._font['space'].width
        self._glyph_height = self._font.em + self._font.os2_typolinegap
        self._glyph_offset = -self._font.descent

    def _set_name(self, font_name: str) -> None:
        self._font.fontname = font_name
        self._font.familyname = font_name
        self._font.fullname = font_name

    def _draw_path(self, pen: object, path: list[tuple]) -> None:
        width, height = self._glyph_width // 8, self._glyph_height // 8

        x, y = path[0]
        pen.moveTo((width * x, height * y + self._glyph_offset))
        for x, y in path[1:]:
            pen.lineTo((width * x, height * y + self._glyph_offset))
        pen.closePath()

    def _draw_paths(self, code: int) -> None:
        char = self._font.createChar(code)
        char.width = self._glyph_width
        pen = char.glyphPen()
        for path in self._tracer.paths():
            self._draw_path(pen, path)

    def _draw_glyph(self, code: int, glyph: list[bytes]) -> None:
        self._tracer.load_bin(glyph)
        self._tracer.draw()
        self._draw_paths(code)

    def config_primary(self) -> None:
        """Use 8-bit characters in primary font."""
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

    def set_primary(self, charset: list[...]) -> None:
        """Set the primary character set.

        :arg charset: Character set.
        """
        for index, glyph in enumerate(charset):
            self._draw_glyph(index, glyph)

    def add_charset(self, charset: list[...]) -> None:
        """Add a character set to the UTF-8 user area.

        :arg charset: Character set.
        """
        for glyph in charset:
            self._draw_glyph(self._offset, glyph)
            self._offset += 1

    def make_font(self, ttf_font: str) -> None:
        """Generate font file.

        :arg ttf_font: Font file name.
        """
        self._font.generate(ttf_font)
        self._font.close()
