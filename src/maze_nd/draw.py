import random

import cv2
import numpy as np
from PIL import Image, PyAccess

from maze_nd.colors import get_color_dictionary


def draw(maze, highlighted_cell: tuple[int, int, int], theme: str, expand_highlighted_cell: bool = True,
         frame_time_ms: int = 40, draw_scale: int = 16) -> Image:
    """
    Draw the maze.

    Parameters
    ----------
    maze: mazeND
        The maze object to draw
    highlighted_cell: tuple[int]
        Coordinates of cell to highlight
    theme: str
        Maze color theme
    expand_highlighted_cell: bool
        True during animation, false at end to ID goal cell.
    frame_time_ms: int
        Time to wait on each frame of generation in milliseconds.
    draw_scale: int
        Pixel scale of maze image.

    Returns
    -------
    img_resized : Image
        The maze image.
    """
    color_dict = get_color_dictionary(theme)
    border_height = _get_border_height(maze.grid.shape)
    border_img = Image.new('RGB', (1, border_height), color=color_dict["border"])
    montage_img = border_img
    for plane_indices in get_plane_indices(maze):
        img: Image = get_img(maze, plane_indices, highlighted_cell, color_dict, expand_highlighted_cell)
        img = cv2.copyMakeBorder(np.asarray(img), 0, border_height - img.height, 0, 0,
                                 cv2.BORDER_CONSTANT, value=(128, 128, 128))
        montage_img = np.concatenate((montage_img, img, border_img), axis=1)

    img_resized = cv2.resize(np.asarray(montage_img),
                             dsize=(draw_scale * montage_img.shape[1], draw_scale * montage_img.shape[0]),
                             interpolation=cv2.INTER_NEAREST)

    cv2.imshow('maze', img_resized)
    frame_time_this_frame = int(frame_time_ms + 700 * np.exp(-0.04 * np.sum(np.logical_not(maze.grid))))
    cv2.waitKey(frame_time_this_frame)
    return img_resized


def get_img(maze, plane_indices: tuple[int, int], highlighted_cell: tuple[int, ...], color_dict: dict,
            expand_highlighted_cell: bool) -> Image:
    """
    Returns an Image representation of the maze at this point in generation.

    Parameters
    ----------
    maze: MazeND
        The maze object
    plane_indices: tuple[int, int]
        A 2-tuple of dimension indices to draw
    highlighted_cell: tuple[int]
        Coordinates of cell to highlight
    color_dict: dict
        Maze color dictionary.
    expand_highlighted_cell: bool
        True during animation, false at end to ID goal cell.
    Returns
    -------
    im: PIL.Image.
        Image representation of the maze
    """
    im = Image.new('RGB', (maze.grid.shape[plane_indices[0]], maze.grid.shape[plane_indices[1]]))
    pixels: PyAccess = im.load()
    plane = get_plane(maze, plane_indices=plane_indices, highlighted_cell=highlighted_cell)
    for x in range(maze.grid.shape[plane_indices[0]]):
        for y in range(maze.grid.shape[plane_indices[1]]):
            if plane[x, y]:
                pixels[x, y] = color_dict["wall"]
            else:
                pixels[x, y] = color_dict["passage"]
    if highlighted_cell is not None:
        hci = [highlighted_cell[plane_indices[0]], highlighted_cell[plane_indices[1]]]
        if isinstance(color_dict["highlight"], list):
            a_highlight_color = random.choice(color_dict["highlight"])
            if expand_highlighted_cell:
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        pixels[hci[0] + i, hci[1] + j] = a_highlight_color
            else:
                pixels[hci[0], hci[1]] = a_highlight_color
        else:
            if expand_highlighted_cell:
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        pixels[hci[0] + i, hci[1] + j] = color_dict["highlight"]
            else:
                pixels[hci[0], hci[1]] = color_dict["highlight"]

    return im


def get_plane(maze, plane_indices: tuple[int, int], highlighted_cell: tuple[int, ...]) -> np.ndarray:
    """
    Get a 2D plane of the maze for drawing.

    Parameters
    ----------
    maze : MazeND
        The maze object
    plane_indices: tuple[int, int]
        The two dimension indices of the plane to construct
    highlighted_cell : tuple[int, ...]
        The maze coordinates of the highlighted cell.

    Returns
    -------
    plane: np.ndarray
        A 2D array representing the plane of the maze along plane_indices and passing through highlighted_cell.
    """
    ndim = len(maze.grid.shape)
    dims_to_remove = set(range(ndim)).difference(set(plane_indices))
    plane = maze.grid
    for dim in sorted(dims_to_remove, reverse=True):
        plane = plane.take(indices=highlighted_cell[dim], axis=dim)
    return plane


def _get_border_height(shape: tuple) -> int:
    if len(shape) == 2:
        border_height = shape[1]
    else:
        border_height = max(shape)
    return border_height


def get_plane_indices(maze) -> tuple:
    """
    Get a tuple of 2D plane indices spanning the maze. Used for drawing different plane_indices of the maze.
    E.g., for a 3D maze, return ((0, 1), (1, 2)).

    Parameters
    ----------
    maze : MazeND
        The maze object

    Returns
    -------
    plane_indices: tuple[tuple[int]]
        Tuple of dimension indices.
    """
    plane_indices = ()
    ndim = len(maze.grid.shape)
    for i in range(ndim - 1):
        plane_indices += (i, np.mod(i + 1, ndim)),
    return plane_indices
