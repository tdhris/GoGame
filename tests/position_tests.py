import sys
sys.path.append("..")

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

    def test_you_can_change_coordinates_from_the_change_position_method(self):
        point = Position()
        point.change_position(100, 100)
        self.assertEqual(100, point.x)
        self.assertEqual(100, point.y)

    def test_equality(self):
        point_a = Position(0, 0)
        point_b = Position(0, 0)
        self.assertEqual(point_b, point_a)

    def test_unequality(self):
        point_a = Position(0, 0)
        point_b = Position(0, 1)
        self.assertNotEqual(point_b, point_a)

    def test_representation(self):
        point_a = Position(13, 13)
        self.assertEqual("(13, 13)", str(point_a))


if __name__ == '__main__':
    unittest.main()
