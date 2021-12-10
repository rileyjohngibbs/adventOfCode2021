from typing import Optional


def digest_input(input_lines: list[str]) -> list[list[int]]:
    return [
        [int(digit) for digit in row]
        for row in input_lines
    ]


def part_one(grid: list[list[int]]) -> int:
    risk_level_sum = 0
    for ri, row in enumerate(grid):
        for ci, value in enumerate(row):
            is_minimum = (
                (ri == 0 or grid[ri - 1][ci] > value)
                and (ri == len(grid) - 1 or grid[ri + 1][ci] > value)
                and (ci == 0 or grid[ri][ci - 1] > value)
                and (ci == len(row) - 1 or grid[ri][ci + 1] > value)
            )
            if is_minimum:
                risk_level_sum += value + 1
    return risk_level_sum


def part_two(grid_values: list[list[int]]) -> int:
    grid = Grid(grid_values)
    basin_sizes: list[int] = []
    basined_values: set[tuple[int, int, int]] = set()
    for ri, row in enumerate(grid_values):
        for ci, value in enumerate(row):
            is_minimum = (
                (ri == 0 or grid_values[ri - 1][ci] > value)
                and (ri == len(grid_values) - 1 or grid_values[ri + 1][ci] > value)
                and (ci == 0 or grid_values[ri][ci - 1] > value)
                and (ci == len(row) - 1 or grid_values[ri][ci + 1] > value)
            )
            if is_minimum and (ri, ci, value) not in basined_values:
                basin: set[tuple[int, int, int]] = {(ri, ci, value)}
                frontier = {(ri, ci, value)}
                basined_values.add((ri, ci, value))
                while frontier:
                    frontier = {
                        neighbor
                        for ri, ci, _ in frontier
                        for neighbor in grid.neighbors(ri, ci)
                        if neighbor[2] != 9
                        and neighbor not in basin
                    }
                    basin |= frontier
                    basined_values |= frontier
                basin_sizes.append(len(basin))
    largest_basins = sorted(basin_sizes)[-3:]
    basin_product = 1
    for basin_size in largest_basins:
        basin_product *= basin_size
    return basin_product


class Grid:
    def __init__(self, grid_values: list[list[int]]):
        self.grid_values = grid_values

    def left(self, row_index: int, column_index: int) -> Optional[tuple[int, int, int]]:
        """Returns row, column, value"""
        if column_index == 0:
            return None
        return (row_index, column_index - 1, self.grid_values[row_index][column_index - 1])

    def right(self, row_index: int, column_index: int) -> Optional[tuple[int, int, int]]:
        """Returns row, column, value"""
        if column_index == len(self.grid_values[row_index]) - 1:
            return None
        return (row_index, column_index + 1, self.grid_values[row_index][column_index + 1])

    def up(self, row_index: int, column_index: int) -> Optional[tuple[int, int, int]]:
        """Returns row, column, value"""
        if row_index == 0:
            return None
        return (row_index - 1, column_index, self.grid_values[row_index - 1][column_index])

    def down(self, row_index: int, column_index: int) -> Optional[tuple[int, int, int]]:
        """Returns row, column, value"""
        if row_index == len(self.grid_values) - 1:
            return None
        return (row_index + 1, column_index, self.grid_values[row_index + 1][column_index])

    def neighbors(self, row_index: int, column_index: int) -> set[tuple[int, int, int]]:
        return {
            neighbor
            for method in (self.left, self.right, self.up, self.down)
            if (neighbor := method(row_index, column_index)) is not None
        }
