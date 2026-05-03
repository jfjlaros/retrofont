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
        arrows = {(0, 1): '🡳', (-1, 0): '🡲', (0, -1): '🡱', (1, 0): '🡰'}
        self._drawing[2 * r + dr + 1][2 * c + dc + 1] = arrows[d]
        #self.print()

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


#class Pixel:
#    def __init__(self, bit):
#        self._bit = bit
#        self._border_right = ' '
#        self._border_down = ' '
#        self._border_left = ' '
#        self._border_up = ' '
#
#    def arrow(self, direction):
#        arrows = ('🡳', '🡲', '🡱', '🡰')
#
#    def print(self, row):
#        if (row == 0):
#            print(f'  ')


    
class Glyph:
    _occupied = 0b10000000
    _visited  = 0b01000000

    def __init__(self, glyph):
        #self._glyph = [[cell for cell in line] for line in glyph]
        self._glyph = [[self._occupied if cell == '#' else 0 for cell in line] for line in glyph]
        self._position = (0, 0)
        self._direction = (0, 1)

    #def set(self, p, cell):
    #    r, c = p
    #    self._glyph[r][c] = cell

    def visit(self, p):
        r, c = p
        self._glyph[r][c] |= self._visited

    #def get(self, p):
    #    r, c = p
    #    if r < 0 or r > 7 or c < 0 or c > 7:
    #        return ' '
    #    return self._glyph[r][c]

    def get(self, p):
        r, c = p
        if r < 0 or r > 7 or c < 0 or c > 7:
            return 0
        return self._glyph[r][c]

    #def position(self):
    #    r, c = self._position
    #    return self._glyph[r][c]

    def rotate_cw(self):
        self._direction = rotate_cw(self._direction)

    def rotate_ccw(self):
        self._direction = rotate_ccw(self._direction)

    #def navigate(self):
    #    next_position = add(self._position, self._direction)
    #    if self.get(next_position) == ' ':
    #        self.rotate_cw()
    #        return

    #    next_border = add(next_position, rotate_ccw(self._direction))
    #    if self.get(next_border) != ' ':
    #        self.next()
    #        self.rotate_ccw()
    #    self.next()

    def navigate(self):
        next_position = add(self._position, self._direction)
        if not (self.get(next_position) & self._occupied):
            self.rotate_cw()
            return

        next_border = add(next_position, rotate_ccw(self._direction))
        if self.get(next_border) & self._occupied:
            self.next()
            self.rotate_ccw()
        self.next()

    #def next(self):
    #    self.set(self._position, '·')
    #    self._position = add(self._position, self._direction)

    def next(self):
        self.visit(self._position)
        self._position = add(self._position, self._direction)

    #def find(self):
    #    for r in range(8):
    #        for c in range(8):
    #            if self.get((r, c)) != ' ':
    #                self._position = (r, c)
    #                return

    def find(self):
        for r in range(8):
            for c in range(8):
                if self.get((r, c)) & self._occupied:
                    self._position = (r, c)
                    return

    #def trace(self, drawing):
    #    start = self._position
    #    start_direction = self._direction
    #    position = (-1, -1)
    #    direction = (-1, -1)
    #    while position != start or direction != start_direction:
    #        drawing.border(self._position, rotate_ccw(self._direction))
    #        self.navigate()
    #        position = self._position
    #        direction = self._direction
    #        #drawing.print()
    #        #print()

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

    #def print(self):
    #    for line in self._glyph:
    #        for cell in line:
    #            stdout.write(cell)
    #        stdout.write('\n')

    def pictogram(self, cell):
        if cell & self._visited:
            return '·'
        if cell & self._occupied:
            return '#'
        return ' '

    def print(self):
        for line in self._glyph:
            for cell in line:
                stdout.write(self.pictogram(cell))
            stdout.write('\n')


glyph_test = [' ###### ',
              '########',
              '##    ##',
              '########',
              '########',
              '##    ##',
              '##    ##',
              '##    ##']

glyph_bin = [0b01111110,
             0b11111111,
             0b11000011,
             0b11111111,
             0b11111111,
             0b11000011,
             0b11000011,
             0b11000011]

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
