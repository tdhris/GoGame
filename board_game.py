from board import Board
from goban import Goban
from itertools import cycle

class BoardGame:
    def __init__(self, players, size=Board.DEFAULT_BOARD_SIZE):
        self._board = Board(size)
        self._players = players
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
            self.check_outcome()
            self._change_turn()

    def is_move_valid(self, move):
        return self.board.is_iniside_board(move)

    def check_outcome(self):
        if self.board.is_board_full():
            self.end_game()

    def win_game(self):
        self._has_winner = True
        self.winner = self._current_player
        self.end_game()

    def end_game(self):
        self._running = False

    def _change_turn(self):
        self._current_player = self._get_next_player()

    def _get_next_player(self):
        return next(self._next_player)

    def _next_player(self):
        for player in cycle(self._players):
            yield player
    