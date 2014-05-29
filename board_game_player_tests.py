from board_game_player import BoardGamePlayer
from position import Position
import unittest


class BoardPlayerTests(unittest.TestCase):
    def setUp(self):
        self.symbol = "X"
        self.player = BoardGamePlayer(self.symbol)

    def test_player_symbol_is_the_one_provided(self):
        self.assertEqual(self.symbol, self.player.symbol)

    def test_player_keeps_track_of_his_own_moves(self):
        p1 = Position(0, 0)
        self.player.make_move(p1)
        p2 = Position(3, 4)
        self.player.make_move(p2)
        p3 = Position(5, 7)
        self.player.make_move(p3)
        self.assertEqual([p1, p2, p3], self.player.moves)

    def test_player_removes_move_from_record_when_move_is_in_record(self):
        p1 = Position(0, 0)
        self.player.make_move(p1)
        p2 = Position(3, 4)
        self.player.make_move(p2)
        p3 = Position(5, 7)
        self.player.make_move(p3)
        self.assertEqual([p1, p2, p3], self.player.moves)
        self.player.remove_move(p2)
        self.assertEqual([p1, p3], self.player.moves)

    def test_player_DOES_NOT_remove_move_from_record_when_move_is_NOT_in_record(self):
        p1 = Position(0, 0)
        self.player.make_move(p1)
        p2 = Position(3, 4)
        self.assertEqual([p1], self.player.moves)
        self.player.remove_move(p2)
        self.assertEqual([p1], self.player.moves)


if __name__ == '__main__':
    unittest.main()
