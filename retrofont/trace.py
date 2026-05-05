from sys import stdout


def add(p1, p2):
    r1, c1 = p1
    r2, c2 = p2
    return (r1 + r2, c1 + c2)


def rotate_cw(p):
    r, c = p
    return (c, -r)


def rotate_ccw(p):
    r, c = p
    return (-c, r)


class Glyph:
    def __init__(self):
        self._glyph = [[' ' for _ in range(16)] for _ in range(16)]

    def _get(self, p):
        r, c = p
        if r < 0 or r > 15 or c < 0 or c > 15:
            return ' '
        return self._glyph[r][c]

    def _visit(self, p, d):
        r, c = p
        arrows = {(1, 0): '🡳', (0, 1): '🡲', (-1, 0): '🡱', (0, -1): '🡰'}
        self._glyph[r][c] = arrows[d]

    def _step(self, p, d):
        self._visit(p, d)
        return add(p, d)

    def _navigate(self, p, d):
        if self._get(add(p, d)) == ' ':
            return (p, rotate_cw(d))
        _d = rotate_ccw(d)
        if self._get(add(p, _d)) != ' ':
            return (self._step(p, _d), _d)
        return (self._step(p, d), d)

    def _find_start(self):
        for r in range(16):
            for c in range(16):
                if self._get((r, c)) == '·' and self._get((r - 1, c)) == ' ':
                    yield (r, c)

    def _trace(self, p, d):
        _p, _d = p, d
        while self._get(_p) == '·':
            _p, _d = self._navigate(_p, _d)

    def load(self, glyph):
        for r, line in enumerate(glyph):
            for c, cell in enumerate(line):
                self._glyph[2 * r][2 * c] = cell
                self._glyph[2 * r + 1][2 * c] = cell
                self._glyph[2 * r][2 * c + 1] = cell
                self._glyph[2 * r + 1][2 * c + 1] = cell

    def draw(self):
        for p in self._find_start():
            self._trace(p, (0, 1))

    def print(self):
        for line in self._glyph:
            for cell in line:
                stdout.write(cell)
            stdout.write('\n')


glyphs = [
    [' ······ ',
     '········',
     '··    ··',
     '········',
     '········',
     '··    ··',
     '··    ··',
     '··    ··'],
    ['········',
     '·      ·',
     '· ···· ·',
     '· ·  · ·',
     '· ·  · ·',
     '· ···· ·',
     '·      ·',
     '········'],
    ['    ·   ',
     '     ·  ',
     '   · ·  ',
     '   ··   ',
     '    ·   ',
     '     ···',
     '··   · ·',
     '··   ···']]

glyph = Glyph()
for g in glyphs:
    glyph.load(g)
    glyph.draw()
    glyph.print()
    print(f'\n{16 * '—'}\n')
