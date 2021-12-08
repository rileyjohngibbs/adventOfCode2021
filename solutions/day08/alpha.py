from dataclasses import dataclass
from itertools import product
import re

DIGIT_RENDERS = [
    frozenset("abcefg"),
    frozenset("cf"),
    frozenset("acdeg"),
    frozenset("acdfg"),
    frozenset("bcdf"),
    frozenset("abdfg"),
    frozenset("abdefg"),
    frozenset("acf"),
    frozenset("abcdefg"),
    frozenset("abcdfg"),
]
SIGNAL_CODES = "abcdefg"


@dataclass(frozen=True)
class Entry:
    signal_pattern: list[str]
    output_values: list[str]


def digest_input(input_lines: list[str]) -> list["Entry"]:
    return [
        Entry(
            *[
                group.split(" ")
                for group in re.match(r"(.*) \| (.*)", input_line).groups()
            ]
        )
        for input_line in input_lines
    ]


def part_one(entries: list["Entry"]) -> int:
    return sum(
        bool({1, 4, 7, 8} & get_candidate_digits(output_value))
        for entry in entries
        for output_value in entry.output_values
    )


def part_two(entries: list["Entry"]) -> int:
    output_value_sum = 0
    for entry in entries:
        solution: dict[str, int] = solve_signal_pattern(entry.signal_pattern)
        output_value_sum += int(
            "".join(str(solution[frozenset(value)]) for value in entry.output_values)
        )
    return output_value_sum


def solve_signal_pattern(signal_pattern: list[str]) -> dict[frozenset[str], int]:
    matrix: dict[str, set[str]] = {a: set(SIGNAL_CODES) for a in SIGNAL_CODES}
    for signal in signal_pattern:
        candidate_renders = get_candidate_renders(signal)
        uncommon_render_codes = set().union(*candidate_renders)
        for code in signal:
            matrix[code] &= uncommon_render_codes
        common_render_codes = set(SIGNAL_CODES).intersection(*candidate_renders)
        for code, render_codes in matrix.items():
            if code not in signal:
                render_codes -= common_render_codes

    inf_loop_watcher = 0
    while not all(len(render_codes) == 1 for render_codes in matrix.values()):
        for code, render_codes in matrix.items():
            if len(render_codes) == 1:
                for other_code, other_render_codes in matrix.items():
                    if other_code != code:
                        other_render_codes -= render_codes
            if len(render_codes) == 0:
                raise Exception(f"Unable to solve: no possible solutions remain for {code}")
        inf_loop_watcher += 1
        if inf_loop_watcher > 30:  # Probably could lower this threshold but it doesn't matter
            raise Exception("Unable to solbe: this is probably an infinite loop")

    solution = {}
    for signal in signal_pattern:
        meaning = frozenset(list(matrix[code])[0] for code in signal)
        solution[frozenset(signal)] = next(
            digit for digit, render in enumerate(DIGIT_RENDERS) if render == meaning
        )
    return solution


def get_candidate_digits(unknown_render: str) -> set[int]:
    return {
        digit
        for digit, render in enumerate(DIGIT_RENDERS)
        if len(render) == len(unknown_render)
    }


def get_candidate_renders(unknown_render: str) -> set[frozenset[str]]:
    return {render for render in DIGIT_RENDERS if len(render) == len(unknown_render)}
