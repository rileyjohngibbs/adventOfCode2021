from functools import reduce
from typing import Any, Optional, Union

import pytest


def digest_input(input_lines: list[str]) -> list["Pair"]:
    return [Pair.from_string(input_line) for input_line in input_lines]


def part_one(pairs: list["Pair"]) -> int:
    return reduce(lambda a, b: a + b, pairs).magnitude()


def part_two(pairs: list["Pair"]) -> int:
    return max(
        a.copy().add(b.copy()).magnitude()
        for i, a in enumerate(pairs)
        for j, b in enumerate(pairs)
        if i != j
    )


class Pair:
    left: Union[int, "Pair"]
    right: Union[int, "Pair"]

    def __init__(self, left: Union[int, "Pair"], right: Union[int, "Pair"]):
        self.left = left
        self.right = right

    def __eq__(self, other: Any) -> bool:
        return (
            type(other) == Pair
            and self.left == other.left
            and self.right == other.right
        )

    def __repr__(self) -> str:
        return f"[{self.left},{self.right}]"

    def add(self, other: "Pair") -> "Pair":
        return Pair(self, other).fully_reduce()

    def __add__(self, other: "Pair") -> "Pair":
        """
        Open question: When running the solution on the problem input, if I use
        `(a.copy() + b.copy()).magnitude()` instead of performing the `.copy()` in this
        method, I get a lower (and incorrect) result. Why is it different to copy in
        here than it is to copy before sending into here?

        I've changed my solution to use `.add(other)` instead because I don't like
        having code in my solution that I don't fully understand.
        """
        return Pair(self.copy(), other.copy()).fully_reduce()

    @classmethod
    def from_string(cls, pair_string: str) -> "Pair":
        if not pair_string.startswith("[") or not pair_string.endswith("]"):
            raise ValueError(f"Invalid pair string {pair_string}")  # pragma: no cover
        depth = 0
        left_index = 1
        while not (depth == 0 and pair_string[left_index] == ","):
            if pair_string[left_index] == "[":
                depth += 1
            elif pair_string[left_index] == "]":
                depth -= 1
            left_index += 1
        left_string = pair_string[1:left_index]
        left: Union[int, Pair]
        if left_string.startswith("["):
            left = cls.from_string(left_string)
        else:
            left = int(left_string)
        right_string = pair_string[left_index + 1 : -1]
        right: Union[int, Pair]
        if right_string.startswith("["):
            right = cls.from_string(right_string)
        else:
            right = int(right_string)
        return cls(left, right)

    def copy(self) -> "Pair":
        left: Union[int, Pair]
        right: Union[int, Pair]
        if type(self.left) == Pair:
            left = self.left.copy()
        else:
            left = self.left
        if type(self.right) == Pair:
            right = self.right.copy()
        else:
            right = self.right
        return Pair(left, right)

    def fully_reduce(self) -> "Pair":
        reducing = True
        while reducing:
            reducing = self.reduce()
        return self

    def reduce(self) -> bool:
        original = self.copy()
        self.explode()
        if self == original:
            return self.split()
        return True

    def explode(self, depth: int = 0) -> Optional[tuple[int, int]]:
        if depth >= 4:
            if type(self.left) == int and type(self.right) == int:
                return (self.left, self.right)
            else:  # pragma: no cover
                raise TypeError(f"Tried exploding a non-numerical: {self}")
        if type(self.left) == Pair:
            left_explode = self.left.explode(depth + 1)
            if left_explode is not None:
                left, right = left_explode
                if depth == 3:
                    self.left = 0
                if type(self.right) == Pair:
                    self.right.add_left(right)
                elif type(self.right) == int:
                    self.right += right
                return (left, 0)
        if type(self.right) == Pair:
            right_explode = self.right.explode(depth + 1)
            if right_explode is not None:
                left, right = right_explode
                if depth == 3:
                    self.right = 0
                if type(self.left) == Pair:
                    self.left.add_right(left)
                elif type(self.left) == int:
                    self.left += left
                return (0, right)
        return None

    def add_right(self, addend: int) -> None:
        if type(self.right) == Pair:
            self.right.add_right(addend)
        elif type(self.right) == int:
            self.right += addend

    def add_left(self, addend: int) -> None:
        if type(self.left) == Pair:
            self.left.add_left(addend)
        elif type(self.left) == int:
            self.left += addend

    def split(self) -> bool:
        if type(self.left) == int and self.left >= 10:
            self.left = Pair(int(self.left / 2), int(self.left / 2 + 0.5))
            left_split = True
        elif type(self.left) == Pair:
            left_split = self.left.split()
        else:
            left_split = False
        if not left_split:
            if type(self.right) == int and self.right >= 10:
                self.right = Pair(int(self.right / 2), int(self.right / 2 + 0.5))
                return True
            elif type(self.right) == Pair:
                return self.right.split()
        return left_split

    def magnitude(self) -> int:
        if type(self.left) == int:
            left = self.left * 3
        elif type(self.left) == Pair:
            left = self.left.magnitude() * 3
        if type(self.right) == int:
            right = self.right * 2
        elif type(self.right) == Pair:
            right = self.right.magnitude() * 2
        return left + right


