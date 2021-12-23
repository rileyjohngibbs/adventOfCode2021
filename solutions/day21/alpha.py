from dataclasses import dataclass

import pytest


def digest_input(input_lines: list[str]) -> tuple[int, int]:
    return (
        int(input_lines[0].rsplit(" ", 1)[-1]),
        int(input_lines[1].rsplit(" ", 1)[-1]),
    )


def part_one(starts: tuple[int, int]) -> int:
    p1 = Player(starts[0])
    p2 = Player(starts[1])
    p1_turn = True
    die = 1
    while p1.score < 1000 and p2.score < 1000:
        roll = (3 * die + 3) % 10
        player = p1 if p1_turn else p2
        player.move_and_score(roll)
        die += 3
        p1_turn = not p1_turn
    loser = p1 if p1.score < 1000 else p2
    return loser.score * (die - 1)


def part_two(starts: tuple[int, int]) -> int:
    roll_counts = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}
    universe_counts = {GameState(0, 0, starts[0], starts[1], True): 1}
    p1wins, p2wins = 0, 0
    while any(not gs.game_over() for gs in universe_counts):
        game_state = next(gs for gs in universe_counts)
        for other_game_state in universe_counts:
            if other_game_state.can_reach(game_state):
                game_state = other_game_state
        count = universe_counts.pop(game_state)
        for move, factor in roll_counts.items():
            new_state = game_state.state_after_move(move)
            if new_state.game_over():
                if new_state.p1score >= 21:
                    p1wins += count * factor
                else:
                    p2wins += count * factor
            else:
                universe_counts[new_state] = (
                    universe_counts.get(new_state, 0) + count * factor
                )
    return max(p1wins, p2wins)


@dataclass(frozen=True)
class GameState:
    p1score: int
    p2score: int
    p1position: int
    p2position: int
    p1turn: bool

    def state_after_move(self, move: int) -> "GameState":
        if self.p1turn:
            p1position = (self.p1position + move) % 10
            p1score = self.p1score + (p1position or 10)
            p2position = self.p2position
            p2score = self.p2score
        else:
            p2position = (self.p2position + move) % 10
            p2score = self.p2score + (p2position or 10)
            p1position = self.p1position
            p1score = self.p1score
        return GameState(p1score, p2score, p1position, p2position, not self.p1turn)

    def game_over(self) -> bool:
        return self.p1score >= 21 or self.p2score >= 21

    def can_reach(self, other: "GameState") -> bool:
        if self.game_over():
            return False
        return (
            self.p1turn
            and not other.p1turn
            and self.p1score <= other.p1score - 3
            and self.p2score <= other.p2score
            or self.p1turn == other.p1turn
            and self.p1score <= other.p1score - 3
            and self.p2score <= other.p2score - 3
            or not self.p1turn
            and other.p1turn
            and self.p1score <= other.p1score
            and self.p2score <= other.p2score - 3
        )


class Player:
    _position: int
    score: int

    def __init__(self, position: int):
        self._position = position
        self.score = 0

    def move_and_score(self, move: int):
        self._position = (self._position + move) % 10
        self.score += self.position

    @property
    def position(self) -> int:
        return self._position if self._position else 10


def test_part_one():
    assert part_one((4, 8)) == 739785


def test_part_two():
    assert part_two((4, 8)) == 444356092776315


@pytest.mark.parametrize(
    "a, b, reach",
    [
        (GameState(0, 0, 1, 1, True), GameState(10, 10, 1, 1, True), True),
    ],
)
def test_can_reach(a, b, reach):
    assert a.can_reach(b) == reach
