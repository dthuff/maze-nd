import unittest
import numpy as np
from maze_nd.maze_nd import MazeND


class MazeNDTestCase(unittest.TestCase):
    def test_create_2d_maze(self):
        # ARRANGE
        maze_shape = [10, 10]
        expected_result = (11, 11)

        # ACT
        maze = MazeND(maze_shape)

        # ASSERT
        self.assertEqual(maze.grid.shape, expected_result)

    def test_create_3d_maze(self):
        # ARRANGE
        maze_shape = [10, 10, 10]
        expected_result = (11, 11, 11)

        # ACT
        maze = MazeND(maze_shape)

        # ASSERT
        self.assertEqual(maze.grid.shape, expected_result)

    def test_create_4d_maze(self):
        # ARRANGE
        maze_shape = [10, 10, 10, 20]
        expected_result = (11, 11, 11, 21)

        # ACT
        maze = MazeND(maze_shape)

        # ASSERT
        self.assertEqual(maze.grid.shape, expected_result)


if __name__ == '__main__':
    unittest.main()
