![A woodsy maze](https://github.com/dthuff/maze-nd/blob/master/examples/maze_kaboom_100_30.png)

# maze-nd

A python package for generating n-dimensional mazes via [randomized Prim's Algorithm](https://en.wikipedia.org/wiki/Maze_generation_algorithm)

Initial implementation in 2D from: https://github.com/ArneStenkrona/MazeFun

# Getting Started

## Prerequisites
Poetry: https://python-poetry.org/docs/#installation

## Installation

### Clone the repository: 

    git clone https://github.com/dthuff/maze-nd

### and install dependencies:

    cd maze-nd/
    poetry install

### Or, install via pip:

    pip install maze-nd

# Usage
## Generating maze structures
The MazeND class defines a maze data structure represented by a boolean array of arbitrary shape `maze.grid`.

A 2D maze of 40 rows and 40 columns can be generated with:

    from maze_nd.maze_nd import MazeND
    maze = MazeND([40, 40])

Note that maze dimensions must be odd to ensure a solid outer border. If even shape args are passed, they will be forced to be odd.

    maze = MazeND([40, 40])

    >>> maze.grid.shape
    (39, 39)

A 3D maze of 40 rows, 40 columns, and 20 slices can be generated with:

    maze = MazeND([40, 40, 20])

A 7D maze:

    maze = MazeND([20, 20, 20, 10, 10, 20, 5])

_**Caution**_: generation time is proportional to `np.prod(maze.grid.shape)`. This can quickly blow up for mazes with more than 4 dimensions.


## Visualizing maze structures

The maze generation process can be visualized using `examples/draw_maze.py`:

    poetry run python draw_maze.py 40 40

By default, this will save an image of the maze at `examples/maze_image.png`

Any number of shape dimensions can be passed. A 3D maze can be generated via:

    poetry run python draw_maze.py 20 20 20

For mazes with dimension N > 2, 2D planes of the maze will be drawn separated by a vertical border. For an N-D maze, N-1 planes are shown.


The animation can be turned off using `--skip-animation`:

    poetry run python draw_maze.py 40 40 --skip-animation

Fun color themes can be applied via `--theme`:

    poetry run python draw_maze.py --theme beachy 40 40

Available themes are: 
`default`
![A boring, default maze](https://github.com/dthuff/maze-nd/blob/master/examples/maze_default_90_40.png)

`beachy`, 
![A beachy maze](https://github.com/dthuff/maze-nd/blob/master/examples/maze_beachy_90_40.png)

`woodsy`, 
![A woodsy maze](https://github.com/dthuff/maze-nd/blob/master/examples/maze_woodsy_90_40.png)

`christmas`, 
![A festive, christmas maze](https://github.com/dthuff/maze-nd/blob/master/examples/maze_christmas_90_40.png)

and `kaboom`.
![An explosive, kaboom maze](https://github.com/dthuff/maze-nd/blob/master/examples/maze_kaboom_90_40.png)