EXPLODING_NO_LEFT = Pair(Pair(Pair(Pair(Pair(3, 4), 2), 10), 5), 6)
EXPLODING = Pair(Pair(Pair(1, Pair(2, Pair(3, 4))), 5), 6)
REDUCED = Pair(Pair(Pair(1, Pair(2, 3)), 4), 5)
SPLITTING = Pair(Pair(Pair(10, Pair(2, 3)), 4), 5)


@pytest.mark.parametrize(
    "before, after",
    [
        (EXPLODING_NO_LEFT, Pair(Pair(Pair(Pair(0, 6), 10), 5), 6)),
        (EXPLODING, Pair(Pair(Pair(1, Pair(5, 0)), 9), 6)),
        (REDUCED, REDUCED),
        (SPLITTING, SPLITTING),
    ],
)
def test_explode(before, after):
    before_copy = before.copy()
    before_copy.explode()
    assert before_copy == after


@pytest.mark.parametrize(
    "before, after",
    [
        (EXPLODING_NO_LEFT, Pair(Pair(Pair(Pair(Pair(3, 4), 2), Pair(5, 5)), 5), 6)),
        (EXPLODING, EXPLODING),
        (REDUCED, REDUCED),
        (SPLITTING, Pair(Pair(Pair(Pair(5, 5), Pair(2, 3)), 4), 5)),
    ],
)
def test_split(before, after):
    before_copy = before.copy()
    before_copy.split()
    assert before_copy == after


@pytest.mark.parametrize(
    "before, after",
    [
        (EXPLODING_NO_LEFT, Pair(Pair(Pair(Pair(0, 6), 10), 5), 6)),
        (EXPLODING, Pair(Pair(Pair(1, Pair(5, 0)), 9), 6)),
        (REDUCED, REDUCED),
        (SPLITTING, Pair(Pair(Pair(Pair(5, 5), Pair(2, 3)), 4), 5)),
    ],
)
def test_reduce(before, after):
    before_copy = before.copy()
    before_copy.reduce()
    assert before_copy == after


def test_from_string():
    assert Pair.from_string("[[1,2],[3,[4,5]]]") == Pair(
        Pair(1, 2), Pair(3, Pair(4, 5))
    )


EXAMPLE = [
    "[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]",
    "[[[5,[2,8]],4],[5,[[9,9],0]]]",
    "[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]",
    "[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]",
    "[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]",
    "[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]",
    "[[[[5,4],[7,7]],8],[[8,3],8]]",
    "[[9,3],[[9,9],[6,[4,9]]]]",
    "[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]",
    "[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]",
]


def test_part_one():
    assert part_one(digest_input(EXAMPLE)) == 4140


def test_part_two():
    assert part_two(digest_input(EXAMPLE)) == 3993


SUM_TESTS = [
    "[1,1]",
    "[2,2]",
    "[3,3]",
    "[4,4]",
    "[5,5]",
    "[6,6]",
]


@pytest.mark.parametrize(
    "pair_strings, sum_string",
    [
        (SUM_TESTS[:-2], "[[[[1,1],[2,2]],[3,3]],[4,4]]"),
        (SUM_TESTS[:-1], "[[[[3,0],[5,3]],[4,4]],[5,5]]"),
        (SUM_TESTS[:], "[[[[5,0],[7,4]],[5,5]],[6,6]]"),
    ],
)
def test_summing(pair_strings, sum_string):
    pairs = [Pair.from_string(s) for s in pair_strings]
    total = pairs[0]
    for pair in pairs[1:]:
        total.add(pair)
    assert str(total) == sum_string


@pytest.mark.parametrize(
    "pairs_string, magnitude",
    [
        ("[[1,2],[[3,4],5]]", 143),
        ("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]", 1384),
        ("[[[[1,1],[2,2]],[3,3]],[4,4]]", 445),
        ("[[[[3,0],[5,3]],[4,4]],[5,5]]", 791),
        ("[[[[5,0],[7,4]],[5,5]],[6,6]]", 1137),
        ("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]", 3488),
    ],
)
def test_magnitude(pairs_string, magnitude):
    pair = Pair.from_string(pairs_string)
    assert pair.magnitude() == magnitude


def test_add_and_reduce():
    pair = Pair.from_string("[[[[4,3],4],4],[7,[[8,4],9]]]") + Pair.from_string("[1,1]")
    pair.fully_reduce()
    assert str(pair) == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"


def test_another_example():
    numbers = [
        "[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]",
        "[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]",
        "[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]",
        "[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]",
        "[7,[5,[[3,8],[1,4]]]]",
        "[[2,[2,2]],[8,[8,1]]]",
        "[2,9]",
        "[1,[[[9,3],9],[[9,0],[0,7]]]]",
        "[[[5,[7,4]],7],1]",
        "[[[[4,2],2],6],[8,7]]",
    ]
    pairs = digest_input(numbers)
    assert (
        str(reduce(lambda a, b: a + b, pairs))
        == "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]"
    )
