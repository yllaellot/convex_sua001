from pytest import approx
from math import sqrt
from r2point import R2Point
from convex import Polygon


class TestR2Point:

    def setup_method(self):
        self.f = Polygon(
            R2Point(
                0.0, -2.0), R2Point(
                1.0, -1.0), R2Point(
                1.0, 1.0), R2Point(
                -1.0, 0.0), 1.5811388300841895)

    # Расстояние от точки до самой себя равно нулю
    def test_dist1(self):
        a = R2Point(1.0, 1.0)
        assert a.dist(R2Point(1.0, 1.0)) == approx(0.0)

    # Расстояние между двумя различными точками положительно
    def test_dist2(self):
        a = R2Point(1.0, 1.0)
        assert a.dist(R2Point(1.0, 0.0)) == approx(1.0)

    def test_dist3(self):
        a = R2Point(1.0, 1.0)
        assert a.dist(R2Point(0.0, 0.0)) == approx(sqrt(2.0))

    # Площадь треугольника равна нулю, если все вершины совпадают
    def test_area1(self):
        a = R2Point(1.0, 1.0)
        assert R2Point.area(a, a, a) == approx(0.0)

    # Площадь треугольника равна нулю, если все вершины лежат на одной прямой
    def test_area2(self):
        a, b, c = R2Point(0.0, 0.0), R2Point(1.0, 1.0), R2Point(2.0, 2.0)
        assert R2Point.area(a, b, c) == approx(0.0)

    # Площадь треугольника положительна при обходе вершин против часовой
    # стрелки
    def test_area3(self):
        a, b, c = R2Point(0.0, 0.0), R2Point(1.0, 0.0), R2Point(1.0, 1.0)
        assert R2Point.area(a, b, c) > 0.0

    # Площадь треугольника отрицательна при обходе вершин по часовой стрелке
    def test_area4(self):
        a, b, c = R2Point(0.0, 0.0), R2Point(1.0, 0.0), R2Point(1.0, 1.0)
        assert R2Point.area(a, c, b) < 0.0

    # Точки могут лежать внутри и вне "стандартного" прямоугольника с
    # противопложными вершинами (0,0) и (2,1)
    def test_is_inside1(self):
        a, b = R2Point(0.0, 0.0), R2Point(2.0, 1.0)
        assert R2Point(1.0, 0.5).is_inside(a, b) is True

    def test_is_inside2(self):
        a, b = R2Point(0.0, 0.0), R2Point(2.0, 1.0)
        assert R2Point(1.0, 0.5).is_inside(b, a) is True

    def test_is_inside3(self):
        a, b = R2Point(0.0, 0.0), R2Point(2.0, 1.0)
        assert R2Point(1.0, 1.5).is_inside(a, b) is False

    # Ребро [(0,0), (1,0)] может быть освещено или нет из определённой точки
    def test_is_light1(self):
        a, b = R2Point(0.0, 0.0), R2Point(1.0, 0.0)
        assert R2Point(0.5, 0.0).is_light(a, b) is False

    def test_is_light2(self):
        a, b = R2Point(0.0, 0.0), R2Point(1.0, 0.0)
        assert R2Point(2.0, 0.0).is_light(a, b) is True

    def test_is_light3(self):
        a, b = R2Point(0.0, 0.0), R2Point(1.0, 0.0)
        assert R2Point(0.5, 0.5).is_light(a, b) is False

    def test_is_light4(self):
        a, b = R2Point(0.0, 0.0), R2Point(1.0, 0.0)
        assert R2Point(0.5, -0.5).is_light(a, b) is True

    # векторное произведение векторов a и b
    def test_vec_1(self):
        a, b = R2Point(0.0, 0.0), R2Point(1.0, 0.0)
        assert R2Point.vec(a, b) == 0.0

    def test_vec_2(self):
        a, b = R2Point(1.0, 1.0), R2Point(1.0, 2.0)
        assert R2Point.vec(a, b) == 1.0

    # Лежит ли точка P внутри треугольника ABC (sua001)
    def test_in_trangle_1(self):
        a, b, c = R2Point(0.0, 0.0), R2Point(1.0, 2.0), R2Point(2.0, 0.0)
        p = R2Point(1.0, 1.0)
        assert R2Point.in_trangle(a, b, c, p) == 1

    def test_in_trangle_2(self):
        a, b, c = R2Point(0.0, 0.0), R2Point(1.0, 2.0), R2Point(2.0, 0.0)
        p = R2Point(0.0, 0.0)
        assert R2Point.in_trangle(a, b, c, p) == 1

    def test_in_trangle_3(self):
        a, b, c = R2Point(0.0, 0.0), R2Point(1.0, 2.0), R2Point(2.0, 0.0)
        p = R2Point(1.0, 0.0)
        assert R2Point.in_trangle(a, b, c, p) == 1

    def test_in_trangle_4(self):
        a, b, c = R2Point(0.0, 0.0), R2Point(1.0, 2.0), R2Point(2.0, 0.0)
        p = R2Point(4.0, 4.0)
        assert R2Point.in_trangle(a, b, c, p) == 0

    # Пересчет при удалении  (sua001)
    def test_per_1(self):
        R2Point.per(self.f, R2Point(0.0, 2.0))
        assert self.f.distance() == 1.0

    def test_per_2(self):
        R2Point.per(self.f, R2Point(-1.0, 2.0))
        assert self.f.distance() == approx(0.48507125007266594)
