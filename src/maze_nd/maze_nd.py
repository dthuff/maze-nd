import random
import time

import cv2
import numpy as np
from PIL import Image, PyAccess


# Credit for initial 2D implementation of Prim's Algorithm to Arne Stenkrona
# https://github.com/ArneStenkrona/MazeFun
# Their implementation made the N-D implementation much easier! <3


class MazeND:
    """
    A maze data structure, represented as a boolean grid where
        False = Passage - where the player can move
        True = Wall
    """

    def __init__(self, shape: list[int], animate_generation: bool = False, scale: int = 16, frame_time: float = 0.1):
        self.grid = np.ones(_force_odd_dimension(shape), dtype=bool)
        self.plane = None
        self.animate_generation = animate_generation
        self._scale = scale  # Pixel scale of maze image. Used if animate_generation is True.
        self._frame_time = frame_time  # time for 1 frame, in sec. Used if animate_generation is True.
        self.generate()

    def get_frontier(self, seed_pt: list) -> set:
        """
        Returns the frontier of cell seed_pt. Frontier is all walls exactly 2 cells away from seed_pt

        Parameters
        ----------
        seed_pt: list
            Coordinates of current cell

        Returns
        -------
        frontier: set[list]
            Set of all frontier cells
        """
        frontier = set()
        if self.inside_maze(seed_pt):
            for dim_index, element in enumerate(seed_pt):
                left_neighbor_ind = seed_pt.copy()
                left_neighbor_ind[dim_index] = seed_pt[dim_index] - 2
                right_neighbor_ind = seed_pt.copy()
                right_neighbor_ind[dim_index] = seed_pt[dim_index] + 2
                if element > 1 and self.grid[tuple(left_neighbor_ind)]:
                    frontier.add(tuple(left_neighbor_ind))
                if element + 2 < self.grid.shape[dim_index] and self.grid[tuple(right_neighbor_ind)]:
                    frontier.add(tuple(right_neighbor_ind))
        return frontier

    def inside_maze(self, seed_pt) -> bool:
        """
        Check that a seed point is within the maze grid.
        """
        for dim_idx, element in enumerate(seed_pt):
            if not 0 <= element < self.grid.shape[dim_idx]:
                return False
            return True

    def get_neighbors(self, seed_pt: list) -> set:
        """
        Returns the neighbors of cell. The neighbors of a cell are all passages exactly 2 cells away from seed_pt
        Parameters
        ----------
        seed_pt: list
            Coordinates of current cell

        Returns
        -------
        neighbors: set
            Set of all neighbor cells
        """
        neighbors = set()
        if self.inside_maze(seed_pt):
            for dim_index, element in enumerate(seed_pt):
                left_neighbor_ind = seed_pt.copy()
                left_neighbor_ind[dim_index] = seed_pt[dim_index] - 2
                right_neighbor_ind = seed_pt.copy()
                right_neighbor_ind[dim_index] = seed_pt[dim_index] + 2
                if element > 1 and not self.grid[tuple(left_neighbor_ind)]:
                    neighbors.add(tuple(left_neighbor_ind))
                if element + 2 < self.grid.shape[dim_index] and not self.grid[tuple(right_neighbor_ind)]:
                    neighbors.add(tuple(right_neighbor_ind))
        return neighbors

    def connect(self, pt1: list, pt2: list):
        """
        Connects two cells pt1 and pt2 with a passage.

        Parameters
        ----------
        pt1: list
            Coordinates of 1st cell
        pt2: list
            Coordinates of 2nd cell
        """
        pt_between = pt1.copy()
        for dim_index, element in enumerate(zip(pt1, pt2)):
            if pt1[dim_index] - pt2[dim_index]:
                pt_between[dim_index] = (pt1[dim_index] + pt2[dim_index]) // 2
        self.grid[tuple(pt_between)] = False
        self.grid[tuple(pt1)] = False

    def generate(self):
        """
        Generates a maze using Prim's algorithm
            Pseudo code:
            1. All points are assumed to be walls
            2. Pick the seed_pt (1, 1, 1, ...) and set it to be a passage
            3. Initialize the set frontier that contains all frontier points of seed_pt
            4. while frontier is not empty:
                4a. Pick a random frontier cell from frontier
                4b. Remove that cell from the frontier
                4c. Get neighbors of a_frontier_cell
                4d. Connect a_frontier_cell with a random neighbor from neighbors
                4e. Add the frontier of a_frontier_cell to frontier
        Returns
        -------

        """
        ind = 1
        for i in range(1, self.grid.ndim):
            ind += np.prod(self.grid.shape[i:])
        np.put(self.grid, ind, False)
        seed_pt = np.unravel_index(ind, self.grid.shape)
        frontier = self.get_frontier(list(seed_pt))
        while frontier:
            a_frontier_cell = random.choice(tuple(frontier))
            frontier.remove(a_frontier_cell)
            if self.animate_generation:
                self.draw(highlighted_cell=a_frontier_cell)
                time.sleep(self._frame_time)
            neighbors = self.get_neighbors(list(a_frontier_cell))
            if neighbors:
                a_neighbor_cell = random.choice(tuple(neighbors))
                self.connect(list(a_frontier_cell), list(a_neighbor_cell))
            frontier_of_frontier_cell = self.get_frontier(list(a_frontier_cell))
            for cell in frontier_of_frontier_cell:
                frontier.add(cell)

    def draw(self, passage_color=(255, 255, 255), wall_color=(0, 0, 0), highlighted_cell: tuple = None,
             highlight_color=(0, 255, 0), wait_key=1):
        """
        Draws an image of the maze with cv2.imshow()
        :param passage_color: colour of the passages
        :param wall_color: colour of the walls
        :param highlighted_cell: desired cell to highlight
        :param highlight_color: colour of highlight
        :param wait_key: argument to pass to cv2.waitKey()
        """
        img: Image = self.get_img(passage_color, wall_color, highlighted_cell, highlight_color)
        img_resized = cv2.resize(np.asarray(img),
                                 (600, 600),
                                 interpolation=cv2.INTER_NEAREST)
        cv2.imshow('maze', img_resized)
        cv2.waitKey(wait_key)

    # noinspection PyUnresolvedReferences
    def get_img(self, passage_color=(0, 0, 0), wall_color=(255, 255, 255), highlighted_cell: tuple = None,
                highlight_color=(0, 255, 0)) -> Image:
        """
        Fetches an image representation of the maze
        :param passage_color: colour of the passages
        :param wall_color: colour of the walls
        :param highlighted_cell: desired cell to highlight
        :param highlight_color: colour of highlight
        :return: image of the maze
        """
        im = Image.new('RGB', (self.grid.shape[0], self.grid.shape[1]))
        pixels: PyAccess = im.load()
        for x in range(self.grid.shape[0]):
            for y in range(self.grid.shape[1]):
                if self.grid[x, y]:
                    pixels[x, y] = passage_color
                else:
                    pixels[x, y] = wall_color
        if highlighted_cell is not None:
            pixels[highlighted_cell] = highlight_color
        return im


def _force_odd_dimension(shape: list[int]) -> list[int]:
    """
    Force maze dimensions to be odd, to ensure solid border.
    Parameters
    ----------
    shape: list[int]
        The shape of the maze.
    Returns
    -------
    shae: list[int]
        The shape of the maze, with any even dimensions reduced by 1, so that they are odd.
    """
    for idx, dim in enumerate(shape):
        if not np.mod(dim, 2):
            shape[idx] = dim - 1
    return shape
