from dataclasses import dataclass


class BingoBoard:
    SIZE = 5

    @property
    def wins(self) -> tuple[tuple[int, ...], ...]:
        return tuple(
            tuple(range(x * self.SIZE, x * self.SIZE + self.SIZE))
            for x in range(self.SIZE)
        ) + tuple(
            tuple(range(x, self.SIZE * self.SIZE, self.SIZE)) for x in range(self.SIZE)
        )

    squares: list["BingoSquare"]
    reverse_lookup: dict[int, "BingoSquare"]

    def __init__(self, numbers: list[int]):
        self.squares = [BingoSquare(False, number) for number in numbers]
        self.reverse_lookup = {number: square for square, number in enumerate(numbers)}

    @property
    def winning_board(self):
        return any(all(self.squares[position] for position in win) for win in self.wins)

    def mark(self, number: int) -> None:
        square = self.reverse_lookup.get(number)
        if square is not None:
            self.squares[square].marked = True

    @property
    def score(self) -> int:
        return sum(square.number for square in self.squares if not square)


@dataclass
class BingoSquare:
    marked: bool
    number: int

    def __bool__(self):
        return self.marked


def digest_input(input_lines: list[str]) -> tuple[list[int], list["BingoBoard"]]:
    calls = [int(x) for x in input_lines[0].split(",")]
    board_lines = input_lines[1:]
    row = 0
    boards = []
    while row < len(board_lines):
        numbers = [
            int(number)
            for row in range(row + 1, row + 1 + BingoBoard.SIZE)
            for number in board_lines[row].split()
        ]
        boards.append(BingoBoard(numbers))
        row += BingoBoard.SIZE + 1
    return calls, boards


def part_one(game: tuple[list[int], list["BingoBoard"]]) -> int:
    calls, boards = game
    for call in calls:
        for board in boards:
            board.mark(call)
        winning_board = next((b for b in boards if b.winning_board), None)
        if winning_board is not None:
            break
    score = winning_board.score * call
    return score


def part_two(game: tuple[list[int], list["BingoBoard"]]) -> int:
    calls, boards = game
    for call in calls:
        for board in boards:
            board.mark(call)
        if len(boards) > 1:
            boards = [b for b in boards if not b.winning_board]
        else:
            if boards[0].winning_board:
                break
    losing_board = boards[0]
    score = losing_board.score * call
    return score
