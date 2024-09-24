from window import Window
from geometry import *
from time import sleep
import random

class Cell():
    def __init__(self, 
                 p1 : Point, 
                 p2 : Point,
                 p3 : Point, 
                 p4 : Point,
                 win : Window=None,
                 has_left_wall=True,
                 has_right_wall=True, 
                 has_top_wall=True,
                 has_bottom_wall=True):
        
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall
        self._p1 = p1
        self._p2 = p2
        self._p3 = p3
        self._p4 = p4
        self._center = Point((p2.x + p1.x) // 2, (p3.y + p1.y) // 2)
        self.visited = False
        self._win = win

    def draw(self):
        left_wall = Line(self._p1, self._p3)
        right_wall = Line(self._p2, self._p4)
        top_wall = Line(self._p1, self._p2)
        bottom_wall = Line(self._p3, self._p4)

        if self.has_left_wall:
            self._win.draw_line(left_wall)
        else:
            self._win.draw_line(left_wall, "white")

        if self.has_right_wall:
            self._win.draw_line(right_wall)
        else:
            self._win.draw_line(right_wall, "white")

        if self.has_top_wall:
            self._win.draw_line(top_wall)
        else:
            self._win.draw_line(top_wall, "white")

        if self.has_bottom_wall:
            self._win.draw_line(bottom_wall)
        else:
            self._win.draw_line(bottom_wall, "white")
        
    def draw_move(self, to_cell, undo=False):
        fill_color = "gray" if undo else "red"
        self._win.draw_line(Line(self._center, to_cell._center), fill_color)

    def __repr__(self) -> str:
        return f"Cell with top-left corner: {self._p1}"

class Maze():
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None) -> None:
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self.seed = random.seed(seed) if not seed else seed
        self._cells = self._create_cells()
        self._draw_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        cells = []
        curr_y = self.y1
        for i in range(self.num_rows):
            row = []
            curr_x = self.x1
            new_y = curr_y + self.cell_size_y

            for j in range(self.num_cols):
                new_x = curr_x + self.cell_size_x
                cell = Cell(Point(curr_x, curr_y),
                            Point(new_x, curr_y),
                            Point(curr_x, new_y),
                            Point(new_x, new_y),
                            self.win)
                curr_x = new_x
                row.append(cell)
            curr_y = new_y
            cells.append(row)
        return cells

    def _draw_cells(self):
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        cell = self._cells[i][j]
        cell.draw()
        self._animate()

    def _break_entrance_and_exit(self):
        top_left = self._cells[0][0]
        bottom_right = self._cells[self.num_rows - 1][self.num_cols - 1]

        top_left.has_top_wall = False
        self._draw_cell(0, 0)

        bottom_right.has_bottom_wall = False
        self._draw_cell(self.num_rows - 1, self.num_cols - 1)

    def _break_walls_r(self, i, j):
        curr_cell = self._cells[i][j]
        curr_cell.visited = True
        self._cells[i][j].visited = True

        while True:
            to_visit = []
            visit = {}

            # left 
            if j > 0 and not self._cells[i][j - 1].visited:
                cell = self._cells[i][j - 1] 
                to_visit.append(cell)
                visit[cell] = (i, j - 1)

            # right
            if j < self.num_cols - 1 and not self._cells[i][j + 1].visited:
                cell = self._cells[i][j + 1]
                to_visit.append(cell)
                visit[cell] = (i, j + 1)
            
            # top
            if i > 0 and not self._cells[i - 1][j].visited:
                cell = self._cells[i - 1][j]
                to_visit.append(cell)
                visit[cell] = (i - 1, j)

            # bottom
            if i < self.num_rows - 1 and not self._cells[i + 1][j].visited:
                cell = self._cells[i + 1][j]
                to_visit.append(cell)
                visit[cell] = (i + 1, j)

            if not to_visit:
                self._draw_cell(i, j)
                return
            
            new_cell = to_visit[random.randrange(0, len(to_visit))]
            x, y = visit[new_cell]
            if x == i and y < j:
                curr_cell.has_left_wall = False
                new_cell.has_right_wall = False
            if x == i and y > j:
                curr_cell.has_right_wall = False
                new_cell.has_left_wall = False
            if y == j and x < i:
                curr_cell.has_top_wall = False
                new_cell.has_bottom_wall = False
            if y == j and x > i:
                curr_cell.has_bottom_wall = False
                new_cell.has_top_wall = False

            self._break_walls_r(x, y)

    def _reset_cells_visited(self):
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                cell = self._cells[i][j]
                cell.visited = False

    def solve(self):
        return self._solve_r(0, 0)
    
    def _solve_r(self, i, j):
        self._animate()
        if i == self.num_rows - 1 and j == self.num_cols - 1:
            return True
        
        curr_cell = self._cells[i][j]
        curr_cell.visited = True

        # left 
        if j > 0 and not self._cells[i][j - 1].visited:
            cell = self._cells[i][j - 1] 
            if not curr_cell.has_left_wall and not cell.has_right_wall:
                curr_cell.draw_move(cell)
                if self._solve_r(i, j - 1):
                    return True
                curr_cell.draw_move(cell, True)

        # right
        if j < self.num_cols - 1 and not self._cells[i][j + 1].visited:
            cell = self._cells[i][j + 1]
            if not curr_cell.has_right_wall and not cell.has_left_wall:
                curr_cell.draw_move(cell)
                if self._solve_r(i, j + 1):
                    return True
                curr_cell.draw_move(cell, True)
        
        # top
        if i > 0 and not self._cells[i - 1][j].visited:
            cell = self._cells[i - 1][j]
            if not curr_cell.has_top_wall and not cell.has_bottom_wall:
                curr_cell.draw_move(cell)
                if self._solve_r(i - 1, j):
                    return True
                curr_cell.draw_move(cell, True)
        # bottom
        if i < self.num_rows - 1 and not self._cells[i + 1][j].visited:
            cell = self._cells[i + 1][j]
            if not curr_cell.has_bottom_wall and not cell.has_top_wall:
                curr_cell.draw_move(cell)
                if self._solve_r(i + 1, j):
                    return True
                curr_cell.draw_move(cell, True)
        
        return False

    def _animate(self):
        self.win.redraw()
        sleep(0.05)

    def __repr__(self):
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                print(self._cells[i][j])