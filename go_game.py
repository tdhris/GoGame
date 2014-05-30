from board_game import BoardGame
from position import Position
from go_player import GoPlayer

"""
Inherited from BoardGame (& relevant):
* properties:
    - board
    - running
    - current_player
    -has_winner

* methods:
    - is_move_valid
    - end_game
    - _check_board_full(self):
"""


class GoGame(BoardGame):
    BLACK = "B"
    WHITE = "W"
    DEFAULT_KOMI = 6.5
    DEFAULT_GOBAN_SIZE = 19
    MAX_PASSES_IN_SUCCESSION = 2

    def __init__(self, size=DEFAULT_GOBAN_SIZE, komi=DEFAULT_KOMI):
        players = [GoPlayer(self.BLACK), GoPlayer(self.WHITE)]
        super(GoGame, self).__init__(players, size)
        self._komi = komi
        self._passes_in_succession = 0

    @property
    def goban(self):
        return self._board

    @property
    def komi(self):
        return self._komi

    @property
    def opponent(self):
        if self.current_player.symbol == self.BLACK:
            return self.players[1]
        else:
            return self.players[0]

    def make_move(self, move):
        if self.running and self.is_move_valid(move):
            self._passes_in_succession = 0
            self.board.place(move, self.current_player.symbol)
            self.current_player.make_move(move)
            self._check_game_state()
            self._change_turn()

    def pass_move(self):
        self.current_player.pass_move()
        self._passes_in_succession += 1
        if self.current_player.two_passes_in_succession():
            self.resign()
        elif self._passes_in_succession == self.MAX_PASSES_IN_SUCCESSION:
            self.end_game()
        else:
            self._change_turn()

    def resign(self):
        self.winner = self.opponent
        self._has_winner = True
        self.end_game()

    def _change_turn(self):
        self._current_player = self.opponent

    def _check_game_state(self):
        self._check_board_full()
        self._capture_stones()

    def _capture_stones(self):
        new_stone = self.current_player.last_move()
        groups = self._get_adjacent_opponent_groups(new_stone)
        for group in groups:
            if self._group_surrounded(group):
                self._remove_group(group)
                self.current_player.capture_stones(*group)

    def _remove_group(self, group):
        for stone in group:
            self._remove_stone(stone)

    def _remove_stone(self, stone):
        self.goban.remove(stone)
        self.current_player.remove_move(stone)

    def _get_adjacent_opponent_groups(self, stone):
        groups = []
        oppositecolor_neighbors = self._get_oppositecolor_neighbors(stone)
        for neighbor in oppositecolor_neighbors:
            if self.goban.at(neighbor) == self.opponent.symbol:
                group = self._get_group(neighbor)
                if group not in groups:
                    groups.append(group)
        return groups

    def _get_group(self, origin):
        group = set([origin])
        neighbors_to_add = self._get_samecolor_neighbors(origin)

        while len(neighbors_to_add) > 0:
            neighbor = neighbors_to_add.pop()
            group.add(neighbor)
            adjacent_to_neighbor = self._get_samecolor_neighbors(neighbor)
            for adjacent in adjacent_to_neighbor:
                if adjacent not in neighbors_to_add and adjacent not in group:
                    neighbors_to_add.add(adjacent)
        return group

    def _get_oppositecolor_neighbors(self, stone):
        oppositecolor_neighbors = set()
        all_neighbors = self._get_neighbors(stone)
        for neighbor in all_neighbors:
            if not self.goban.is_empty(neighbor) and self.goban.at(neighbor) != self.goban.at(stone):
                oppositecolor_neighbors.add(neighbor)
        return oppositecolor_neighbors

    def _get_samecolor_neighbors(self, stone):
        samecolor_neighbors = set()
        all_neighbors = self._get_neighbors(stone)
        for neighbor in all_neighbors:
            if not self.goban.is_empty(neighbor) and self.goban.at(neighbor) == self.goban.at(stone):
                samecolor_neighbors.add(neighbor)
        return samecolor_neighbors

    def _group_surrounded(self, group):
        for stone in group:
            if self._has_at_least_one_liberty(stone):
                return False
        return True

    def _has_at_least_one_liberty(self, stone):
        neighbors = self._get_neighbors(stone)
        for neighbor in neighbors:
            if self.goban.is_empty(neighbor):
                return True
        return False

    def _get_neighbors(self, stone):
        neighbors = set()
        if stone.x > 0:
            upper = Position(stone.x - 1, stone.y)
            neighbors.add(upper)

        if stone.x < self.goban.size - 1:
            lower = Position(stone.x + 1, stone.y)
            neighbors.add(lower)

        if stone.y > 0:
            left = Position(stone.x, stone.y - 1)
            neighbors.add(left)

        if stone.y < self.goban.size - 1:
            right = Position(stone.x, stone.y + 1)
            neighbors.add(right)
        return neighbors
