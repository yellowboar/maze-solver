from tkinter import Canvas

class Point():
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
    
    def get_tuple(self):
        return (self.x, self.y)

    def __repr__(self):
        return f"Point({self.x}, {self.y})"
    
class Line():
    def __init__(self, p1 : Point, p2 : Point) -> None:
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas : Canvas, fill_color):
        x1, y1 = self.p1.get_tuple()
        x2, y2 = self.p2.get_tuple()
        
        canvas.create_line(
            x1, y1, x2, y2, fill=fill_color, width=2
        )
