from position import Position
import unittest


class PositionBasicTests(unittest.TestCase):
    def test_basic_x_is_zero_and_y_is_zero_functionality(self):
        point = Position()
        self.assertEqual(0, point.x)
        self.assertEqual(0, point.y)

    def test_position_with_negative_coords(self):
        point = Position(-10, -10)
        self.assertEqual(-10, point.x)
        self.assertEqual(-10, point.y)

    def test_you_cannot_change_coordinates_manually(self):
        point = Position()
        point.x = 10
        self.assertEqual(0, point.x)

    def test_you_can_change_coordinates_from_the_change_position_method(self):
        point = Position()
        point.change_position(100, 100)
        self.assertEqual(100, point.x)
        self.assertEqual(100, point.y)


if __name__ == '__main__':
    unittest.main()