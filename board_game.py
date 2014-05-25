from board import Board
from itertools import cycle
from copy import copy


"""
BoardGame Class

When creating instances of BoardGame(), a list of players should always be provided as a parameter.
When creating a subclass of BoardGame, BoardGame.__init__ method should always be called with the 'players' parameter.

Attributes:
* board
        An object of the Board class

* running
        Returns true if the game is still in progress.

* current_player
        Returns the player whose turn it is in the game.

* player_count
        Returns the number of players in the game.

Functionality:


"""


class BoardGame:
    def __init__(self, players, size=Board.DEFAULT_BOARD_SIZE):
        self._board = Board(size)
        self._players = copy(players)
        self._next_player = self._next_player()
        self._current_player = self._get_next_player()
        self._running = True
        self._has_winner = False
    
    @property
    def board(self):
        return self._board

    @property
    def running(self):
        return self._running

    @property
    def current_player(self):
        return self._current_player

    @property
    def player_count(self):
        return len(self._players)

    @property
    def players(self):
        return self._players    

    @property
    def has_winner(self):
        return self._has_winner

    def make_move(self, move):
        if self.running and self.is_move_valid(move):
            self.board.place(move, self.current_player)
            self._check_board_full()
            self._change_turn()

    def is_move_valid(self, move):
        return self.board.is_iniside_board(move)

    def win_game(self):
        self._has_winner = True
        self.winner = self._current_player
        self.end_game()

    def resign(self):
        resigning_player = self._current_player
        self._change_turn()
        self._players.remove(resigning_player)
        self._check_at_least_two_players()

    def end_game(self):
        self._running = False

    def _check_board_full(self):
        if self.board.is_board_full():
            self.end_game()

    def _check_at_least_two_players(self):
        if self.player_count == 1:
            self.win_game()

    def _change_turn(self):
        self._current_player = self._get_next_player()

    def _get_next_player(self):
        return next(self._next_player)

    def _next_player(self):
        for player in cycle(self._players):
            yield player
    