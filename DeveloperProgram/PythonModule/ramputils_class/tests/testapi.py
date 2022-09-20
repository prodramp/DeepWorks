import unittest
from src.ramputils import calc


class RampUtilsTest(unittest.TestCase):
    def test(self):
        self.assertEqual(calc('addition', 1, 2, 3, 5)[1], 11)
        self.assertEqual(calc('subtraction', 30, 5)[1], 25)
        self.assertEqual(calc('multiplication', 1, 2, 3, 5)[1], 30)
        self.assertEqual(calc('division', 2, 5)[1], 0.4)


if __name__ == '__main__':
    test_obj = RampUtilsTest()
    test_obj.test()


