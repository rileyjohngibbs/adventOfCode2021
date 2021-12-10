from dataclasses import dataclass


def part_two(input_lines: list[str]) -> int:
    tree = Tree(0, {})
    for line in input_lines:
        leaf = tree
        for bit in line:
            leaf.count += 1
            leaf = leaf.bit_branches.setdefault(bit, Tree(0, {}))
        leaf.count += 1

    oxygen = ""
    leaf = tree
    while leaf.bit_branches:
        bit, leaf = max(leaf.bit_branches.items(), key=rating_key)
        oxygen += bit

    cotwo = ""
    leaf = tree
    while leaf.bit_branches:
        bit, leaf = min(leaf.bit_branches.items(), key=rating_key)
        cotwo += bit

    return int(oxygen, 2) * int(cotwo, 2)


@dataclass
class Tree:
    count: int
    bit_branches: dict[str, "Tree"]


def rating_key(key_value: tuple[str, Tree]):
    key, value = key_value
    return value.count, key == "1"


def test_rating_key():
    assert rating_key(("0", Tree(1, {}))) < rating_key(("1", Tree(1, {})))


def test_given_part_two():
    test_input = [
        "00100",
        "11110",
        "10110",
        "10111",
        "10101",
        "01111",
        "00111",
        "11100",
        "10000",
        "11001",
        "00010",
        "01010",
    ]
    assert part_two(test_input) == 230
