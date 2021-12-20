from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    @classmethod
    def from_string(cls, string_address: str) -> "Point":
        x, y = string_address.split(",", 1)
        return cls(int(x), int(y))


@dataclass(frozen=True)
class BoundingBox:
    x1: int
    x2: int
    y1: int
    y2: int

    def contains(self, point: "Point") -> bool:
        return self.x1 <= point.x <= self.x2 and self.y1 <= point.y <= self.y2
