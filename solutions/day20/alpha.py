import pytest


def digest_input(input_lines: list[str]) -> "Grid":
    algorithm = tuple(c == "#" for c in input_lines[0])
    grid = [[c == "#" for c in row] for row in input_lines[2:]]
    return Grid(algorithm, grid)


class Grid:
    def __init__(self, algorithm: tuple[bool, ...], grid_values: list[list[bool]]):
        self.grid_dict = {
            (x, y): value
            for y, row in enumerate(grid_values)
            for x, value in enumerate(row)
        }
        self.size = (len(grid_values[0]), len(grid_values))
        self.algorithm = algorithm
        self.default = False

    def iterate(self) -> None:
        new_dict: dict[tuple[int, int], bool] = {}
        self.grid_dict.update(
            {(i - 1, -1): self.default for i in range(self.size[0] + 2)}
            | {(i - 1, self.size[1]): self.default for i in range(self.size[0] + 2)}
            | {(-1, j - 1): self.default for j in range(self.size[1] + 2)}
            | {(self.size[0], j - 1): self.default for j in range(self.size[1] + 2)}
        )
        for address, value in self.grid_dict.items():
            x, y = address
            neighborhood = (
                self.grid_dict.get((x + dx, y + dy), self.default)
                for dy in range(-1, 2)
                for dx in range(-1, 2)
            )
            algorithm_index = int("".join(map(str, map(int, neighborhood))), 2)
            new_value = self.algorithm[algorithm_index]
            new_dict[(x + 1, y + 1)] = new_value
        self.size = (self.size[0] + 2, self.size[1] + 2)
        self.grid_dict = new_dict
        self.default = self.algorithm[1 - 2 * self.default]

    def print(self) -> str:
        print_grid: list[list[str]] = [
            ["."] * self.size[0] for _ in range(self.size[1])
        ]
        for address, value in self.grid_dict.items():
            print_grid[address[1]][address[0]] = "#" if value else "."
        return "\n".join("".join(row) for row in print_grid)


def part_one(grid: "Grid") -> int:
    grid.iterate()
    grid.iterate()
    return sum(grid.grid_dict.values())


def part_two(grid: "Grid") -> int:
    for _ in range(50):
        grid.iterate()
    return sum(grid.grid_dict.values())


@pytest.fixture
def example_input():
    return [
        (
            "..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##"
            "#..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###"
            ".######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#."
            ".#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#....."
            ".#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.."
            "...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#....."
            "..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#"
        ),
        "",
        "#..#.",
        "#....",
        "##..#",
        "..#..",
        "..###",
    ]


def test_part_one(example_input):
    assert part_one(digest_input(example_input)) == 35


def test_part_two(example_input):
    assert part_two(digest_input(example_input)) == 3351
