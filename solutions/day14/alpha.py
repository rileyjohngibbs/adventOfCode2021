from collections import Counter

import pytest


def digest_input(input_lines: list[str]) -> tuple[str, dict[str, str]]:
    base = input_lines[0]
    insertions: dict[str, str] = {}
    for input_line in input_lines[2:]:
        pair_key, insertion = input_line.split(" -> ")
        insertions[pair_key] = insertion
    return base, insertions


def part_one(chain_rules: tuple[str, dict[str, str]]) -> int:
    chain, insertion_rules = chain_rules
    for _ in range(10):
        chain = apply_insertion_rules(chain, insertion_rules)
    counter = Counter(chain).most_common()
    least, most = counter[-1][1], counter[0][1]
    return most - least


def apply_insertion_rules(chain: str, insertion_rules: dict[str, str]) -> str:
    output = ""
    for a, b in zip(chain[:-1], chain[1:]):
        insertion = insertion_rules[f"{a}{b}"]
        output += f"{a}{insertion}"
    output += chain[-1]
    return output


def part_two(chain_rules: tuple[str, dict[str, str]]) -> int:
    chain, insertion_rules = chain_rules
    character_counter = implicitly_apply_insertion_rules(chain, insertion_rules, 40)
    least = min(character_counter.values())
    most = max(character_counter.values())
    return most - least


def implicitly_apply_insertion_rules(
    chain: str, insertion_rules: dict[str, str], steps: int
) -> dict[str, int]:
    token_counter = dict(Counter(f"{a}{b}" for a, b in zip(chain[:-1], chain[1:])))
    for _ in range(steps):
        token_counter = build_new_token_counter(token_counter, insertion_rules)

    character_counter: dict[str, int] = {}
    for token, count in token_counter.items():
        character_counter[token[0]] = character_counter.get(token[0], 0) + count
    character_counter[chain[-1]] = character_counter.get(chain[-1], 0) + 1

    return character_counter


def build_new_token_counter(
    counter: dict[str, int], insertion_rules: dict[str, str]
) -> dict[str, int]:
    new_counter: dict[str, int] = {}
    for token, count in counter.items():
        insert = insertion_rules[token]
        new_counter[f"{token[0]}{insert}"] = (
            new_counter.get(f"{token[0]}{insert}", 0) + count
        )
        new_counter[f"{insert}{token[1]}"] = (
            new_counter.get(f"{insert}{token[1]}", 0) + count
        )
    return new_counter


TEST_CASE = [
    "NNCB",
    "",
    "CH -> B",
    "HH -> N",
    "CB -> H",
    "NH -> C",
    "HB -> C",
    "HC -> B",
    "HN -> C",
    "NN -> C",
    "BH -> H",
    "NC -> B",
    "NB -> B",
    "BN -> B",
    "BB -> N",
    "BC -> B",
    "CC -> N",
    "CN -> C",
]


@pytest.mark.parametrize("steps", [0, 1, 2, 5, 10])
def test_implicit(steps):
    chain, insertion_rules = digest_input(TEST_CASE)

    explicit_chain = chain
    for _ in range(steps):
        explicit_chain = apply_insertion_rules(explicit_chain, insertion_rules)
    explicit_counter = dict(Counter(explicit_chain))

    implicit_counter = implicitly_apply_insertion_rules(chain, insertion_rules, steps)

    assert explicit_counter == implicit_counter
