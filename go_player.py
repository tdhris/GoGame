from board_game_player import BoardGamePlayer

class GoPlayer(BoardGamePlayer):
    def __init__(self, symbol):
        super(GoPlayer, self).__init__(symbol)
        self._captured_stones = 0

    @property
    def stones(self):
        return self._moves

    @property
    def captured_stones(self):
        return self._captured_stones

    def capture_stone(self):
        self._captured_stones += 1
