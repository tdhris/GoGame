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

    def capture_stones(self, *stones):
        for stone in stones:
            self._captured_stones += 1

    def last_move(self):
        last = len(self.stones) - 1
        return self.stones[last]
