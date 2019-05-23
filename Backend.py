import random

import numpy


class Game:
    def __init__(self, row, col, bombs):
        self._row = row
        self._col = col
        self._bombs = bombs

        self._marked = [[0 for _ in range(col)] for _ in range(row)]
        self._board = [[0 for _ in range(col)] for _ in range(row)]
        self._board = self.build_board(bombs)

        self._counter = 0
        self._end = False
        self._fields = row * col

    def generate(self, cc, rr):
        for ccc in range(cc - 1, cc + 2):
            for rrr in range(rr - 1, rr + 2):
                if self._col > ccc >= 0 and self._row > rrr >= 0 and self._board[rrr][ccc] != 9:
                    yield rrr, ccc

    def generate2(self):
        for r in range(self._row):
            for c in range(self._col):
                yield r, c

    def build_board(self, bombs):
        temp = 0
        while temp < bombs:
            bombsRow = random.randint(0, self._row - 1)
            bombsCol = random.randint(0, self._col - 1)
            if self._board[bombsRow][bombsCol] != 9:
                self._board[bombsRow][bombsCol] = 9
                temp += 1
        for rr in range(self._row):
            for cc in range(self._col):
                if self._board[rr][cc] == 9:
                    for rrr, ccc in self.generate(cc, rr):
                        self._board[rrr][ccc] += 1
        return self._board

    def print_board(self):
        print(numpy.array(self._board))

    def xyzzy(self):
        bombs = []
        for rr in range(self._row):
            for cc in range(self._col):
                if self._board[rr][cc] == 9:
                    bombs.append((rr, cc))
        return bombs

    def won(self):
        if self._fields == self._bombs:
            self._end = True
            return True
        elif self._counter == self._bombs:
            for r, c in self.generate2():
                if self._board[r][c] == 9 and self._marked[r][c] != 1:
                    break
            else:
                self._end = True
                return True
        return False

    def add_marked(self, r, c):
        self._marked[r][c] += 1
        self._marked[r][c] %= 3

    def ret_marked(self, r, c):
        return self._marked[r][c]

    def add_counter(self):
        self._counter += 1

    def sub_counter(self):
        self._counter -= 1

    def ret_counter(self):
        return self._counter

    def field(self):
        self._fields -= 1

    def check_neighbours(self, r, c, retval):
        if self._board[r][c] == 9:
            self._end = True
            return False
        else:
            self._fields -= 1
            self._marked[r][c] = 3
            if self._board[r][c] == 0:
                for rr in [r - 1, r, r + 1]:
                    for cc in [c - 1, c, c + 1]:
                        if 0 <= cc < self._col and 0 <= rr < self._row:
                            if self._marked[rr][cc] != 3:
                                self.check_neighbours(rr, cc, retval)
            retval.append((r, c))
        return True

    def ret_value(self, r, c):
        return self._board[r][c]

    def is_end(self):
        return self._end

    def is_bomb(self, r, c):
        return self._board[r][c] == 9


if __name__ == "__main__":
    g1 = Game(6, 9, 10)
    g1.print_board()
