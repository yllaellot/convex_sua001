from pytest import approx
from math import sqrt
from r2point import R2Point
from convex import Figure, Void, Point, Segment, Polygon


class TestFigure:
    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        self.a = Figure()

    # area
    def test_figure1(self):
        assert self.a.area() == 0

    # perimeter
    def test_figure2(self):
        assert self.a.perimeter() == 0


class TestVoid:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        a = R2Point(-1.0, 0.0)
        self.f = Void(a)

    # Нульугольник является фигурой
    def test_figure(self):
        assert isinstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Void (нульугольник)
    def test_void(self):
        assert isinstance(self.f, Void)

    # Периметр нульугольника нулевой
    def test_perimeter(self):
        assert self.f.perimeter() == 0.0

    # Площадь нульугольника нулевая
    def test_аrea__1(self):
        assert self.f.area() == 0.0

    # Расстояние до фиксированной точки нульугольника равно нулю
    def test_аrea__2(self):
        assert self.f.distance() == 0.0

    # При добавлении точки нульугольник превращается в одноугольник
    def test_add(self):
        assert isinstance(self.f.add(R2Point(0.0, 0.0)), Point)


class TestPoint:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        self.f = Point(R2Point(0.0, 0.0), R2Point(-1.0, 0.0))

    # Одноугольник является фигурой
    def test_figure(self):
        assert isinstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Point (одноугольник)
    def test_point(self):
        assert isinstance(self.f, Point)

    # Периметр одноугольника нулевой
    def test_perimeter(self):
        assert self.f.perimeter() == 0.0

    # Площадь одноугольника нулевая
    def test_аrea_1(self):
        assert self.f.area() == 0.0

    # Расстояние до фиксированной точки от одноугольника равно длине отрезка
    # проведенного из вершины данного одноугольника к фиксированной точке
    def test_аrea_2(self):
        assert self.f.distance() == 1.0

    # При добавлении точки одноугольник может не измениться
    def test_add1(self):
        assert self.f.add(R2Point(0.0, 0.0)) is self.f

    # При добавлении точки одноугольник может превратиться в двуугольник
    def test_add2(self):
        assert isinstance(self.f.add(R2Point(1.0, 0.0)), Segment)


class TestSegment:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        self.f = Segment(R2Point(0.0, 0.0), R2Point(1.0, 0.0),
                         R2Point(0.0, 1.0), 1)

    # Двуугольник является фигурой
    def test_figure(self):
        assert isinstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Segment (двуугольник)
    def test_segment(self):
        assert isinstance(self.f, Segment)

    # Периметр двуугольника равен удвоенной длине отрезка
    def test_perimeter(self):
        assert self.f.perimeter() == approx(2.0)

    # Площадь двуугольника нулевая
    def test_аrea_1(self):
        assert self.f.area() == 0.0

    # Расстояние от фиксированной точки (0, 1) до отрезка ((0, 0), (1, 0))
    def test_аrea_2(self):
        assert self.f.distance() == 1.0

    # При добавлении точки двуугольник может не измениться
    def test_add1(self):
        assert self.f.add(R2Point(0.5, 0.0)) is self.f

    # При добавлении точки двуугольник может превратиться в другой двуугольник
    def test_add2(self):
        assert isinstance(self.f.add(R2Point(2.0, 0.0)), Segment)

    # При добавлении точки двуугольник может превратиться в другой двуугольник
    def test_add3(self):
        assert isinstance(self.f.add(R2Point(-1.0, 0.0)), Segment)

    # При добавлении точки двуугольник может превратиться в треугольник
    def test_add4(self):
        assert isinstance(self.f.add(R2Point(0.0, 1.0)), Polygon)


