from sys import stdout


class Drawing:
    def __init__(self):
        self._drawing = [[' '] * 17 for _ in range(17)]

    def set(self, p, cell):
        r, c = p
        self._drawing[2 * r + 1][2 * c + 1] = cell

    def get(self, p):
        r, c = p
        return drawing[2 * r + 1][2 * c + 1]

    def border(self, p, d):
        r, c = p
        dr, dc = d
        if self._drawing[2 * r + dr + 1][2 * c + dc + 1] != ' ':
            print('OI')
        #self._drawing[2 * r + dr + 1][2 * c + dc + 1] = '—' if dr else '|'
        arrows = {(0, 1): 'v', (-1, 0): '>', (0, -1): '^', (1, 0): '<'}
        self._drawing[2 * r + dr + 1][2 * c + dc + 1] = arrows[d]

    def print(self):
        for line in self._drawing:
            for cell in line:
                stdout.write(cell)
            stdout.write('\n')

    def add_glyph(self, glyph):
        for r, line in enumerate(glyph):
            for c, cell in enumerate(line):
                if cell == '#':
                    self.set((r, c), cell)


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
        self._glyph = [[cell for cell in line] for line in glyph]
        self._position = (0, 0)
        self._direction = (0, 1)

    def set(self, p, cell):
        r, c = p
        self._glyph[r][c] = cell

    def get(self, p):
        r, c = p
        if r < 0 or r > 7 or c < 0 or c > 7:
            return ' '
        return self._glyph[r][c]

    def position(self):
        r, c = self._position
        return self._glyph[r][c]

    def rotate_cw(self):
        self._direction = rotate_cw(self._direction)

    def rotate_ccw(self):
        self._direction = rotate_ccw(self._direction)

    def navigate(self):
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
        self.set(self._position, '·')
        self._position = add(self._position, self._direction)

    def find(self):
        for r in range(8):
            for c in range(8):
                if self.get((r, c)) != ' ':
                    self._position = (r, c)
                    return

    def trace(self, drawing):
        start = self._position
        start_direction = self._direction
        position = (-1, -1)
        direction = (-1, -1)
        while position != start or direction != start_direction:
            drawing.border(self._position, rotate_ccw(self._direction))
            self.navigate()
            position = self._position
            direction = self._direction
            #drawing.print()
            #print()

    def print(self):
        for line in self._glyph:
            for cell in line:
                stdout.write(cell)
            stdout.write('\n')


glyph_test = [' ###### ',
              '########',
              '##    ##',
              '########',
              '########',
              '##    ##',
              '##    ##',
              '##    ##']

#glyph_test = ['########',
#              '       #',
#              '########',
#              '#       ',
#              '#       ',
#              '########',
#              '       #',
#              '########']

#glyph_test = ['########',
#              '#      #',
#              '# #### #',
#              '# #  # #',
#              '# #  # #',
#              '# #### #',
#              '#      #',
#              '########']

#glyph_test = ['        ',
#              '        ',
#              '     #  ',
#              '   # #  ',
#              '   ##   ',
#              '    #   ',
#              '        ',
#              '        ']

drawing = Drawing()
#drawing.add_glyph(glyph_test)

glyph = Glyph(glyph_test)
glyph.find()
glyph.trace(drawing)
glyph.print()
print()

glyph._position = (1, 2)
glyph._direction = (0, -1)
glyph.trace(drawing)
glyph.print()
print()

drawing.print()
