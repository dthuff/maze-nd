import random

import cv2
import numpy as np

from maze_nd.draw import draw


class MazeND:
    """
    A maze data structure represented as a boolean grid where
        False = Passage
        True = Wall

        Credit for 2D implementation of Prim's Algorithm to Arne Stenkrona: https://github.com/ArneStenkrona/MazeFun
    """

    def __init__(self, shape: list[int], animate_generation: bool = False, save_image: bool = True,
                 theme: str = "default", wait_to_destroy_image: bool = False):
        self.grid = np.ones(_force_odd_dimension(shape), dtype=bool)
        self.generate(animate=animate_generation, save_image=save_image, theme=theme)
        if wait_to_destroy_image:
            cv2.waitKey(0)

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
            All neighbor cells
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

    def generate(self, animate: bool = False, save_image: bool = False, theme: str = "default"):
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
            if animate:
                draw(self, highlighted_cell=a_frontier_cell, theme=theme, expand_highlighted_cell=True)
            neighbors = self.get_neighbors(list(a_frontier_cell))
            if neighbors:
                a_neighbor_cell = random.choice(tuple(neighbors))
                self.connect(list(a_frontier_cell), list(a_neighbor_cell))
            frontier_of_frontier_cell = self.get_frontier(list(a_frontier_cell))
            for cell in frontier_of_frontier_cell:
                frontier.add(cell)

        self.connect(list(a_frontier_cell), list(a_neighbor_cell))
        image = draw(self, highlighted_cell=a_frontier_cell, theme=theme, expand_highlighted_cell=False)
        if save_image:
            cv2.imwrite("./maze_image.png", image)


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
