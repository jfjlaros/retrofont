from copy import copy
from sys import stdout


def double(iterable):
    result = []
    for item in iterable:
        result += [copy(item), copy(item)]
    return result


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
    def __init__(self, glyph):
        self._glyph = double([double(line) for line in glyph])
        self._position = (0, 0)
        self._direction = (0, 1)

    def get(self, p):
        r, c = p
        if r < 0 or r > 15 or c < 0 or c > 15:
            return ' '
        return self._glyph[r][c]

    def rotate_cw(self):
        self._direction = rotate_cw(self._direction)

    def rotate_ccw(self):
        self._direction = rotate_ccw(self._direction)

    def visit(self, p):
        r, c = p
        arrows = {(1, 0): '🡳', (0, 1): '🡲', (-1, 0): '🡱', (0, -1): '🡰'}
        self._glyph[r][c] = arrows[self._direction]

    def step(self):
        next_position = add(self._position, self._direction)
        if self.get(next_position) == ' ':
            self.rotate_cw()
            return

        next_border = add(next_position, rotate_ccw(self._direction))
        if self.get(next_border) != ' ':
            self.next()
            self.rotate_ccw()
        self.next()

    def next(self):
        self.visit(self._position)
        self._position = add(self._position, self._direction)

    def find(self):
        for r in range(16):
            for c in range(16):
                if self.get((r, c)) == '·' and self.get((r - 1, c)) == ' ':
                    yield (r, c)

    def trace(self, p):
        start = self._position
        start_direction = self._direction
        position = (-1, -1)
        direction = (-1, -1)
        while position != start or direction != start_direction:
            self.step()
            position = self._position
            direction = self._direction

    def draw(self):
        for p in self.find():
            self._position = p
            self.trace(p)

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
     '       ·',
     '········',
     '·       ',
     '·       ',
     '········',
     '       ·',
     '········'],
    ['········',
     '·      ·',
     '· ···· ·',
     '· ·  · ·',
     '· ·  · ·',
     '· ···· ·',
     '·      ·',
     '········'],
    ['· · · · ',
     ' · · · ·',
     '· · · · ',
     ' · · · ·',
     '· · · · ',
     ' · · · ·',
     '· · · · ',
     ' · · · ·'],
    ['    ·   ',
     '     ·  ',
     '   · ·  ',
     '   ··   ',
     '    ·   ',
     '     ···',
     '··   · ·',
     '··   ···']]

glyph = Glyph(glyphs[0])
glyph.draw()
glyph.print()
