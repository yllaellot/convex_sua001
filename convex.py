from deq import Deq
from r2point import R2Point


class Figure:
    """ Абстрактная фигура """

    def perimeter(self):
        return 0.0

    def area(self):
        return 0.0

    def distance(self):
        return 0.0


class Void(Figure):
    """ "Hульугольник" """

    def __init__(self, pointA):
        self.pointA = pointA

    def add(self, p):
        return Point(p, self.pointA)


class Point(Figure):
    """ "Одноугольник" """

    def __init__(self, p, pointA):
        self.p = p
        self.A = pointA
        self.min_dist = ((p.x - pointA.x)**2 + (p.y - pointA.y)**2)**0.5

    def add(self, q):
        return self if self.p == q else Segment(self.p, q, self.A,
                                                self.min_dist)

    def distance(self):
        return (self.min_dist)


class Segment(Figure):
    """ "Двуугольник" """

    def __init__(self, p, q, pointA, md):
        self.p, self.q, self.min_dist, self.A = p, q, md, pointA

    def perimeter(self):
        return 2.0 * self.p.dist(self.q)

    def add(self, r):
        if R2Point.is_triangle(self.p, self.q, r):
            return Polygon(self.p, self.q, r, self.A, self.min_dist)
        elif self.q.is_inside(self.p, r):
            return Segment(self.p, r, self.A, self.min_dist)
        elif self.p.is_inside(self.q, r):
            return Segment(self.q, r, self.A, self.min_dist)
        else:
            return self

    def distance(self):
        self.min_dist = min(self.min_dist,
                            R2Point.find_distance(self.p, self.q, self.A))
        return (self.min_dist)


class Polygon(Figure):
    """ Многоугольник """

    def __init__(self, a, b, c, pointA, el):
        self.points = Deq()
        self.A = pointA
        self.points.push_first(b)
        if b.is_light(a, c):
            self.points.push_first(a)
            self.points.push_last(c)
        else:
            self.points.push_last(a)
            self.points.push_first(c)
        self._perimeter = a.dist(b) + b.dist(c) + c.dist(a)
        self._area = abs(R2Point.area(a, b, c))
        self.key = R2Point.in_trangle(a, b, c, pointA)
        if (self.key == 1):
            self.min_dist = 0
        else:
            self.min_dist = min(el, R2Point.find_distance(c, a, self.A),
                                R2Point.find_distance(c, b, self.A))

    def perimeter(self):
        return self._perimeter

    def area(self):
        return self._area

    def distance(self):
        return self.min_dist

    # добавление новой точки
    def add(self, t):

        # поиск освещённого ребра
        for n in range(self.points.size()):
            if t.is_light(self.points.last(), self.points.first()):
                break
            self.points.push_last(self.points.pop_first())

        # хотя бы одно освещённое ребро есть
        if t.is_light(self.points.last(), self.points.first()):

            # учёт удаления ребра, соединяющего конец и начало дека
            self._perimeter -= self.points.first().dist(self.points.last())
            self._area += abs(R2Point.area(t,
                                           self.points.last(),
                                           self.points.first()))
            if (self.key == 0 and R2Point.in_trangle(self.points.first(),
                                                     self.points.last(), t,
                                                     self.A)):
                self.min_dist = 0
                self.key = 1

            # удаление освещённых рёбер из начала дека
            p = self.points.pop_first()
            while t.is_light(p, self.points.first()):
                self._perimeter -= p.dist(self.points.first())
                self._area += abs(R2Point.area(t, p, self.points.first()))
                if (self.key == 0 and R2Point.in_trangle(self.points.first(),
                                                         p, t, self.A)):
                    self.min_dist = 0
                    self.key = 1
                p = self.points.pop_first()
            self.points.push_first(p)

            # удаление освещённых рёбер из конца дека
            p = self.points.pop_last()
            while t.is_light(self.points.last(), p):
                self._perimeter -= p.dist(self.points.last())
                self._area += abs(R2Point.area(t, p, self.points.last()))
                if (self.key == 0 and R2Point.in_trangle(p, self.points.last(),
                                                         t, self.A)):
                    self.min_dist = 0
                    self.key = 1
                p = self.points.pop_last()
            self.points.push_last(p)

            # добавление двух новых рёбер
            self._perimeter += t.dist(self.points.first()) + \
                t.dist(self.points.last())
            if (self.key == 0):
                R2Point.per(self, t)
            self.points.push_first(t)

        return self


if __name__ == "__main__":
    f = Polygon(
        R2Point(
            0.1, -0.1), R2Point(
            -0.1, 0.1), R2Point(
            -0.0, 0.2), R2Point(
            -0.2, 0.1), 1)
    f.add(R2Point(0.0, -0.2))
    f.add(R2Point(-0.7, 0.0))
