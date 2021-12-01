def digest_input(input_lines: list[str]) -> list[int]:
    return [int(line) for line in input_lines]


def part_one(input_lines: list[int]) -> int:
    return sum(
        input_lines[i] > input_lines[i - 1]
        for i in range(1, len(input_lines))
    )


def part_two(input_lines: list[int]) -> int:
    return sum(
        input_lines[i] > input_lines[i - 3]
        for i in range(3, len(input_lines))
    )
