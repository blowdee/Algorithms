from shapely.geometry import LineString
from bisect import bisect_left, insort


class SweepLine:
    def __init__(self):
        self.values = []

    def insert(self, value):
        assert value not in self.values
        insort(self.values, value)

    def delete(self, value):
        assert value in self.values
        assert (self.values.pop(self.position(value)) == value)

    def find_neighbours(self, value):
        p = self.position(value)
        left = None
        right = None
        if p > 0:
            left = self.values[p - 1]
        if p < len(self.values) - 1:
            right = self.values[p + 1]
        return left, right

    def position(self, value):
        i = bisect_left(self.values, value)
        if i != len(self.values) and self.values[i] == value:
            return i
        raise ValueError


def cross_product(x1, y1, x2, y2):
    return x1 * y2 - y1 * x2


def intersect(o1, p1, o2, p2):
    d1 = (p1[0] - o1[0], p1[1] - o1[1])
    d2 = (p2[0] - o2[0], p2[1] - o2[1])

    cross = cross_product(d1[0], d1[1], d2[0], d2[1])

    x = (o2[0] - o1[0], o2[1] - o1[1])

    if abs(cross) == 0:
        return False

    t = cross_product(x[0], x[1], d2[0], d2[1])
    u = cross_product(x[0], x[1], d1[0], d1[1])

    t = float(t) / cross
    u = float(u) / cross

    if 0 < t < 1 and 0 < u < 1:
        return True

    return False


def find_intersections(segments):
    end_points = []
    for i, (x1, _, x2, _) in enumerate(segments):
        end_points.append((x1, i, x1 >= x2))
        end_points.append((x2, i, x1 < x2))

    end_points = sorted(end_points)
    sweep_line = SweepLine()
    res = []

    for _, label, is_right in end_points:
        segment = segments[label]
        if not is_right:
            sweep_line.insert(label)
            for n in sweep_line.find_neighbours(label):
                if n is not None and intersect(
                        (segment[0], segment[1]),
                        (segment[2], segment[3]),
                        (segments[n][0], segments[n][1]),
                        (segments[n][2], segments[n][3])
                ):
                    res.append([segment, segments[n]])
        else:
            p, s = sweep_line.find_neighbours(label)
            if p is not None and s is not None:
                predecessor = segments[p]
                successor = segments[s]
                if intersect((predecessor[0], predecessor[1]), (predecessor[2], predecessor[3]),
                             (successor[0], successor[1]), (successor[2], successor[3])):
                    res.append([predecessor, successor])
            sweep_line.delete(label)

    return res


with open('input.txt', 'r') as file:
    N = file.readline()
    lines = [tuple(map(int, x.split(' '))) for x in file.readlines()]

result = find_intersections(lines)

for (x11, y11, x12, y12), (x21, y21, x22, y22) in result:
    line1, line2 = LineString([(x11, y11), (x12, y12)]), LineString([(x21, y21), (x22, y22)])
    print(line1.intersection(line2))
