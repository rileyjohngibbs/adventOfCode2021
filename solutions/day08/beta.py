from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Display:
    signal_pattern: list[set[str]]
    output_values: list[set[str]]


def digest_input(input_lines: list[str]) -> list["Display"]:
    return [
        Display(
            *[
                [set(x) for x in group.split(" ")]
                for group in re.match(r"(.*) \| (.*)", input_line).groups()
            ]
        )
        for input_line in input_lines
    ]


def part_two(displays: list["Display"]) -> int:
    return sum(solve_display(display) for display in displays)


def solve_display(display: Display) -> int:
    one = next(pattern for pattern in display.signal_pattern if len(pattern) == 2)
    four_arm = (
        next(pattern for pattern in display.signal_pattern if len(pattern) == 4) - one
    )

    solved_output = 0
    for output_value in display.output_values:
        if len(output_value) == 2:
            digit = 1
        elif len(output_value) == 3:
            digit = 7
        elif len(output_value) == 4:
            digit = 4
        elif len(output_value) == 5:
            # 2, 3, 5
            if one & output_value == one:
                digit = 3
            elif four_arm & output_value == four_arm:
                digit = 5
            else:
                digit = 2
        elif len(output_value) == 6:
            # 6, 9, 0
            if one & output_value != one:
                digit = 6
            elif four_arm & output_value != four_arm:
                digit = 0
            else:
                digit = 9
        elif len(output_value) == 7:
            digit = 8
        solved_output = 10 * solved_output + digit
    return solved_output
