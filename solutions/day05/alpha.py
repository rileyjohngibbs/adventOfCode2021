from solutions.common.point import Point


def digest_input(input_lines: list[str]) -> list[tuple["Point", "Point"]]:
    digested = []
    for line in input_lines:
        start, end = line.split(" -> ", 1)
        digested.append((Point.from_string(start), Point.from_string(end)))
    return digested


def part_one(vents: list[tuple["Point", "Point"]]) -> int:
    ones: set[Point] = set()
    twos: set[Point] = set()
    rectilinear_vents = ((v1, v2) for v1, v2 in vents if v1.x == v2.x or v1.y == v2.y)
    for vent in rectilinear_vents:
        for point in interpolate(*vent):
            if point not in ones:
                ones.add(point)
            else:
                twos.add(point)
    return len(twos)


def part_two(vents: list[tuple["Point", "Point"]]) -> int:
    ones: set[Point] = set()
    twos: set[Point] = set()
    for vent in vents:
        for point in interpolate(*vent):
            if point not in ones:
                ones.add(point)
            else:
                twos.add(point)
    return len(twos)


def interpolate(start: "Point", end: "Point") -> set["Point"]:
    length = max(abs(start.x - end.x), abs(start.y - end.y))
    dx = (end.x - start.x) // length
    dy = (end.y - start.y) // length
    return {Point(start.x + dx * k, start.y + dy * k) for k in range(length)} | {end}
