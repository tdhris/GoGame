from go_game import GoGame
from position import Position
import unittest

DEFAULT_GOBAN_SIZE = 19
BLACK = "B"
WHITE = "W"


class GoGameBasicFunctionalityTests(unittest.TestCase):
    def setUp(self):
        self.game = GoGame()

    def test_go_game_has_a_goban_of_size_DEFAULT_GOBAN_SIZE(self):
        self.assertEqual(DEFAULT_GOBAN_SIZE, self.game.goban.size)

    def test_komi_is_6_5_by_default(self):
        self.assertEqual(6.5, self.game.komi)

    def test_you_can_create_go_game_with_a_goban_of_size_THIRTEEN_and_NINE(self):
        go = GoGame(13)
        self.assertEqual(13, go.goban.size)

        joseki = GoGame(9)
        self.assertEqual(9, joseki.goban.size)

    def test_first_current_player_is_BLACK(self):
        self.assertEqual(BLACK, self.game.current_player.symbol)

    def test_first_opponent_is_WHITE(self):
        self.assertEqual(WHITE, self.game.opponent.symbol)

    def test_game_changes_turns_automatically_when_players_make_valid_moves(self):
        g = GoGame()
        for i in range(DEFAULT_GOBAN_SIZE):
            if i % 2 == 0:
                self.assertEqual(BLACK, g.current_player.symbol)
            else:
                self.assertEqual(WHITE, g.current_player.symbol)
            p = Position(i, i)
            g.make_move(p)

    def test_stone_is_captured_when_it_has_no_liberties_left(self):
        #     [[None, BLACK, None, ...],
        #      [BLACK, WHITE, None, ...],
        #      [None, BLACK, None], ...,
        #       ....]
        black_move1 = Position(0, 1)
        black_move2 = Position(1, 0)
        black_move3 = Position(2, 1)
        black_move4 = Position(1, 2)

        white_move1 = Position(1, 1)
        white_move2 = Position(10, 10)
        white_move3 = Position(11, 11)

        self.game.make_move(black_move1)
        self.game.make_move(white_move1)
        self.game.make_move(black_move2)
        self.game.make_move(white_move2)
        self.game.make_move(black_move3)
        self.game.make_move(white_move3)
        self.game.make_move(black_move4)

        self.assertFalse(self.game._has_at_least_one_liberty(white_move1))
        self.assertEqual(BLACK, self.game.goban.at(black_move4))
        self.assertTrue(self.game.goban.is_empty(white_move1))

    def tearDown(self):
        self.game.goban.clear_board()

if __name__ == '__main__':
    unittest.main()
