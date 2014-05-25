import unittest
from board import Board
from position import Position


class BoardGameBasicFunctionalityTests(unittest.TestCase):
    def test_board_of_size_three(self):
        test_size = 3
        board = Board(test_size)
        self.assertEqual(test_size, board.size)


    def test_board_of_size_100(self):
        test_size = 100
        board = Board(100)
        self.assertEqual(test_size, board.size)


    def test_board_negative_size(self):
        negative_size = -10
        self.assertRaises(Board(negative_size))


    def test_is_board_empty(self):
        board = Board()
        self.assertTrue(board.is_board_empty())


    def test_at_function_when_square_is_empty(self):
        board = Board(3)
        p = Position(2, 2)
        self.assertEqual(board.EMPTY_FIELD, board.at(p))

    def test_at_function_when_position_is_invalid(self):
        board = Board()
        p = Position(10, 10)
        self.assertRaises(board.at(p))


    def test_is_squere_empty_function_when_square_is_empty(self):
        board = Board(3)
        p = Position()
        self.assertTrue(board.is_empty(p))


    def test_place_function(self):
        board = Board(3)
        p = Position(2, 2)
        symbol = "X"
        board.place(p, symbol)
        self.assertEqual(symbol, board.at(p))


    def test_place_function_when_position_is_invalid(self):
        board = Board(3)
        p = Position(10, 10)
        symbol = "X"
        self.assertRaises(board.place(p, symbol))


    def test_is_suqre_empty_function_when_square_is_NOT_empty(self):
        board = Board()
        p = Position()
        symbol = "X"
        board.place(p, symbol)
        self.assertFalse(board.is_empty(p))


    def test_at_function_when_square_is_NOT_empty(self):
        board = Board()
        p = Position(2, 2)
        symbol = "X"
        board.place(p, symbol)
        self.assertEqual(symbol, board.at(p))


    def test_remove_when_square_is_not_empty(self):
        board = Board()
        p = Position(2, 2)
        symbol = "X"
        board.place(p, symbol)
        self.assertEqual(symbol, board.at(p))
        board.remove(p)
        self.assertTrue(board.is_empty(p))


class BoardGameCountingTests(unittest.TestCase):
    def test_count_empty_fields_when_all_fields_are_empty(self):
        size = 3
        board = Board(size)
        self.assertEqual(size ** 2, board.count_empty_fields())

    def test_count_empty_fields_when_one_field_is_not_empty(self):
        size = 3
        b = Board(size)
        p = Position()
        b.place(p, "X")
        self.assertEqual((size ** 2) - 1, b.count_empty_fields())

    def test_count_empty_fields_when_just_one_field_is_empty(self):
        size = 3
        b = Board(size)
        for i in range(size):
            for j in range(size):
                p = Position(i, j)
                b.place(p, "X")
        p = Position()
        b.remove(p)
        self.assertEqual(1, b.count_empty_fields())

    def test_count_empty_fields_when_there_are_no_empty_fields(self):
        size = 3
        b = Board(size)
        for i in range(size):
            for j in range(size):
                p = Position(i, j)
                b.place(p, "X")
        self.assertEqual(0, b.count_empty_fields())

    def test_count_taken_fields_when_there_are_no_empty_fields(self):
        size = 3
        b = Board(size)
        for i in range(size):
            for j in range(size):
                p = Position(i, j)
                b.place(p, "X")
        self.assertEqual(size ** 2, b.count_taken_fields())


if __name__ == '__main__':
    unittest.main()