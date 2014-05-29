class BoardGamePlayer:
    def __init__(self, symbol):
        self._symbol = symbol
        self._moves = []

    @property
    def symbol(self):
        return self._symbol

    @property
    def moves(self):
        return self._moves

    def make_move(self, move):
        self._moves.append(move)

    def remove_move(self, move):
        if move in self.moves:
            self._moves.remove(move)
