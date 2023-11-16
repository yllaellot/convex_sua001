#!/usr/bin/env -S python3 -B
from tk_drawer import TkDrawer
from r2point import R2Point
from convex import Void, Point, Segment, Polygon


def void_draw(self, tk):
    pass


def point_draw(self, tk):
    tk.draw_point(self.p)
    tk.draw_point_const(self.A)


def segment_draw(self, tk):
    tk.draw_line(self.p, self.q)
    tk.draw_point_const(self.A)


def polygon_draw(self, tk):
    tk.draw_point_const(self.A)
    for n in range(self.points.size()):
        tk.draw_line(self.points.last(), self.points.first())
        self.points.push_last(self.points.pop_first())


setattr(Void, 'draw', void_draw)
setattr(Point, 'draw', point_draw)
setattr(Segment, 'draw', segment_draw)
setattr(Polygon, 'draw', polygon_draw)


tk = TkDrawer()
tk.clean()
print("Введите фиксированную точку: ")
a = R2Point()
f = Void(a)
print("Начло работы с выпуклой оболочкой:")
try:
    while True:
        f = f.add(R2Point())
        tk.clean()
        f.draw(tk)
        print(f"S = {f.area()}, P = {f.perimeter()},",
              f" Минимальное расстояние фиксированной точки: {f.distance()}\n")
except (EOFError, KeyboardInterrupt):
    print("\nStop")
    tk.close()
