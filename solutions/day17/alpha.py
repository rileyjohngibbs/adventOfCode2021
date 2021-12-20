from enum import Enum
import re
from typing import Optional

from solutions.common.point import BoundingBox, Point


def digest_input(input_lines: list[str]) -> BoundingBox:
    coordinates = (
        int(g)
        for g in re.match(
            r".*?(\d+).*?(\d+).*?(-?\d+).*?(-?\d+)", input_lines[0]
        ).groups()
    )
    return BoundingBox(*coordinates)


def part_one(bounding_box: BoundingBox) -> int:
    min_x_velocity = calculate_minimum_x_velocity(bounding_box.x1)
    max_x_velocity = bounding_box.x2
    highest_shot = 0
    for dx in range(min_x_velocity, max_x_velocity + 1):
        overshot = False
        dy = bounding_box.y1 - 1
        while not overshot and dy < -(bounding_box.y1):
            dy += 1
            height, shot_result = calculate_arc(dx, dy, bounding_box)
            if shot_result is ShotResult.HIT and highest_shot < height:
                highest_shot = height
            else:
                overshot = shot_result is ShotResult.OVERSHOT
    return highest_shot


class ShotResult(Enum):
    MISS = 0
    HIT = 1
    OVERSHOT = 2


def calculate_minimum_x_velocity(left_bound: int) -> int:
    x = 0
    while (x**2 + x) / 2 < left_bound:
        x += 1
    return x


def calculate_arc(dx: int, dy: int, target: BoundingBox) -> tuple[int, ShotResult]:
    """Returns highest point and the result"""
    x, y = 0, 0
    max_height = 0
    while x <= target.x2 and y >= target.y1:
        x += dx
        if dx > 0:
            dx -= 1
        y += dy
        dy -= 1
        if y > max_height:
            max_height = y
        if x > target.x2 and y > target.y2:
            return max_height, ShotResult.OVERSHOT
        if target.contains(Point(x, y)):
            return max_height, ShotResult.HIT
        if y < target.y1 or x > target.x2:
            return max_height, ShotResult.MISS


def part_two(bounding_box: BoundingBox) -> int:
    min_x_velocity = calculate_minimum_x_velocity(bounding_box.x1)
    max_x_velocity = bounding_box.x2
    count = 0
    for dx in range(min_x_velocity, max_x_velocity + 1):
        overshot = False
        dy = bounding_box.y1 - 1
        while not overshot and dy < -(bounding_box.y1):
            dy += 1
            height, shot_result = calculate_arc(dx, dy, bounding_box)
            if shot_result is ShotResult.HIT:
                count += 1
            else:
                overshot = shot_result is ShotResult.OVERSHOT
    return count
