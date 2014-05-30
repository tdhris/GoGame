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

    def test_get_ONE_opposite_color_neighbor(self):
        black_move1 = Position(0, 0)
        white_move1 = Position(0, 1)

        self.game.make_move(black_move1)
        self.game.make_move(white_move1)
        self.assertEqual({white_move1}, self.game._get_oppositecolor_neighbors(black_move1))

    def test_you_can_make_a_move_at_0_0(self):
        p = Position(0, 0)
        self.game.make_move(p)
        self.assertFalse(self.game.goban.is_empty(p))

    def test_get_all_OPPOSITE_color_neighbors_directly_adjacent_to_a_given_stone(self):
          # [[BLACK, WHITE, None],
          #  [WHITE, BLACK, None],
          #  [None, None, None]]

        black_move1 = Position(0, 0)
        white_move1 = Position(0, 1)
        black_move2 = Position(1, 1)
        white_move2 = Position(1, 0)

        self.game.make_move(black_move1)
        self.game.make_move(white_move1)
        self.game.make_move(black_move2)
        self.game.make_move(white_move2)
        self.game.make_move(black_move1)

        self.assertEqual({black_move1, black_move2}, self.game._get_oppositecolor_neighbors(white_move2))
        self.assertEqual({white_move1, white_move2}, self.game._get_oppositecolor_neighbors(black_move1))

    def test_get_SAMECOLOR_neighbors_directly_adjacent_to_a_given_stone(self):
        # [[BLACK, BLACK, None],
        #  [WHITE, BLACK, None],
        #  [WHITE, None, None]]
        black_move1 = Position(0, 0)
        white_move1 = Position(1, 0)
        black_move2 = Position(0, 1)
        white_move2 = Position(2, 0)
        black_move3 = Position(1, 1)

        self.game.make_move(black_move1)
        self.game.make_move(white_move1)
        self.game.make_move(black_move2)
        self.game.make_move(white_move2)
        self.game.make_move(black_move3)

        self.assertEqual({white_move2}, self.game._get_samecolor_neighbors(white_move1))
        self.assertEqual({black_move1, black_move3}, self.game._get_samecolor_neighbors(black_move2))

    def test_get_adjacent_opponent_group_by_given_stone(self):
        # [[None, None, None],
        #  [WHITE, WHITE, WHITE],
        #  [WHITE, None, None]]

        #useless black moves
        black_move1 = Position(10, 10)
        black_move2 = Position(12, 10)
        black_move3 = Position(12, 0)
        black_move4 = Position(12, 1)

        #important moves
        white_move1 = Position(1, 0)
        white_move2 = Position(1, 1)
        white_move3 = Position(1, 2)
        white_move4 = Position(2, 0)

        self.game.make_move(black_move1)
        self.game.make_move(white_move1)
        self.game.make_move(black_move2)
        self.game.make_move(white_move2)
        self.game.make_move(black_move3)
        self.game.make_move(white_move3)
        self.game.make_move(black_move4)
        self.game.make_move(white_move4)

        self.assertEqual({white_move1, white_move2, white_move3, white_move4}, self.game._get_group(white_move1))

    def test_get_ALL_opposite_color_adjacent_groups(self):
        # [[None, None, WHITE],
        #  [WHITE, BLACK, WHITE],
        #  [WHITE, None, None]]

        #important moves
        black_move1 = Position(1, 1)

        white_move1 = Position(1, 0)
        white_move2 = Position(2, 0)
        white_move3 = Position(0, 2)
        white_move4 = Position(1, 2)

        #not important
        black_move2 = Position(11, 11)
        black_move3 = Position(12, 12)
        black_move4 = Position(13, 13)

        self.game.make_move(black_move1)
        self.game.make_move(white_move1)
        self.game.make_move(black_move2)
        self.game.make_move(white_move2)
        self.game.make_move(black_move3)
        self.game.make_move(white_move3)
        self.game.make_move(black_move4)
        self.game.make_move(white_move4)

        self.assertTrue({white_move1, white_move2} in self.game._get_adjacent_opponent_groups(black_move1))
        self.assertTrue({white_move4, white_move3} in self.game._get_adjacent_opponent_groups(black_move1))


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

        #not important
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

    def test_stone_is_NOT_captured_when_adjacent_to_samecolor_stones_that_have_liberties_left(self):
        #     [[None, BLACK, None, None ...],
        #      [BLACK, WHITE, WHITE, None ...],
        #      [None, BLACK, BLACK, None], ...,
        #       ....]
        black_move1 = Position(0, 1)
        black_move2 = Position(1, 0)
        black_move3 = Position(2, 1)
        black_move4 = Position(2, 2)

        white_move1 = Position(1, 1)
        white_move2 = Position(1, 2)
        white_move3 = Position(1, 3)

        self.game.make_move(black_move1)
        self.game.make_move(white_move1)
        self.game.make_move(black_move2)
        self.game.make_move(white_move2)
        self.game.make_move(black_move3)
        self.game.make_move(white_move3)
        self.game.make_move(black_move4)

        self.assertTrue(self.game._has_at_least_one_liberty(white_move2))
        self.assertEqual(WHITE, self.game.goban.at(white_move2))
        self.assertEqual(WHITE, self.game.goban.at(white_move1))
        self.assertFalse(self.game.goban.is_empty(white_move1))

    def test_two_stones_are_removed_when_the_group_has_no_liberties_and_no_eyes(self):
        #     [[None, BLACK, BLACK, ...],
        #      [BLACK, WHITE, WHITE, ...],
        #      [None, BLACK, BLACK, ...,]
        #       ....]
        black_move1 = Position(0, 1)
        black_move2 = Position(1, 0)
        black_move3 = Position(2, 1)
        black_move4 = Position(0, 2)
        black_move5 = Position(2, 2)
        black_capturing_move = Position(1, 3)

        white_move1 = Position(1, 1)
        white_move2 = Position(1, 2)
        #useless moves
        white_move3 = Position(11, 11)
        white_move4 = Position(12, 12)
        white_move5 = Position(13, 13)

        self.game.make_move(black_move1)
        self.assertEqual(BLACK, self.game.goban.at(black_move1))
        self.game.make_move(white_move1)
        self.assertEqual(WHITE, self.game.goban.at(white_move1))
        self.game.make_move(black_move2)
        self.assertEqual(BLACK, self.game.goban.at(black_move2))
        self.game.make_move(white_move2)
        self.assertEqual(WHITE, self.game.goban.at(white_move2))
        self.game.make_move(black_move3)
        self.assertEqual(BLACK, self.game.goban.at(black_move3))
        self.game.make_move(white_move3)
        self.assertEqual(WHITE, self.game.goban.at(white_move3))
        self.game.make_move(black_move4)
        self.assertEqual(BLACK, self.game.goban.at(black_move4))
        self.game.make_move(white_move4)
        self.assertEqual(WHITE, self.game.goban.at(white_move4))
        self.game.make_move(black_move5)
        self.assertEqual(BLACK, self.game.goban.at(black_move5))
        self.game.make_move(white_move5)
        self.assertEqual(WHITE, self.game.goban.at(white_move5))
        self.game.make_move(black_capturing_move)

        self.assertEqual(BLACK, self.game.goban.at(black_capturing_move))
        self.assertTrue(self.game.goban.is_empty(white_move1))
        self.assertTrue(self.game.goban.is_empty(white_move2))
        self.assertEqual(self.game.opponent.captured_stones_count, 2)
        self.assertEqual({white_move1, white_move2}, self.game.opponent.captured_stones)

    def tearDown(self):
        self.game.goban.clear_board()

if __name__ == '__main__':
    unittest.main()
