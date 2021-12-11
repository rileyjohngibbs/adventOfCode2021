from itertools import product


def digest_input(input_lines: list[str]) -> list[list[int]]:
    return [[int(x) for x in row] for row in input_lines]


def part_one(octopodes: list[list[int]]) -> int:
    octopodes_grid = OctopodesGrid(octopodes)
    flashes = 0
    for _ in range(100):
        octopodes_grid.increment_step()
        flashes += len(octopodes_grid.value_addresses[0])
    return flashes


def part_two(octopodes: list[list[int]]) -> int:
    octopodes_grid = OctopodesGrid(octopodes)
    steps = 0
    grid_size = octopodes_grid.dimensions[0] * octopodes_grid.dimensions[1]
    while len(octopodes_grid.value_addresses[0]) != grid_size:
        octopodes_grid.increment_step()
        steps += 1
    return steps


class OctopodesGrid:
    addresses: set[tuple[int, int]]
    dimensions: tuple[int, int]
    value_addresses: dict[int, set[tuple[int, int]]]

    def __init__(self, octopodes: list[list[int]]):
        self.dimensions = (len(octopodes), len(octopodes[0]))
        self.addresses = set(
            product(range(self.dimensions[0]), range(self.dimensions[1]))
        )
        self.value_addresses: dict[int, set[tuple[int, int]]] = {
            x: set() for x in range(10)
        }
        for ri, row in enumerate(octopodes):
            for ci, octopus in enumerate(row):
                self.value_addresses[octopus].add((ri, ci))

    def increment_step(self) -> None:
        self.value_addresses.update(
            {k + 1: v for k, v in self.value_addresses.items()} | {0: set()}
        )
        while self.value_addresses[10]:
            addresses_to_increment = [
                (r + dr, c + dc)
                for r, c in self.value_addresses[10]
                for dr in range(-1, 2)
                for dc in range(-1, 2)
                if (dr != 0 or dc != 0) and (r + dr, c + dc) in self.addresses
            ]
            self.value_addresses[0].update(self.value_addresses[10])
            self.value_addresses[10] = set()
            for address_to_increment in addresses_to_increment:
                self._charge_octopus_at(address_to_increment)
        self.value_addresses.pop(10, None)

    def _charge_octopus_at(self, address: tuple[int, int]) -> None:
        octo_value = next(
            (
                value
                for value, addresses_with_value in self.value_addresses.items()
                if 1 <= value <= 9 and address in addresses_with_value
            ),
            None,
        )
        if octo_value is not None:
            self.value_addresses[octo_value].remove(address)
            self.value_addresses[octo_value + 1].add(address)

    def render(self) -> str:
        print_grid = [
            ["." for _ in range(self.dimensions[1])] for _ in range(self.dimensions[0])
        ]
        for value, addresses in self.value_addresses.items():
            for address in addresses:
                print_grid[address[0]][address[1]] = value
        return "\n".join("".join(str(octo) for octo in row) for row in print_grid)


PART_ONE_TEST_INPUT = [
    "5483143223",
    "2745854711",
    "5264556173",
    "6141336146",
    "6357385478",
    "4167524645",
    "2176841721",
    "6882881134",
    "4846848554",
    "5283751526",
]


def test_part_one():
    assert part_one(digest_input(PART_ONE_TEST_INPUT)) == 1656


def test_part_one_step_two():
    octopodes_grid = OctopodesGrid(digest_input(PART_ONE_TEST_INPUT))
    assert sum(len(a) for a in octopodes_grid.value_addresses.values()) == 100
    print(octopodes_grid.render())
    print()
    octopodes_grid.increment_step()
    print(octopodes_grid.render())
    print()
    octopodes_grid.increment_step()
    print(octopodes_grid.render())
    # Uncomment to see grid at each step
    # assert False


def test_part_one_small():
    input_ = [
        "11111",
        "19991",
        "19191",
        "19991",
        "11111",
    ]
    octopodes = digest_input(input_)
    octopodes_grid = OctopodesGrid(octopodes)
    octopodes_grid.increment_step()
    value_addresses = octopodes_grid.value_addresses
    assert value_addresses[0] == {(ri, ci) for ri in range(1, 4) for ci in range(1, 4)}
    assert value_addresses[1] == set()
    assert value_addresses[2] == set()
    assert value_addresses[3] == {(0, 0), (0, 4), (4, 0), (4, 4)}
    assert value_addresses[4] == {
        (0, 1),
        (0, 3),
        (1, 0),
        (1, 4),
        (3, 0),
        (3, 4),
        (4, 1),
        (4, 3),
    }
    assert value_addresses[5] == {(0, 2), (2, 0), (2, 4), (4, 2)}
