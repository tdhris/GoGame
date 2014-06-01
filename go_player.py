from board_game_player import BoardGamePlayer


class GoPlayer(BoardGamePlayer):
    MAX_PASSES_IN_SUCCESSION = 2

    def __init__(self, symbol):
        super(GoPlayer, self).__init__(symbol)
        self._captured_stones = set()
        self._captured_stones_count = 0
        self._passes_in_succession_count = 0
        self.territory = 0

    @property
    def stones(self):
        return self._moves

    @property
    def captured_stones(self):
        return self._captured_stones

    @property
    def captured_stones_count(self):
        return self._captured_stones_count

    def capture_stones(self, *stones):
        for stone in stones:
            if stone not in self.captured_stones:
                self._captured_stones_count += 1
                self._captured_stones.add(stone)

    def make_move(self, move):
        super(GoPlayer, self).make_move(move)
        self._passes_in_succession_count = 0

    def last_move(self):
        last = len(self.stones) - 1
        return self.stones[last]

    def pass_move(self):
        self._passes_in_succession_count += 1

    def two_passes_in_succession(self):
        return self._passes_in_succession_count == 2
