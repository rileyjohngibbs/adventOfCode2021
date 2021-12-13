from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Display:
    signal_pattern: list[set[str]]
    output_values: list[set[str]]


def digest_input(input_lines: list[str]) -> list["Display"]:
    return [
        Display(*[[set(x) for x in group.split(" ")] for group in match.groups()])
        for input_line in input_lines
        if (match := re.match(r"(.*) \| (.*)", input_line)) is not None
    ]


def part_two(displays: list["Display"]) -> int:
    return sum(solve_display(display) for display in displays)


def solve_display(display: Display) -> int:
    one = next(pattern for pattern in display.signal_pattern if len(pattern) == 2)
    four_arm = (
        next(pattern for pattern in display.signal_pattern if len(pattern) == 4) - one
    )
    resolver = DigitResolver(one, four_arm)

    solved_output = 0
    for output_value in display.output_values:
        digit = resolver.resolve(output_value)
        solved_output = 10 * solved_output + digit
    return solved_output


class DigitResolver:
    """
    Uses the pattern for the digit 1 and the "arm" of the digit 4 to solve any other
    signal pattern.

    The "arm" of the digit 4 is the two signals in 4 that are not in 1.
    """

    def __init__(self, one: set[str], four_arm: set[str]):
        self.one = one
        self.four_arm = four_arm

    def resolve(self, pattern: set[str]) -> int:
        if len(pattern) == 2:
            digit = 1
        elif len(pattern) == 3:
            digit = 7
        elif len(pattern) == 4:
            digit = 4
        elif len(pattern) == 5:
            # 2, 3, 5
            if self.one & pattern == self.one:
                digit = 3
            elif self.four_arm & pattern == self.four_arm:
                digit = 5
            else:
                digit = 2
        elif len(pattern) == 6:
            # 6, 9, 0
            if self.one & pattern != self.one:
                digit = 6
            elif self.four_arm & pattern != self.four_arm:
                digit = 0
            else:
                digit = 9
        elif len(pattern) == 7:
            digit = 8
        return digit
