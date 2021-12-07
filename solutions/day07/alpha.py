def digest_input(input_lines: list[str]) -> list[int]:
    return [int(n) for n in input_lines[0].split(",")]


def part_one(positions: list[int]) -> int:
    median = sorted(positions)[(len(positions) - 1) // 2]
    return sum(abs(position - median) for position in positions)


def part_two(positions: list[int]) -> int:
    mean = sum(positions) / len(positions)
    # Sometimes we round up, sometimes down, but why inconsistent?
    candidates = (int(mean), int(mean + 0.5))
    return min(
        total_fuel_two(positions, candidate_mean) for candidate_mean in candidates
    )


def total_fuel_two(positions: list[int], destination: int) -> int:
    return sum(sum_range(abs(position - destination)) for position in positions)


def sum_range(upper_end: int) -> int:
    return (upper_end ** 2 + upper_end) // 2


def test_part_one():
    input_lines = ["16,1,2,0,4,2,7,1,2,14"]
    positions = digest_input(input_lines)
    assert part_one(positions) == 37


def test_part_two():
    input_lines = ["16,1,2,0,4,2,7,1,2,14"]
    positions = digest_input(input_lines)
    assert part_two(positions) == 168
