from board_game import BoardGame
from position import Position
import unittest


class BoardGameBasicFunctionalityTests(unittest.TestCase):
    def setUp(self):
        self.players = ["X", "O"]
        self.board_size = len(self.players)
        self.game = BoardGame(self.players, self.board_size)

    def test_board_game_has_a_board_of_a_given_size(self):
        self.assertEqual(self.board_size, self.game.board.size)

    def test_game_running_at_the_beginning_of_the_game(self):
        self.assertTrue(self.game.running)

    def test_game_stops_if_board_is_full(self):
        size_of_board_with_one_field = 1
        game = BoardGame(self.players, size_of_board_with_one_field)
        p = Position(0, 0)
        game.make_move(p)
        self.assertFalse(game.running)

    def test_board_remains_empty_if_move_is_invalid(self):
        size_of_board_with_one_field = 1
        g = BoardGame(self.players, size_of_board_with_one_field)
        p = Position(5, 5)
        g.make_move(p)
        self.assertTrue(g.board.is_board_empty())

    def test_game_stops_if_game_is_won(self):
        self.game.win_game()
        self.assertFalse(self.game.running)

    def test_game_has_winner_when_game_is_won(self):
        self.game.win_game()
        self.assertFalse(self.game.running)
        self.assertTrue(self.game.has_winner)

    def test_first_current_player_is_the_first_player_in_list_of_players(self):
        self.assertEqual(self.players[0], self.game.current_player)

    def test_game_changes_turns_automatically_when_players_make_valid_moves(self):
        players = ["X", "Y", "O", "Z"]
        g = BoardGame(players, len(players))
        for i in range(len(players)):
            self.assertEqual(players[i], g.current_player)
            p = Position(i, i)
            g.make_move(p)

    def test_game_does_not_change_turns_automatically_when_players_make_invalid_moves(self):
        p = Position(len(self.players) + 10)
        self.assertEqual(self.players[0], self.game.current_player)
        self.game.make_move(p)
        self.assertEqual(self.players[0], self.game.current_player)

    def tearDown(self):
        self.game.board.clear_board()

if __name__ == '__main__':
    unittest.main()