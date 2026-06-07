from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen

from .trace import Tracer, get_lsb


class TTF:
    """TrueType font generator."""
    def __init__(self, base_font: str, font_name: str) -> None:
        """
        :arg base_font: File name of base font file.
        :arg font_name: Font name.
        """
        self._font = TTFont(base_font)
        self._glyphs = self._font.getGlyphSet()

        self._offset = 0xe000
        self._config()
        self._set_name(font_name)

        self._cmap_tables = list(
            filter(lambda x: x.isUnicode(), self._font['cmap'].tables))

        self._tracer = Tracer()

    def _config(self) -> None:
        self._glyph_width = self._glyphs.get('space').width
        self._glyph_offset = self._font['OS/2'].sTypoDescender
        self._glyph_height = (
            self._font['OS/2'].sTypoAscender +
            self._font['OS/2'].sTypoLineGap - self._glyph_offset)

    def _set_name(self, font_name: str) -> None:
        self._font['name'].setName(font_name, 1, 3, 1, 0x409)
        self._font['name'].setName('Regular', 2, 3, 1, 0x409)
        self._font['name'].setName(f'{font_name} Regular', 4, 3, 1, 0x409)
        self._font['name'].setName(f'{font_name}-Regular', 6, 3, 1, 0x409)

    def _draw_path(self, pen: object, path: list[int]) -> None:
        width, height = self._glyph_width // 8, self._glyph_height // 8

        r, c = path[0]
        pen.moveTo((width * c, height * (8 - r) + self._glyph_offset))
        for r, c in path[1:]:
            pen.lineTo((width * c, height * (8 - r) + self._glyph_offset))
        pen.closePath()

    def _draw_paths(self, code: int) -> None:
        paths = self._tracer.get_paths()
        pen = TTGlyphPen(self._glyphs)
        for path in paths:
            self._draw_path(pen, path)

        glyph_name = f'uni{code:04x}'
        self._font['glyf'][glyph_name] = pen.glyph()

        lsb = get_lsb(paths) * self._glyph_width // 8
        self._font['hmtx'][glyph_name] = (self._glyph_width, lsb)

        for table in self._cmap_tables:
            table.cmap[code] = glyph_name

    def _draw_glyph(self, code: int, glyph: bytes) -> None:
        self._tracer.load(glyph)
        self._tracer.trace()
        self._draw_paths(code)

    def config_primary(self) -> None:
        """Use 8-bit characters in primary font."""
        self._glyph_width = 2048
        self._glyph_height = self._glyph_width
        self._glyph_offset = 0

        self._font['OS/2'].sTypoAscender = self._glyph_height
        self._font['OS/2'].sTypoDecender = 0
        self._font['OS/2'].sTypoLineGap = 0

        self._font['OS/2'].usWinAscent = self._glyph_height
        self._font['OS/2'].usWinDescent = 0

        self._font['hhea'].ascent = self._glyph_height
        self._font['hhea'].descent = 0
        self._font['hhea'].linegap = 0

    def set_primary(self, charset: list[bytes]) -> None:
        """Set the primary character set.

        :arg charset: Character set.
        """
        for index, glyph in enumerate(charset):
            self._draw_glyph(index, glyph)

    def add_charset(self, charset: list[bytes]) -> None:
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
        self._font.save(ttf_font)
        self._font.close()
