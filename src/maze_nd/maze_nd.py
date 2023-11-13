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

    def get_plane_indices(self):
        """
        Get a tuple of 2D plane indices spanning the maze. Used for drawing different plane_indices of the maze.
        E.g., for a 3D maze, return ((0, 1), (1, 2), (2, 0)).

        Returns
        -------
        plane_indices: tuple[tuple[int]]
            Tuple of dimension indices.
        """
        plane_indices = ()
        ndim = len(self.grid.shape)
        for i in range(ndim):
            plane_indices += (i, np.mod(i + 1, ndim)),
        return plane_indices

    def draw(self, passage_color: tuple[int, int, int] = (255, 255, 255),
             wall_color: tuple[int, int, int] = (0, 0, 0), highlighted_cell: tuple[int] = None,
             highlight_color: tuple[int, int, int] = (0, 255, 0)):
        """
        Draw the maze.

        Parameters
        ----------
        passage_color: tuple[int, int, int]
            BGR color tuple to use for passage cells
        wall_color: tuple[int, int, int]
            BGR color tuple to use for wall cells
        highlighted_cell: tuple[int]
            Coordinates of cell to highlight
        highlight_color: tuple[int, int, int]
            BGR color tuple to use for highlighted cell
        """
        ndim = len(self.grid.shape)

        border_img = Image.new('RGB', (1, max(self.grid.shape)), color=(255, 0, 0))
        montage_img = border_img
        for plane_indices in self.get_plane_indices():
            img: Image = self.get_img(plane_indices, passage_color, wall_color, highlighted_cell, highlight_color)
            img = cv2.copyMakeBorder(np.asarray(img), 0, max(self.grid.shape) - img.height, 0, 0,
                                     cv2.BORDER_CONSTANT, value=(128, 128, 128))
            montage_img = np.concatenate((montage_img, img, border_img), axis=1)

        # img_resized = cv2.resize(np.asarray(montage_img), (600 * ndim, 600), interpolation=cv2.INTER_NEAREST)
        img_resized = cv2.resize(np.asarray(montage_img),
                                 dsize=(self._scale * montage_img.shape[1], self._scale * montage_img.shape[0]),
                                 interpolation=cv2.INTER_NEAREST)

        cv2.imshow('maze', img_resized)
        cv2.waitKey(1)

    # noinspection PyUnresolvedReferences
    def get_img(self, plane_indices: tuple[int, int] = (0, 1), passage_color: tuple[int, int, int] = (0, 0, 0),
                wall_color: tuple[int, int, int] = (255, 255, 255),
                highlighted_cell: tuple[int] = None,
                highlight_color: tuple[int, int, int] = (0, 255, 0)) -> Image:
        """
        Returns an Image representation of the maze at this point in generation.

        Parameters
        ----------
        plane_indices: tuple[int, int]
            A 2-tuple of dimension indices to draw
        passage_color: tuple[int, int, int]
            BGR color tuple to use for passage cells
        wall_color: tuple[int, int, int]
            BGR color tuple to use for wall cells
        highlighted_cell: tuple[int]
            Coordinates of cell to highlight
        highlight_color: tuple[int, int, int]
            BGR color tuple to use for highlighted cell
        Returns
        -------
        im: PIL.Image.
            Image representation of the maze
        """
        im = Image.new('RGB', (self.grid.shape[plane_indices[0]], self.grid.shape[plane_indices[1]]))
        pixels: PyAccess = im.load()
        self.get_plane(plane_indices=plane_indices, highlighted_cell=highlighted_cell)
        for x in range(self.grid.shape[plane_indices[0]]):
            for y in range(self.grid.shape[plane_indices[1]]):
                if self.plane[x, y]:
                    pixels[x, y] = passage_color
                else:
                    pixels[x, y] = wall_color
        if highlighted_cell is not None:
            pixels[highlighted_cell[plane_indices[0]], highlighted_cell[plane_indices[1]]] = highlight_color
        return im

    def get_plane(self, plane_indices: tuple[int, int], highlighted_cell: tuple[int]):
        ndim = len(self.grid.shape)
        dims_to_remove = set(range(ndim)).difference(set(plane_indices))
        dims_to_remove = sorted(dims_to_remove, reverse=True)
        self.plane = self.grid
        for dim in dims_to_remove:
            self.plane = self.plane.take(indices=highlighted_cell[dim], axis=dim)
        # Dumb hack to reverse axis order for final plane when plane_indices are (ndim, 0)
        if plane_indices[1] < plane_indices[0]:
            self.plane = np.transpose(self.plane)


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
