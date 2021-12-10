from enum import Enum
from functools import reduce

PART_ONE_SCORE_MAPPING = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}
PART_TWO_SCORE_MAPPING = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


def part_one(input_lines: list[str]) -> int:
    score = 0
    for input_line in input_lines:
        chunks = [Chunk(input_line[0])]
        for character in input_line[1:]:
            result = chunks[-1].read_next(character)
            if result is ParseResult.NEW_OPEN:
                chunks.append(Chunk(character))
            elif result is ParseResult.CLOSE:
                chunks.pop()
            else:
                score += PART_ONE_SCORE_MAPPING[character]
                break
    return score


def part_two(input_lines: list[str]) -> int:
    scores: list[int] = []
    for input_line in input_lines:
        chunks = [Chunk(input_line[0])]
        chunks = [Chunk(input_line[0])]
        for character in input_line[1:]:
            result = chunks[-1].read_next(character) if chunks else ParseResult.NEW_OPEN
            if result is ParseResult.NEW_OPEN:
                chunks.append(Chunk(character))
            elif result is ParseResult.CLOSE:
                chunks.pop()
            else:
                break
        else:
            scores.append(
                reduce(
                    lambda a, b: 5 * a + PART_TWO_SCORE_MAPPING[b.closer],
                    chunks[::-1],
                    0,
                )
            )
    return sorted(scores)[len(scores) // 2]


class ParseResult(Enum):
    NEW_OPEN = 0
    CLOSE = 1
    ILLEGAL = 2


class Chunk:

    BRACKETS = {
        "(": ")",
        "[": "]",
        "{": "}",
        "<": ">",
    }

    def __init__(self, opener: str):
        self.closer = self.BRACKETS[opener]

    def read_next(self, next_character: str) -> ParseResult:
        if next_character == self.closer:
            result = ParseResult.CLOSE
        elif next_character in self.BRACKETS:
            result = ParseResult.NEW_OPEN
        else:
            result = ParseResult.ILLEGAL
        return result


def test_part_two():
    input_lines = [
        "[({(<(())[]>[[{[]{<()<>>",
        "[(()[<>])]({[<{<<[]>>(",
        "{([(<{}[<>[]}>{[]{[(<()>",
        "(((({<>}<{<{<>}{[]{[]{}",
        "[[<[([]))<([[{}[[()]]]",
        "[{[{({}]{}}([{[{{{}}([]",
        "{<[[]]>}<{[{[{[]{()[[[]",
        "[<(<(<(<{}))><([]([]()",
        "<{([([[(<>()){}]>(<<{{",
        "<{([{{}}[<[[[<>{}]]]>[]]",
    ]
    assert part_two(input_lines) == 288957
