GESTATION_DAYS = 7
MATURATION_DAYS = 2

PART_ONE_DAYS = 80
PART_TWO_DAYS = 256


def digest_input(input_lines: list[str]) -> dict[int, int]:
    counts: dict[int, int] = {}
    for value in input_lines[0].split(","):
        counts[int(value)] = counts.get(int(value), 0) + 1
    return counts


def part_one(counts: dict[int, int]) -> int:
    return generate_fish(counts, PART_ONE_DAYS)


def part_two(counts: dict[int, int]) -> int:
    return generate_fish(counts, PART_TWO_DAYS)


def generate_fish(counts: dict[int, int], days_to_iterate: int) -> int:
    for day in range(days_to_iterate):
        new_counts: dict[int, int] = {}
        for gestation, count in counts.items():
            if gestation == 0:
                new_counts[GESTATION_DAYS - 1] = (
                    new_counts.get(GESTATION_DAYS - 1, 0) + count
                )
                new_counts[GESTATION_DAYS + MATURATION_DAYS - 1] = count
            else:
                new_counts[gestation - 1] = new_counts.get(gestation - 1, 0) + count
        counts = new_counts
    return sum(counts.values())


def test_part_one():
    test_input = {1: 1, 2: 1, 3: 2, 4: 1}
    assert part_one(test_input) == 5934


def test_part_two():
    test_input = {1: 1, 2: 1, 3: 2, 4: 1}
    assert part_two(test_input) == 26984457539
