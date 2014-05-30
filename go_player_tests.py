from go_player import GoPlayer
from position import Position
import unittest


class GoPlayerBoardPlayerTests(unittest.TestCase):
    def setUp(self):
        self.black = "B"
        self.player = GoPlayer(self.black)

    def test_player_symbol_is_the_one_provided(self):
        self.assertEqual(self.black, self.player.symbol)

    def test_player_keeps_track_of_his_own_moves(self):
        p1 = Position(0, 0)
        self.player.make_move(p1)
        p2 = Position(3, 4)
        self.player.make_move(p2)
        p3 = Position(5, 7)
        self.player.make_move(p3)
        self.assertEqual([p1, p2, p3], self.player.stones)

    def test_player_removes_move_from_record_when_move_is_in_record(self):
        p1 = Position(0, 0)
        self.player.make_move(p1)
        p2 = Position(3, 4)
        self.player.make_move(p2)
        p3 = Position(5, 7)
        self.player.make_move(p3)
        self.assertEqual([p1, p2, p3], self.player.stones)
        self.player.remove_move(p2)
        self.assertEqual([p1, p3], self.player.stones)

    def test_player_DOES_NOT_remove_move_from_record_when_move_is_NOT_in_record(self):
        p1 = Position(0, 0)
        self.player.make_move(p1)
        p2 = Position(3, 4)
        self.assertEqual([p1], self.player.stones)
        self.player.remove_move(p2)
        self.assertEqual([p1], self.player.stones)


class GoPlayerTests(unittest.TestCase):
    def setUp(self):
        self.black = "B"
        self.player = GoPlayer("B")

    def test_player_captures_a_stone(self):
        self.assertEqual(0, self.player.captured_stones)
        stone = Position(1, 1)
        self.player.capture_stones(stone)
        self.assertEqual(1, self.player.captured_stones)

    def test_player_captures_multiple_stones(self):
        stones = []
        n = 10
        for i in range(n):
            stone = Position(i, i)
            stones.append(stone)
        self.player.capture_stones(*stones)
        self.assertEqual(n, self.player.captured_stones)

    def test_correctly_returns_last_move_when_it_is_the_only_move(self):
        stone = Position(0, 0)
        self.player.make_move(stone)
        self.assertEqual(stone, self.player.last_move())

    def test_correctlt_returns_last_move_when_there_are_several(self):
        n = 10
        for i in range(n):
            stone = Position(i, i)
            self.player.make_move(stone)
        last = Position(n - 1, n - 1)
        self.assertEqual(last, self.player.last_move())


if __name__ == '__main__':
    unittest.main()
