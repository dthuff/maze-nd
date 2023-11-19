import unittest
from maze_nd.draw import draw

class MyTestCase(unittest.TestCase):
    def test_draw_2d(self):
        # ARRANGE

        # ACT
        result = draw(maze=maze)
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
