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
        self._paths = []

    def _get(self, p):
        r, c = p
        if r < 0 or r > 15 or c < 0 or c > 15:
            return ' '
        return self._glyph[r][c]

    def _visit(self, p, d):
        r, c = p
        arrows = {(1, 0): '🡳', (0, 1): '🡲', (-1, 0): '🡱', (0, -1): '🡰'}
        self._glyph[r][c] = arrows[d]
        #self.print()

    def _path_add(self):
        self._paths.append([])

    def _path_append(self, p):
        r, c = p
        self._paths[-1].append(((r + 1) // 2, (c + 1) // 2))

    def _step(self, p, d):
        self._visit(p, d)
        return add(p, d)

    def _navigate(self, p, d):
        if self._get(add(p, d)) == ' ':
            self._path_append(p)
            return (p, rotate_cw(d))
        _d = rotate_ccw(d)
        if self._get(add(p, _d)) != ' ':
            self._path_append(p)
            return (self._step(p, _d), _d)
        return (self._step(p, d), d)

    def _is_start(self, p):
        return self._get(p) == '·' and self._get(add(p, (-1, 0))) == ' '

    def _find_start(self):
        for r in range(16):
            for c in range(16):
                if self._is_start((r, c)):
                    yield (r, c)

    def _prepend_inner(self, p):
        _p = add(p, (0, -1))
        if self._get(_p) == '·':
            self._visit(add(p, (0, -1)), (0, 1))

    def _trace(self, p, d):
        _p, _d = p, d
        self._prepend_inner(p)
        while self._get(_p) == '·':
            _p, _d = self._navigate(_p, _d)

    def _load(self, p, cell):
        r, c = p
        self._glyph[2 * r][2 * c] = cell
        self._glyph[2 * r + 1][2 * c] = cell
        self._glyph[2 * r][2 * c + 1] = cell
        self._glyph[2 * r + 1][2 * c + 1] = cell

    def load(self, glyph):
        for r, line in enumerate(glyph):
            for c, cell in enumerate(line):
                self._load((r, c), cell)
        self._paths = []

    def load_bin(self, glyph):
        for r, line in enumerate(glyph):
            for c in range(8):
                self._load((7 - c, 7 - r), '·' if line & 1 << c else ' ')
        self._paths = []

    def draw(self):
        for p in self._find_start():
            self._path_add()
            self._path_append(p)
            self._trace(p, (0, 1))

    def paths(self):
        return self._paths

    def print(self):
        for line in self._glyph:
            for cell in line:
                stdout.write(cell)
            stdout.write('\n')
        stdout.write('\n')
        for path in self.paths():
            stdout.write(f'{str(path)}\n')
        stdout.write('\n')


if __name__ == '__main__':
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
    
    glyph_bin = [
        0b11111111,
        0b10000001,
        0b10111101,
        0b10100101,
        0b10100101,
        0b10111101,
        0b10000001,
        0b11111111]
    
    glyph = Glyph()
    glyph.load_bin(glyph_bin)
    glyph.draw()
    glyph.print()
    #for g in glyphs:
    #    glyph.load(g)
    #    glyph.draw()
    #    glyph.print()
