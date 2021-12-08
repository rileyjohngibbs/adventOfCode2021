def part_one(input_lines: list[str]) -> int:
    gamma = int(get_most_common_bits(input_lines), 2)
    place_values = len(input_lines[0])
    epsilon = 2 ** place_values - 1 - gamma
    return gamma * epsilon


def part_two(input_lines: list[str]) -> int:
    oxygen = find_rating(input_lines, True)
    cotwo = find_rating(input_lines, False)
    return int(oxygen, 2) * int(cotwo, 2)


def find_rating(candidates: list[str], keep_most_common: bool, index: int = 0) -> str:
    if len(candidates) == 1:
        return candidates[0]
    zeros, ones = part_two_split(candidates, index)
    filtered_candidates = (
        ones if keep_most_common == (len(ones) >= len(zeros)) else zeros
    )
    return find_rating(filtered_candidates, keep_most_common, index + 1)


def get_most_common_bits(input_lines: list[str]) -> str:
    place_values = len(input_lines[0])
    bit_counts = [0] * place_values
    for input_line in input_lines:
        for i, bit in enumerate(input_line):
            if bit == "1":
                bit_counts[i] += 1
            else:
                bit_counts[i] -= 1
    most_common_bits = ["1" if count >= 0 else "0" for count in bit_counts]
    return "".join(most_common_bits)


def part_two_split(candidates: list[str], index: int) -> tuple[list[str], list[str]]:
    zeros, ones = [], []
    for candidate in candidates:
        if candidate[index] == "0":
            zeros.append(candidate)
        else:
            ones.append(candidate)
    return zeros, ones


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
