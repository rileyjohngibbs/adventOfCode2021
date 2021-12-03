def digest_input(input_lines: list[str]) -> list[tuple[str, int]]:
    return [digest_line(input_line) for input_line in input_lines]


def digest_line(input_line: str) -> tuple[str, int]:
    action_str, value_str = input_line.split()
    return action_str, int(value_str)


def part_one(input_lines: list[tuple[str, int]]) -> int:
    horizontal = 0
    depth = 0
    for action_str, value in input_lines:
        if action_str == "forward":
            horizontal += value
        elif action_str == "up":
            depth -= value
        elif action_str == "down":
            depth += value
        else:
            raise ValueError(action_str)
    return horizontal * depth


def part_two(input_lines: list[tuple[str, int]]) -> int:
    horizontal, depth, aim = 0, 0, 0
    for action_str, value in input_lines:
        if action_str == "down":
            aim += value
        elif action_str == "up":
            aim -= value
        elif action_str == "forward":
            horizontal += value
            depth += aim * value
    return horizontal * depth
