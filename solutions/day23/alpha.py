from copy import deepcopy
from dataclasses import dataclass
import re
from typing import Optional

import pytest

from solutions.common.ordered_list import OrderedList


def digest_input(input_lines: list[str]) -> list[tuple["Pod", "Position"]]:
    zeroth_match = re.match(r"###(.)#(.)#(.)#(.)###", input_lines[2])
    if zeroth_match is None:
        raise ValueError()
    first_match = re.match(r"  #(.)#(.)#(.)#(.)#", input_lines[3])
    if first_match is None:
        raise ValueError()
    pod_positions = [
        (Pod(f), Position(i, 0)) for i, f in enumerate(zeroth_match.groups())
    ] + [(Pod(f), Position(i, -1)) for i, f in enumerate(first_match.groups())]
    return pod_positions


def part_one(pod_positions: list[tuple["Pod", "Position"]]) -> int:
    puzzle = Puzzle(pod_positions)
    return a_star_puzzle(puzzle)


def part_two(pod_positions: list[tuple["Pod", "Position"]]) -> int:
    puzzle = Puzzle(pod_positions, room_size=4)
    return a_star_puzzle(puzzle)


def a_star_puzzle(puzzle: "Puzzle") -> int:
    visited: dict[str, int] = {}
    frontier: OrderedList[tuple[Puzzle, int]] = OrderedList(
        [(puzzle, 0)], lambda i: heuristic(i[0]) + i[1]
    )
    solution: Optional[tuple[Puzzle, int]] = None
    while solution is None and frontier:
        candidate, cost = frontier.pop(0)
        if candidate.is_solved():
            solution = candidate, cost
            break
        candidate_hash = "".join(
            "".join(map(str, room)) for room in candidate.rooms
        ) + "".join(map(str, candidate.hallway))
        if candidate_hash in visited and cost >= visited[candidate_hash]:
            continue
        visited[candidate_hash] = cost
        moves = candidate.legal_moves()
        for move in moves:
            new_puzzle = candidate.copy()
            cost_delta = new_puzzle.execute_move(move)
            frontier.insert((new_puzzle, cost + cost_delta))
    if solution is not None:
        return solution[1]
    else:
        raise StopIteration()


