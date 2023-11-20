import unittest

from maze_nd.maze_nd import MazeND


class MazeNDTestCase(unittest.TestCase):
    def test_create_2d_maze(self):
        # ARRANGE
        maze_shape = [60, 40]
        expected_result = (59, 39)

        # ACT
        maze = MazeND(maze_shape)

        # ASSERT
        self.assertEqual(maze.grid.shape, expected_result)

    def test_create_3d_maze(self):
        # ARRANGE
        maze_shape = [10, 10, 10]
        expected_result = (9, 9, 9)

        # ACT
        maze = MazeND(maze_shape)

        # ASSERT
        self.assertEqual(maze.grid.shape, expected_result)

    def test_create_4d_maze(self):
        # ARRANGE
        maze_shape = [10, 10, 10, 20]
        expected_result = (9, 9, 9, 19)

        # ACT
        maze = MazeND(maze_shape)

        # ASSERT
        self.assertEqual(maze.grid.shape, expected_result)

    def test_animation(self):
        # ARRANGE
        maze_shape = [11, 11]
        expected_result = (11, 11)
        # ACT
        maze = MazeND(maze_shape, animate_generation=True)

        self.assertEqual(maze.grid.shape, expected_result)


if __name__ == '__main__':
    unittest.main()
