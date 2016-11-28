from sympy import solve, symbols
import math
from operator import itemgetter
import pickle

x0, y0 = (0, 0)
x1, y1 = (23, 0)
R = SD = AK = KB = 24.5
KD = AS = 23
KM = NF = 6.5
KN = MF = GN = ED = 16.5
ND = 6.5
EG = 6.7
SE = 8
INCREMENT = 0.02


def solve_system(point1, point2, l1, l2, **kwargs):
    x, y = symbols('x y')

    def make_eq(point, l):
        _x, _y = point
        return (_x - x)**2 + (_y - y)**2 - l**2

    (x, y), _ = sorted(solve([make_eq(point1, l1), make_eq(point2, l2)], x, y), **kwargs)
    return x, y


def solve_for_line(point1, point2, l1, positive=True):
    (_x1, _y1), (_x2, _y2) = point1, point2
    tg = (_y1 - _y2) / (_x1 - _x2)
    coef = 1 if positive else -1
    cos = coef * (1 / (tg**2 + 1))**0.5
    x = _x2 - l1 * cos
    y = _y2 - tg * (_x2 - x)
    return x, y


def angle_generator(increment):
    angle = -0.8
    while angle <= -0.8:
        angle -= increment
        if angle < -math.pi:
            increment *= -1
        yield angle


def main():

    angles = angle_generator(INCREMENT)
    data = []
    for fi in angles:
        try:
            x3, y3 = R * math.cos(fi), R * math.sin(fi)
            x2, y2 = solve_system((x1, y1), (x3, y3), KB, KD)
            x9, y9 = solve_for_line((x1, y1), (x2, y2), KM, positive=False)  # M
            x10, y10 = solve_for_line((x2, y2), (x3, y3), ND, positive=(fi > - math.pi / 2))
            x8, y8 = solve_system((x9, y9), (x10, y10), MF, NF, key=itemgetter(0), reverse=True)  # we need solution with greater x
            x7, y7 = solve_for_line((x8, y8), (x10, y10), GN)  # G
            x6, y6 = solve_system((x3, y3), (x7, y7), ED, EG, key=itemgetter(1), reverse=True)  # we need solution with greater y
            x4, y4 = solve_for_line((x6, y6), (x3, y3), SD)  # S
            x5, y5 = solve_system((x4, y4), (x2, y2), AS, AK, key=itemgetter(1), reverse=True)  # we need solution with greater y
        except TypeError:
            continue
        data.append([(x3, y3), (x2, y2), (x9, y9), (x10, y10), (x8, y8), (x7, y7), (x6, y6), (x4, y4), (x5, y5), fi])
    with open("data", "wb") as f:
        pickle.dump(data, f)


if __name__ == '__main__':
    main()