class TestPolygon:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        self.f = Polygon(
            R2Point(
                0.0, 0.0), R2Point(
                1.0, 0.0), R2Point(
                0.0, 1.0), R2Point(
                2.0, 0.0), 1)

    # Многоугольник является фигурой
    def test_figure(self):
        assert isinstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Polygon (многоугольник)
    def test_polygon(self):
        assert isinstance(self.f, Polygon)

    # Изменение количества вершин многоугольника
    #   изначально их три
    def test_vertexes1(self):
        assert self.f.points.size() == 3
    #   добавление точки внутрь многоугольника не меняет их количества

    def test_vertexes2(self):
        assert self.f.add(R2Point(0.1, 0.1)).points.size() == 3
    #   добавление другой точки может изменить их количество

    def test_vertexes3(self):
        assert self.f.add(R2Point(1.0, 1.0)).points.size() == 4
    #   изменения выпуклой оболочки могут и уменьшать их количество

    def test_vertexes4(self):
        assert self.f.add(
            R2Point(
                0.4,
                1.0)).add(
            R2Point(
                1.0,
                0.4)).add(
                    R2Point(
                        0.8,
                        0.9)).add(
                            R2Point(
                                0.9,
                                0.8)).points.size() == 7
        assert self.f.add(R2Point(2.0, 2.0)).points.size() == 4

    # Изменение периметра многоугольника
    #   изначально он равен сумме длин сторон
    def test_perimeter1(self):
        assert self.f.perimeter() == approx(2.0 + sqrt(2.0))
    #   добавление точки может его изменить

    def test_perimeter2(self):
        assert self.f.add(R2Point(1.0, 1.0)).perimeter() == approx(4.0)

    # Изменение площади многоугольника
    #   изначально она равна (неориентированной) площади треугольника
    def test_аrea1(self):
        assert self.f.area() == approx(0.5)
    #   добавление точки может увеличить площадь

    def test_area2(self):
        assert self.f.add(R2Point(1.0, 1.0)).area() == approx(1.0)

    # Расстояние от фиксированной точки (0.5, 0.5) до трапеции
    # ((0.4, 1.0), (1.0, 0.4), (0.8, 0.9), (0.9, 0.8))
    def test_аrea3(self):
        f = Polygon(
            R2Point(
                0.4, 1.0), R2Point(
                1.0, 0.4), R2Point(
                0.8, 0.9), R2Point(
                0.5, 0.5), 0.282842712474619)
        f.add(R2Point(0.9, 0.8))
        assert f.distance() == 0.282842712474619

    # Расстояние от фиксированной точки (0.1, -0.1) до треугольника
    # ((0.2, 0.0), (0.0, -0.2), (0.4, 0.0)
    def test_my1(self):
        f = Polygon(
            R2Point(
                0.2, 0.0), R2Point(
                0.1, 0.1), R2Point(
                0.1, -0.1), R2Point(
                0.2, -0.1), 1)
        f.add(R2Point(0.0, -0.2))
        f.add(R2Point(0.4, 0.0))
        assert f.distance() == 0.0

    def test_my2(self):
        f = Polygon(
            R2Point(
                -0.2, 0.0), R2Point(
                0.0, 0.3), R2Point(
                0.0, -0.3), R2Point(
                -0.2, -0.2), 0.11094003924504584)
        f.add(R2Point(0.2, 0.0))
        f.add(R2Point(-0.6, -0.3))
        assert f.distance() == 0.0

    #
    def test_my3(self):
        f = Polygon(
            R2Point(
                0.1, -0.1), R2Point(
                -0.1, 0.1), R2Point(
                -0.0, 0.2), R2Point(
                -0.2, 0.1), 1)
        f.add(R2Point(0.0, -0.2))
        f.add(R2Point(-0.7, 0.0))
        assert f.distance() == 0.0

    # Расстояние от фиксированной точки (2.0, 0.0) до трапеции
    # ((0.0, 1.0), (1.0, 0.0), (0.0, 0.0), (2.0, 1.0))
    def test_аrea4(self):
        self.f.add(R2Point(2.0, 1.0))
        assert self.f.distance() == 0.7071067811865475
