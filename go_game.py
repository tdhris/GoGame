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
    TWO_EYES = 2

    def __init__(self, size=DEFAULT_GOBAN_SIZE, komi=DEFAULT_KOMI):
        self._players = [GoPlayer(self.BLACK), GoPlayer(self.WHITE)]
        super(GoGame, self).__init__(self._players, size)
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

    @property
    def black_player(self):
        return self._players[0]
    
    @property
    def white_player(self):
        return self._players[1]

    def make_move(self, move):
        if self.running and self.is_move_valid(move) and self.board.is_empty(move):
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
        self._end_game()

    def _end_game(self):
        self._count_territory()
        self._running = False

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

    def _count_territory(self):
        for player in self._players:
            teritory = 0
            player_groups = self._get_player_groups(player)
            for group in player_groups:
                teritory += self._count_territory_surrounded(group)
            player.territory = teritory

    def _count_territory_surrounded(self, group):
        territory = 0
        common_empty_neighbors = self._get_common_empty_neighbors(group)
        processed = []
        for common_empty_neighbor in common_empty_neighbors:
            if common_empty_neighbor not in processed:
                processed.append(common_empty_neighbor)
                empty_neighbor_group = self._get_group(common_empty_neighbor)
                for empty_neighbor in empty_neighbor_group:
                    processed.append(empty_neighbor)
                if self._territory_surrounded(empty_neighbor_group, group):
                    territory += len(empty_neighbor_group)
        return territory

    def _get_player_groups(self, player=None):
        if player is None:
            player = self.current_player
        player_groups = []
        for stone in player.stones:
            stone_group = self._get_group(stone)
            if stone_group not in player_groups:
                player_groups.append(stone_group)
        return player_groups

    def _get_adjacent_opponent_groups(self, stone):
        groups = []
        oppositecolor_neighbors = self._get_oppositecolor_neighbors(stone)
        for neighbor in oppositecolor_neighbors:
            if self.goban.at(neighbor) == self.opponent.symbol:
                group = self._get_group(neighbor)
                if group not in groups:
                    groups.append(group)
        return groups

    def _get_empty_neighbors_of_group(self, group):
        all_empty_neighbors = set()
        for stone in group:
            empty_neighbors = self._get_empty_neighbors(stone)
            for neighbor in empty_neighbors:
                all_empty_neighbors.add(neighbor)
        return all_empty_neighbors

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
        return set([neighbor for neighbor in self._get_neighbors(stone) if self._oppositecolor_stone(neighbor, stone)])

    def _get_samecolor_neighbors(self, stone):
        return set([neighbor for neighbor in self._get_neighbors(stone) if self._samecolor_stone(neighbor, stone)])

    def _get_empty_neighbors(self, stone):
        return set([neighbor for neighbor in self._get_neighbors(stone) if self.goban.is_empty(neighbor)])

    def _territory_surrounded(self, territory, player_group):
        if self._get_empty_neighbors_of_group(player_group).issubset(territory):
            return False

        surrounded = True
        player_stone = next(iter(player_group))
        for field in territory:
            adjacent_fields = self._get_neighbors(field)
            for adjacent in adjacent_fields:
                if self._oppositecolor_stone(adjacent, player_stone):
                    surrounded = False
        return surrounded

    def _get_common_empty_neighbors(self, group):
        common_empty_neighbors = set()
        for empty_neighbor in self._get_empty_neighbors_of_group(group):
            adjacents_to_neighbor = self._get_neighbors(empty_neighbor)
            neighboring_stones_in_group_count = 0
            for adjacent in adjacents_to_neighbor:
                if adjacent in group:
                    neighboring_stones_in_group_count += 1
            if neighboring_stones_in_group_count > 1:
                common_empty_neighbors.add(empty_neighbor)
        return common_empty_neighbors

    def _group_alive(self, group):
        #group is alive if it has two eyes
        return self._group_has_two_eyes(group)

    def _group_has_two_eyes(self, group):
        #an eye is an empty space surrounded by stones of one colour
        eyes = 0
        empty_neighbors = self._get_empty_neighbors_of_group(group)
        for neighbor in empty_neighbors:
            adjacents = self._get_neighbors(neighbor)
            if adjacents.issubset(group):
                eyes += 1
        return eyes == self.TWO_EYES

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

    def _samecolor_stone(self, first_stone, second_stone):
        return self.goban.at(first_stone) == self.goban.at(second_stone)

    def _oppositecolor_stone(self, first_stone, second_stone):
        return (not self.goban.is_empty(first_stone)) and self.goban.at(first_stone) != self.goban.at(second_stone)
