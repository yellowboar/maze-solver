from window import Window
from geometry import *

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
        self._win = win

    def draw(self):
        if self.has_left_wall:
            self._win.draw_line(Line(self._p1, self._p3))
        if self.has_right_wall:
            self._win.draw_line(Line(self._p2, self._p4))
        if self.has_top_wall:
            self._win.draw_line(Line(self._p1, self._p2))
        if self.has_bottom_wall:
            self._win.draw_line(Line(self._p3, self._p4))
        
    def draw_move(self, to_cell, undo=False):
        fill_color = "gray" if undo else "red"
        self._win.draw_line(Line(self._center, to_cell._center), fill_color)

    def __repr__(self) -> str:
        return f"Cell with top-left corner: {self._p1}"

class Maze():
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None) -> None:
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self._cells = []
    
    def _create_cells(self):
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
            self._cells.append(row)

    def __repr__(self):
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                print(self._cells[i][j])
