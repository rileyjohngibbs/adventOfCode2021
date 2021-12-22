from dataclasses import dataclass
from itertools import product
from typing import Optional

import pytest


def digest_input(input_lines: list[str]) -> list["Scanner"]:
    scanners: list[Scanner] = []
    new_beacons: list[Vector] = []
    for input_line in input_lines:
        if input_line.startswith("---"):
            new_beacons = []
        elif input_line:
            coords = (int(c) for c in input_line.split(","))
            beacon = Vector(*coords)
            new_beacons.append(beacon)
        else:
            scanner = Scanner(new_beacons)
            scanners.append(scanner)
    scanner = Scanner(new_beacons)
    scanners.append(scanner)
    return scanners


def part_one(scanners: list["Scanner"]) -> int:
    beacons: set[Vector] = set()
    scanner_zero = scanners.pop(0)
    for beacon in scanner_zero.beacons:
        beacons.add(beacon)
    translations_to_zero: list[tuple[Scanner, Vector]] = [
        (scanner_zero, Vector(0, 0, 0))
    ]
    count = 0
    count_limit = len(scanners) ** 2
    while scanners:
        count += 1
        if count > count_limit:
            raise Exception("Seems like this is going on too long")
        scanner_to_try = scanners.pop(0)
        for base_scanner, base_translation in translations_to_zero:
            translation = scanner_to_try.match_any_rotation(base_scanner)
            if translation is not None:
                full_translation = base_translation + translation
                translations_to_zero.append((scanner_to_try, full_translation))
                for beacon in scanner_to_try.beacons:
                    beacons.add(beacon + full_translation)
                break
        else:
            scanners.append(scanner_to_try)
    return len(beacons)


def part_two(scanners: list["Scanner"]) -> int:
    beacons: set[Vector] = set()
    scanner_zero = scanners.pop(0)
    for beacon in scanner_zero.beacons:
        beacons.add(beacon)
    translations_to_zero: list[tuple[Scanner, Vector]] = [
        (scanner_zero, Vector(0, 0, 0))
    ]
    count = 0
    count_limit = len(scanners) ** 2
    while scanners:
        count += 1
        if count > count_limit:
            raise Exception("Seems like this is going on too long")
        scanner_to_try = scanners.pop(0)
        for base_scanner, base_translation in translations_to_zero:
            translation = scanner_to_try.match_any_rotation(base_scanner)
            if translation is not None:
                full_translation = base_translation + translation
                translations_to_zero.append((scanner_to_try, full_translation))
                for beacon in scanner_to_try.beacons:
                    beacons.add(beacon + full_translation)
                break
        else:
            scanners.append(scanner_to_try)
    distances = [
        (a[1] - b[1]).manhattan_distance()
        for a, b in product(translations_to_zero, translations_to_zero)
    ]
    return max(distances)


@dataclass(frozen=True)
class Vector:
    x: int
    y: int
    z: int

    def __sub__(self, other: "Vector") -> "Vector":
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __neg__(self) -> "Vector":
        return Vector(-self.x, -self.y, -self.z)

    def manhattan_distance(self) -> int:
        return abs(self.x) + abs(self.y) + abs(self.z)


