from board_game import BoardGame
from position import Position
from go_player import GoPlayer


class GoGame(BoardGame):
    BLACK = "B"
    WHITE = "W"
    DEFAULT_KOMI = 6.5
    DEFAULT_GOBAN_SIZE = 19

    def __init__(self, size=DEFAULT_GOBAN_SIZE, komi=DEFAULT_KOMI):
        players = [GoPlayer(self.BLACK), GoPlayer(self.WHITE)]
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
        self._check_game_state()

    def _check_game_state(self):
        self._capture_stones()

    def _capture_stones(self):
        for stone in self.current_player.stones:
            if not self._has_at_least_one_liberty(stone):
                self._remove_stone(stone)

    def _has_at_least_one_liberty(self, stone):
        if stone.x > 0:
            upper = Position(stone.x - 1, stone.y)
            if self.goban.is_empty(upper):
                return True

        if stone.x < self.goban.size:
            lower = Position(stone.x + 1, stone.y)
            if self.goban.is_empty(lower):
                return True

        if stone.y > 0:
            left = Position(stone.x, stone.y - 1)
            if self.goban.is_empty(left):
                return True

        if stone.y < self.goban.size:
            right = Position(stone.x, stone.y + 1)
            if self.goban.is_empty(right):
                return True
        return False

    def _remove_stone(self, stone):
        self.goban.remove(stone)
        self.current_player.remove_move(stone)

    def _check_all_stones_have_liberties(self):
        pass
