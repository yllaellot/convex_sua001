#!/usr/bin/env -S python3 -B
from r2point import R2Point
from convex import Void

print("Введите фиксированную точку: ")
a = R2Point()
f = Void(a)
print("Начло работы с выпуклой оболочкой:")
try:
    while True:
        f = f.add(R2Point())
        print(f"S = {f.area()}, P = {f.perimeter()},",
              f" Минимальное расстояние фиксированной точки: {f.distance()}\n")
        print()
except (EOFError, KeyboardInterrupt):
    print("\nStop")
