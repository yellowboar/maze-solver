from window import Window
from geometry import *
from maze import *

def main():
    win = Window(800, 600)
    maze = Maze(0, 0, 10, 12, 10, 10, win)
    maze._create_cells()
    print(maze)
    win.wait_for_close()

if __name__ == '__main__':
    main()