class Puzzle:
    """
    +-----------+
    |01234567890|
    +-+A|B|C|D+-+  0
      |A|B|C|D|    1
      +-+-+-+-+
    """

    ROOM_FLAVORS = ["A", "B", "C", "D"]
    ROOM_EXITS = [2, 4, 6, 8]
    HALL_INDEX = 4

    def __init__(
        self, pod_inits: list[tuple["Pod", "Position"]], room_size: int = 2
    ) -> None:
        self.room_size = room_size
        self.rooms: list[list[Optional[Pod]]] = [
            [None] * self.room_size,
            [None] * self.room_size,
            [None] * self.room_size,
            [None] * self.room_size,
        ]
        self.hallway: list[Optional[Pod]] = [None] * 11  # Eleven spots in the hallway
        for pod, position in pod_inits:
            self.get_room(position.room_index)[position.slot] = pod
        if self.room_size == 4:
            self.rooms[0][1:3] = [Pod("D"), Pod("D")]
            self.rooms[1][1:3] = [Pod("C"), Pod("B")]
            self.rooms[2][1:3] = [Pod("B"), Pod("A")]
            self.rooms[3][1:3] = [Pod("A"), Pod("C")]

    def is_solved(self) -> bool:
        return all(
            p is not None and p.flavor == flavor
            for i, flavor in enumerate("ABCD")
            for p in self.rooms[i]
        )

    def copy(self) -> "Puzzle":
        new_puzzle = Puzzle([])
        new_puzzle.rooms = [
            [p if p is None else p.copy() for p in room] for room in self.rooms
        ]
        new_puzzle.hallway = [p if p is None else p.copy() for p in self.hallway]
        new_puzzle.room_size = self.room_size
        return new_puzzle

    def legal_moves(self) -> list["Move"]:
        moves: list[Move] = []
        for room_number in self.unsolved_rooms():
            room = self.rooms[room_number]
            room_exit = self.ROOM_EXITS[room_number]
            pod_index = self.room_size - sum(p is not None for p in room)
            if pod_index != self.room_size and self.hallway[room_exit] is None:
                start = Position(room_number, pod_index)
                pod = room[pod_index]
                if pod is None:
                    raise TypeError()
                solution_room_number = self.ROOM_FLAVORS.index(pod.flavor)
                solution_exit = self.ROOM_EXITS[solution_room_number]
                solution_open = all(
                    occupant is None or occupant.flavor == pod.flavor
                    for occupant in self.rooms[solution_room_number]
                )

                left = room_exit
                while left > 0 and self.hallway[left - 1] is None:
                    left -= 1
                if solution_open and left <= solution_exit < room_exit:
                    solution_room_slot = (
                        self.room_size
                        - 1
                        - sum(p is not None for p in self.rooms[solution_room_number])
                    )
                    left_ends = [Position(solution_room_number, solution_room_slot)]
                else:
                    left_ends = [
                        Position(self.HALL_INDEX, p) for p in range(left, room_exit)
                    ]
                for left_end in left_ends:
                    moves.append(Move(start, left_end))

                right = room_exit
                while right < 10 and self.hallway[right + 1] is None:
                    right += 1
                if solution_open and right >= solution_exit > room_exit:
                    solution_room_slot = (
                        self.room_size
                        - 1
                        - sum(p is not None for p in self.rooms[solution_room_number])
                    )
                    right_ends = [Position(solution_room_number, solution_room_slot)]
                else:
                    right_ends = [
                        Position(self.HALL_INDEX, p)
                        for p in range(room_exit + 1, right + 1)
                    ]
                for right_end in right_ends:
                    moves.append(Move(start, right_end))

        for hall_index, pod in enumerate(self.hallway):
            if pod is None:
                continue
            solution_room_number = self.ROOM_FLAVORS.index(pod.flavor)
            solution_open = all(
                occupant is None or occupant.flavor == pod.flavor
                for occupant in self.rooms[solution_room_number]
            )
            if not solution_open:
                continue
            solution_exit = self.ROOM_EXITS[solution_room_number]
            if solution_exit <= hall_index:
                path_clear = all(
                    self.hallway[i] is None for i in range(solution_exit, hall_index)
                )
            else:
                path_clear = all(
                    self.hallway[i] is None
                    for i in range(hall_index + 1, solution_exit + 1)
                )
            if path_clear:
                start = Position(4, hall_index)
                slots_filled = sum(
                    p is not None for p in self.rooms[solution_room_number]
                )
                solution_room_slot = self.room_size - 1 - slots_filled
                end = Position(solution_room_number, solution_room_slot)
                moves.append(Move(start, end))

        return moves

    def unsolved_rooms(self) -> list[int]:
        room_numbers: list[int] = []
        for number, flavor in enumerate("ABCD"):
            in_stack = False
            for slot, pod in enumerate(self.rooms[number]):
                if not in_stack and pod is not None:
                    in_stack = True
                if in_stack:
                    if pod is None or pod.flavor != flavor:
                        room_numbers.append(number)
                        break
        return room_numbers

    def execute_move(self, move: "Move") -> int:
        """Mutates self and returns the cost of the move"""
        pod = self.get_room(move.start.room_index)[move.start.slot]
        if pod is None:
            raise ValueError()
        self.get_room(move.start.room_index)[move.start.slot] = None
        self.get_room(move.end.room_index)[move.end.slot] = pod
        return pod.move_cost * self.distance(move)

    @classmethod
    def distance(cls, move: "Move") -> int:
        steps = 0
        if move.start.room_index == 4:
            hall_start = move.start.slot
        else:
            hall_start = cls.ROOM_EXITS[move.start.room_index]
            steps += move.start.slot + 1
        if move.end.room_index == 4:
            hall_end = move.end.slot
        else:
            hall_end = cls.ROOM_EXITS[move.end.room_index]
            steps += move.end.slot + 1
        steps += abs(hall_end - hall_start)
        return steps

    def get_room(self, room_index: int) -> list[Optional["Pod"]]:
        if room_index == 4:
            return self.hallway
        else:
            return self.rooms[room_index]


