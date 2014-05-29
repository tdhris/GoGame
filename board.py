class Board:
    EMPTY_FIELD = None
    DEFAULT_BOARD_SIZE = 3

    def __init__(self, size=DEFAULT_BOARD_SIZE):
        self._size = size
        self._board = self._generate_empty_board()

    @property
    def size(self):
        return self._size

    def at(self, position):
        if self.is_iniside_board(position):
            return self._board[position.x][position.y]

    def place(self, position, symbol):
        if self.is_iniside_board(position):
            self._board[position.x][position.y] = symbol

    def remove(self, position):
        self.place(position, self.EMPTY_FIELD)

    def is_empty(self, position):
        return self._board[position.x][position.y] == self.EMPTY_FIELD

    def is_board_full(self):
        for row in self._board:
            for element in row:
                if element is self.EMPTY_FIELD:
                    return False
        return True

    def is_board_empty(self):
        for row in self._board:
            for element in row:
                if element is not self.EMPTY_FIELD:
                    return False
        return True

    def count_taken_fields(self):
        count = 0
        for row in self._board:
            for element in row:
                if element is not self.EMPTY_FIELD:
                    count += 1
        return count

    def count_empty_fields(self):
        return (self.size ** 2) - self.count_taken_fields()

    def clear_board(self):
        self._board = self._generate_empty_board()

    def is_iniside_board(self, position):
        return self._point_inside_board(position.x) and\
            self._point_inside_board(position.y)

    def _generate_empty_board(self):
        return [[self.EMPTY_FIELD] * self.size for row in range(self.size)]

    def _point_inside_board(self, point):
        return point >= 0 and point < self.size
