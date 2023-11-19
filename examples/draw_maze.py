from maze_nd.maze_nd import MazeND
import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--theme", type=str)
    parser.add_argument("shape", type=int, nargs="*")
    parser.add_argument("--skip-animation", action='store_true', default=False)
    cl_args = parser.parse_args()
    return cl_args


if __name__ == "__main__":
    args = parse_args()
    maze = MazeND(args.shape,
                  animate_generation=not args.skip_animation,
                  wait_to_destroy_image=True,
                  theme=args.theme)
