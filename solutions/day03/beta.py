def part_two(input_lines: list[str]) -> int:
    tree = [0, {}]
    for line in input_lines:
        leaf = tree
        for bit in line:
            leaf[0] += 1
            leaf = leaf[1].setdefault(bit, [0, {}])
        leaf[0] += 1

    oxygen = ""
    leaf = tree
    while leaf[1]:
        bit, leaf = max(leaf[1].items(), key=rating_key)
        oxygen += bit

    cotwo = ""
    leaf = tree
    while leaf[1]:
        bit, leaf = min(leaf[1].items(), key=rating_key)
        cotwo += bit

    return int(oxygen, 2) * int(cotwo, 2)


def rating_key(key_value):
    key, value = key_value
    return value[0], key == "1"


def test_rating_key():
    assert rating_key(("0", [1, {}])) < rating_key(("1", [1, {}]))


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
