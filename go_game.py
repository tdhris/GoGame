from board_game import BoardGame

class GoGame(BoardGame):
    BLACK = "B"
    WHITE = "W"
    DEFAULT_KOMI = 6.5
    DEFAULT_GOBAN_SIZE = 19

    def __init__(self, size=DEFAULT_GOBAN_SIZE, komi=DEFAULT_KOMI):
        players = [self.BLACK, self.WHITE]
        super(GoGame, self).__init__(players, size)
        self._komi = komi

    @property
    def goban(self):
        return self._board

    @property
    def komi(self):
        return self._komi

    @property
    def opponent(self):
        return self._get_next_player()

    def make_move(self, move):
        super(GoGame, self).make_move(move)
        self.check_game_state()

    def check_game_state(self):
        pass