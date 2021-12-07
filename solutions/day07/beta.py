from functools import partial
from typing import Callable


def digest_input(input_lines: list[str]) -> list[int]:
    return [int(n) for n in input_lines[0].split(",")]


def part_one(positions: list[int]) -> int:
    return find_minimum(
        min(positions), max(positions), partial(total_fuel_one, positions)
    )


def total_fuel_one(positions: list[int], destination: int) -> int:
    return sum(abs(destination - position) for position in positions)


def part_two(positions: list[int]) -> int:
    return find_minimum(
        min(positions), max(positions), partial(total_fuel_two, positions)
    )


def total_fuel_two(positions: list[int], destination: int) -> int:
    return sum(sum_range(abs(position - destination)) for position in positions)


def sum_range(upper_end: int) -> int:
    return (upper_end ** 2 + upper_end) // 2


def find_minimum(left: int, right: int, key: Callable[[int], int]) -> int:
    guess = (left + right) // 2
    guess_cost = key(guess)
    step_size = (right - guess) // 2
    while step_size >= 1:
        new_guesses = [
            (guess + delta, key(guess + delta)) for delta in (-step_size, step_size)
        ]
        best_guess, best_guess_cost = next(
            filter(lambda ng: ng[1] < guess_cost, new_guesses), (guess, guess_cost)
        )
        if best_guess != guess:
            guess = best_guess
            guess_cost = best_guess_cost
        else:
            step_size = step_size // 2
    return min(key(g) for g in (guess - 1, guess, guess + 1))


def test_part_one():
    input_lines = ["16,1,2,0,4,2,7,1,2,14"]
    positions = digest_input(input_lines)
    assert part_one(positions) == 37


def test_part_two():
    input_lines = ["16,1,2,0,4,2,7,1,2,14"]
    positions = digest_input(input_lines)
    assert part_two(positions) == 168