class Scanner:
    """
    z is forward
    x is right
    y is up
    """

    _relative_positions: Optional[tuple[set[Vector], ...]]

    def __init__(self, beacons: list[Vector], name: str = ""):
        self.beacons = beacons
        self._original_beacons = beacons[:]
        self._relative_positions = None
        self.name = name or f"{beacons[0]} and {len(beacons)} others"

    def __repr__(self) -> str:
        return f"<Scanner: {self.name}>"

    @property
    def relative_positions(self) -> tuple[set[Vector], ...]:
        if self._relative_positions is None:
            self._relative_positions = tuple(
                {other_beacon - beacon for other_beacon in self.beacons}
                for beacon in self.beacons
            )
        return self._relative_positions

    def yaw(self, count: int = 1) -> "Scanner":
        """
        Yaw left (counterclockwise) 90 degrees count times.
        z becomes x
        -x becomes z
        y remains
        """
        count %= 4

        def isometry(beacon: Vector) -> Vector:
            for _ in range(count):
                beacon = Vector(beacon.z, beacon.y, -beacon.x)
            return beacon

        self.beacons = [isometry(beacon) for beacon in self.beacons]
        self._relative_positions = None
        return self

    def roll(self, count: int = 1) -> "Scanner":
        """
        Roll counterclockwise 90 degrees count times.
        z remains
        x becomes y
        -y becomes x
        """
        count %= 4

        def isometry(beacon: Vector) -> Vector:
            for _ in range(count):
                beacon = Vector(-beacon.y, beacon.x, beacon.z)
            return beacon

        self.beacons = [isometry(beacon) for beacon in self.beacons]
        self._relative_positions = None
        return self

    def pitch(self, count: int = 1) -> "Scanner":
        """
        Pitch upward 90 degrees count times.
        z becomes y
        -y becomes z
        x remains
        """
        count %= 4

        def isometry(beacon: Vector) -> Vector:
            for _ in range(count):
                beacon = Vector(beacon.x, beacon.z, -beacon.y)
            return beacon

        self.beacons = [isometry(beacon) for beacon in self.beacons]
        self._relative_positions = None
        return self

    def match(self, other: "Scanner") -> Optional["Vector"]:
        """
        Returns Vector to other Scanner if 12 beacons can be matched.
        """
        for i, beacon in enumerate(self.beacons):
            relative_positions = self.relative_positions[i]
            for j, other_beacon in enumerate(other.beacons):
                other_relative_positions = other.relative_positions[j]
                common_count = len(relative_positions & other_relative_positions)
                if common_count >= 12:
                    return other_beacon - beacon
        else:
            return None

    def match_any_rotation(self, other: "Scanner") -> Optional["Vector"]:
        for rotation in self.all_rotations():
            rotation()
            match = self.match(other)
            if match is not None:
                return match
        return None

    def all_rotations(self):
        rotations = (
            (lambda: None, self.roll, self.roll, self.roll)
            + (lambda: self.roll().yaw(), self.roll, self.roll, self.roll)
            + (lambda: self.roll().yaw(), self.roll, self.roll, self.roll)
            + (lambda: self.roll().yaw(), self.roll, self.roll, self.roll)
            + (lambda: self.roll().pitch(), self.roll, self.roll, self.roll)
            + (lambda: self.pitch(2), self.roll, self.roll, self.roll)
        )
        return rotations


@pytest.fixture
def vectuples():
    return [
        (1, 2, 3),
        (4, 5, 6),
        (7, 2, 3),
        (12, 25, 21),
        (-10, -20, -30),
        (-5, 0, 5),
        (13, -13, -169),
        (8, 5, 3),
        (6, 6, 6),
        (3, 2, 1),
        (6, 5, 4),
        (3, 2, 7),
    ]


def test_match(vectuples):
    base_scanner = Scanner(
        [Vector(0, 1, 2), Vector(-1, 0, 1)] + [Vector(*v) for v in vectuples]
    )
    translation = Vector(10, -10, 0)
    other_scanner = Scanner(
        [Vector(0, -1, -2), Vector(1, 0, -1)]
        + [Vector(*v) + translation for v in vectuples]
    )
    matched_translation = other_scanner.match(base_scanner)
    translated_other_beacons = {b + matched_translation for b in other_scanner.beacons}
    assert len(translated_other_beacons | set(base_scanner.beacons)) == 16


def test_match_any(vectuples):
    base_scanner = Scanner(
        [Vector(0, 1, 2), Vector(-1, 0, 1)] + [Vector(*v) for v in vectuples]
    )
    translation = Vector(10, -10, 0)
    other_scanner = Scanner(
        [Vector(0, -1, -2), Vector(1, 0, -1)]
        + [Vector(*v) + translation for v in vectuples]
    )
    other_scanner.pitch()
    other_scanner.yaw()
    other_scanner.roll(3)
    matched_translation = other_scanner.match_any_rotation(base_scanner)
    translated_other_beacons = {b + matched_translation for b in other_scanner.beacons}
    assert len(translated_other_beacons | set(base_scanner.beacons)) == 16


def test_part_one(example):
    assert part_one(digest_input(example)) == 79


def test_all_rotations(vectuples):
    scanner = Scanner([Vector(*v) for v in vectuples])
    beacons_under_rotation: set[Vector] = set()
    for i, rotation in enumerate(scanner.all_rotations()):
        rotation()
        beacon_set = set(scanner.beacons)
        assert not beacons_under_rotation & beacon_set == beacon_set, (i, rotation)
        beacons_under_rotation.update(beacon_set)


def test_part_two(example):
    assert part_two(digest_input(example)) == 3621
