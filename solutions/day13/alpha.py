from dataclasses import dataclass
from enum import Enum
import pytest


BOLD = "\033[1m"
PLAIN = "\033[0m"


def digest_input(input_lines: list[str]) -> tuple[list["Point"], list["Fold"]]:
    points, folds = [], []
    section = "points"
    for input_line in input_lines:
        if not input_line:
            section = "folds"
        elif section == "points":
            str_x, str_y = input_line.split(",", 1)
            points.append(Point(int(str_x), int(str_y)))
        elif section == "folds":
            var, value = input_line[11:].split("=", 1)
            direction = (
                FoldDirection.VERTICAL if var == "y" else FoldDirection.HORIZONTAL
            )
            folds.append(Fold(direction, int(value)))
    return points, folds


@dataclass(frozen=True)
class Point:
    x: int
    y: int


class FoldDirection(Enum):
    VERTICAL = 0
    HORIZONTAL = 1


@dataclass
class Fold:
    direction: FoldDirection
    coordinate: int

    def should_reflect(self, point: "Point") -> bool:
        return (
            self.direction is FoldDirection.VERTICAL
            and point.y > self.coordinate
            or self.direction is FoldDirection.HORIZONTAL
            and point.x > self.coordinate
        )


def part_one(points_folds: tuple[list["Point"], list["Fold"]]) -> int:
    points = set(points_folds[0])
    folds = points_folds[1]
    for fold in folds:
        points_to_reflect = [p for p in points if fold.should_reflect(p)]
        for point in points_to_reflect:
            points.remove(point)
            points.add(reflect(point, fold))
        break
    return len(points)


def part_two(points_folds: tuple[list["Point"], list["Fold"]]) -> str:
    points = set(points_folds[0])
    folds = points_folds[1]
    for fold in folds:
        points_to_reflect = [p for p in points if fold.should_reflect(p)]
        for point in points_to_reflect:
            points.remove(point)
            points.add(reflect(point, fold))
    width, height = (max(p.x for p in points) + 1, max(p.y for p in points) + 1)
    display_string = "\n".join(
        "".join(
            f"{BOLD}⌼⌼{PLAIN}" if Point(x, y) in points else ".."
            for x in range(width)
        )
        for y in range(height)
    )
    return f"\n{display_string}"


def reflect(point: "Point", fold: "Fold") -> "Point":
    return (
        Point(2 * fold.coordinate - point.x, point.y)
        if fold.direction is FoldDirection.HORIZONTAL
        else Point(point.x, 2 * fold.coordinate - point.y)
    )


@pytest.fixture
def example():
    return [
        "6,10",
        "0,14",
        "9,10",
        "0,3",
        "10,4",
        "4,11",
        "6,0",
        "6,12",
        "4,1",
        "0,13",
        "10,12",
        "3,4",
        "3,0",
        "8,4",
        "1,10",
        "2,14",
        "8,10",
        "9,0",
        "",
        "fold along y=7",
        "fold along x=5",
    ]


def test_part_one(example):
    assert part_one(digest_input(example)) == 17