def heuristic(puzzle: "Puzzle") -> int:
    total = 0
    for room_number, room in enumerate(puzzle.rooms):
        for slot, pod in enumerate(room):
            if pod is None:
                continue
            solution_room_number = puzzle.ROOM_FLAVORS.index(pod.flavor)
            hall_distance = abs(room_number - solution_room_number + slot) * 2
            total += (hall_distance + slot + 2) * pod.move_cost
    return total


@dataclass
class Move:
    start: "Position"
    end: "Position"


@dataclass
class Position:
    room_index: int
    slot: int


class Pod:
    FLAVOR_COSTS = {"A": 1, "B": 10, "C": 100, "D": 1000}

    def __init__(self, flavor: str) -> None:
        if not flavor.upper() in "ABCD":
            raise ValueError("Flavor must be one of A, B, C, or D")
        self.flavor = flavor.upper()

    def __repr__(self) -> str:
        return f"Pod<{self.flavor}>"

    @property
    def move_cost(self) -> int:
        return self.FLAVOR_COSTS[self.flavor]

    def copy(self) -> "Pod":
        return Pod(self.flavor)


def test_legal_moves_one_solvable_pawn():
    puzzle = Puzzle([(Pod("A"), Position(1, 1))])
    moves = puzzle.legal_moves()
    assert len(moves) == 7


def test_legal_moves_stacked_pawns_unsolvable():
    puzzle = Puzzle([(Pod("A"), Position(0, 0)), (Pod("B"), Position(0, 1))])
    moves = puzzle.legal_moves()
    assert len(moves) == 10
    assert all(move.start == Position(0, 0) for move in moves)


def test_legal_moves_separate_pawns_unsolvable():
    puzzle = Puzzle([(Pod("A"), Position(1, 1)), (Pod("B"), Position(0, 1))])
    moves = puzzle.legal_moves()
    assert len(moves) == 20
    assert all(move.start in (Position(0, 1), Position(1, 1)) for move in moves)
    assert all(move.end.room_index == Puzzle.HALL_INDEX for move in moves)


def test_legal_moves_hallway():
    puzzle = Puzzle([(Pod("A"), Position(4, 0))])
    moves = puzzle.legal_moves()
    assert len(moves) == 1
    assert moves[0].start == Position(4, 0)
    assert moves[0].end == Position(0, 1)


@pytest.mark.parametrize(
    "move, distance",
    [
        (Move(Position(4, 0), Position(4, 10)), 10),
        (Move(Position(3, 1), Position(0, 1)), 10),
    ],
)
def test_distance(move, distance):
    assert Puzzle.distance(move) == distance


def test_is_solved():
    puzzle = Puzzle(
        [
            (Pod("A"), Position(0, 0)),
            (Pod("A"), Position(0, 1)),
            (Pod("B"), Position(1, 0)),
            (Pod("B"), Position(1, 1)),
            (Pod("C"), Position(2, 0)),
            (Pod("C"), Position(2, 1)),
            (Pod("D"), Position(3, 0)),
            (Pod("D"), Position(3, 1)),
        ]
    )
    assert puzzle.is_solved()


def test_example_last():
    puzzle = Puzzle(
        [
            (Pod(f), Position(r, i))
            for f, r, i in [
                ("A", 4, 9),
                ("A", 0, 1),
                ("B", 1, 0),
                ("B", 1, 1),
                ("C", 2, 0),
                ("C", 2, 1),
                ("D", 3, 0),
                ("D", 3, 1),
            ]
        ]
    )
    assert a_star_puzzle(puzzle) == 8


def test_example():
    example = [
        "#############",
        "#...........#",
        "###B#C#B#D###",
        "  #A#D#C#A#",
        "  #########",
    ]
    assert part_one(digest_input(example)) == 12521


def test_part_two_example():
    example = [
        "#############",
        "#...........#",
        "###B#C#B#D###",
        "  #A#D#C#A#",
        "  #########",
    ]
    assert part_two(digest_input(example)) == 44169


def test_legal_moves_hall_to_solve_four_size():
    puzzle = Puzzle(
        [(Pod("A"), Position(0, 3)), (Pod("A"), Position(4, 0))], room_size=4
    )
    for room in puzzle.rooms:
        room[1:3] = [None, None]
    moves = puzzle.legal_moves()
    assert len(moves) == 1
    assert moves[0].end.slot == 2
