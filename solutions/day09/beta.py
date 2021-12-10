from functools import reduce
from itertools import product


def digest_input(input_lines: list[str]) -> list[list[int]]:
    return [[int(digit) for digit in row] for row in input_lines]


def part_two(grid: list[list[int]]) -> int:
    unvisited_addresses = set(product(range(len(grid)), range(len(grid[0]))))
    frontier: set[tuple[int, int]] = set()
    basins: list[set[tuple[int, int]]] = []
    current_basin: set[tuple[int, int]] = set()
    basins.append(current_basin)
    while unvisited_addresses:
        while not frontier and unvisited_addresses:
            if current_basin:
                current_basin = set()
                basins.append(current_basin)
            seed = unvisited_addresses.pop()
            if grid[seed[0]][seed[1]] != 9:
                unvisited_addresses.add(seed)
                frontier = {seed}
        if not frontier:
            continue
        candidate = frontier.pop()
        if (
            candidate not in unvisited_addresses
            or grid[candidate[0]][candidate[1]] == 9
        ):
            continue
        current_basin.add(candidate)
        unvisited_addresses.remove(candidate)
        frontier.update(
            {
                (candidate[0], candidate[1] - 1),
                (candidate[0], candidate[1] + 1),
                (candidate[0] - 1, candidate[1]),
                (candidate[0] + 1, candidate[1]),
            }
        )
    top_three = sorted(list(map(len, basins)))[-3:]
    return reduce(lambda a, b: a * b, top_three)
