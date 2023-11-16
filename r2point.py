from math import sqrt


class R2Point:
    """ Точка (Point) на плоскости (R2) """

    # Конструктор
    def __init__(self, x=None, y=None):
        if x is None:
            x = float(input("x -> "))
        if y is None:
            y = float(input("y -> "))
        self.x, self.y = x, y

    # Площадь треугольника
    @staticmethod
    def area(a, b, c):
        return 0.5 * ((a.x - c.x) * (b.y - c.y) - (a.y - c.y) * (b.x - c.x))

    # Лежат ли точки на одной прямой?
    @staticmethod
    def is_triangle(a, b, c):
        return R2Point.area(a, b, c) != 0.0

    # Пересчет при удалении  (sua001)+
    def per(self_convex, t):
        self_convex.min_dist = min(self_convex.min_dist,
                                   R2Point.find_distance(
                                       t,
                                       self_convex.points.last(),
                                       self_convex.A),
                                   R2Point.find_distance(
                                       t,
                                       self_convex.points.first(),
                                       self_convex.A))

    # векторное произведение (sua001)+
    def vec(self, other):
        return ((other.y*self.x) - (other.x*self.y))

    # Лежит ли точка P внутри треугольника ABC (sua001)+
    def in_trangle(A, B, C, P):
        self = R2Point(B.x - A.x, B.y - A.y)
        self_ = R2Point(P.x - A.x, P.y - A.y)
        other1 = R2Point(C.x - B.x, C.y - B.y)
        other1_ = R2Point(P.x - B.x, P.y - B.y)
        other2 = R2Point(A.x - C.x, A.y - C.y)
        other2_ = R2Point(P.x - C.x, P.y - C.y)
        if ((R2Point.vec(self, self_) <= 0 and R2Point.vec(other1, other1_)
             <= 0 and R2Point.vec(other2, other2_) <= 0) or
            (R2Point.vec(self, self_) >= 0 and
             R2Point.vec(other1, other1_) >= 0 and
             R2Point.vec(other2, other2_) >= 0)):
            return 1
        else:
            return 0

    # Расстояние до другой точки
    def dist(self, other):
        return sqrt((other.x - self.x)**2 + (other.y - self.y)**2)

    # Лежит ли точка внутри "стандартного" прямоугольника?
    def is_inside(self, a, b):
        return (((a.x <= self.x and self.x <= b.x) or
                 (a.x >= self.x and self.x >= b.x)) and
                ((a.y <= self.y and self.y <= b.y) or
                 (a.y >= self.y and self.y >= b.y)))

    # Освещено ли из данной точки ребро (a,b)?
    def is_light(self, a, b):
        s = R2Point.area(a, b, self)
        return s < 0.0 or (s == 0.0 and not self.is_inside(a, b))

    # Совпадает ли точка с другой?
    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.x == other.x and self.y == other.y
        return False

    def scalar(p, q):
        return (p.x*q.x + p.y*q.y)

    def find_distance(p, q, pointA):
        a = R2Point((q.x - p.x), (q.y - p.y))
        pA = R2Point((pointA.x - p.x), (pointA.y - p.y))
        qA = R2Point((pointA.x - q.x), (pointA.y - q.y))
        alfa_1 = R2Point.scalar(pA, a)
        alfa_2 = -R2Point.scalar(qA, a)
        if (alfa_1 > 0 and alfa_2 <= 0):
            return R2Point.dist(pointA, q)
        elif (alfa_2 > 0 and alfa_1 <= 0):
            return R2Point.dist(pointA, p)
        else:
            # тут гг
            a_normal = R2Point(a.y/(a.y**2+a.x**2)**0.5,
                               -a.x/(a.y**2+a.x**2)**0.5)
            return (abs(R2Point.scalar(a_normal, pA)))


if __name__ == "__main__":
    x = R2Point(1.0, 1.0)
    print(type(x), x.__dict__)
    print(x.dist(R2Point(1.0, 0.0)))
    a, b, c = R2Point(0.0, 0.0), R2Point(1.0, 0.0), R2Point(1.0, 1.0)
    print(R2Point.area(a, c, b))
