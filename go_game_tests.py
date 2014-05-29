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

    def test_game_changes_turns_automatically_when_players_make_valid_moves(self):
        g = GoGame()
        for i in range(DEFAULT_GOBAN_SIZE):
            if i % 2 == 0:
                self.assertEqual(BLACK, g.current_player.symbol)
            else:
                self.assertEqual(WHITE, g.current_player.symbol)
            p = Position(i, i)
            g.make_move(p)

    def tearDown(self):
        self.game.goban.clear_board()

if __name__ == '__main__':
    unittest.main()
