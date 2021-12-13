import pytest


def digest_input(input_lines: list[str]) -> dict[str, set[str]]:
    nodes: dict[str, set[str]] = {}
    for input_line in input_lines:
        root, branch = input_line.split("-", 1)
        nodes.setdefault(root, set()).add(branch)
        nodes.setdefault(branch, set()).add(root)
    return nodes


def part_one(nodes: dict[str, set[str]]) -> int:
    return len(build_paths_to_end(nodes, ["start"]))


def build_paths_to_end(
    nodes: dict[str, set[str]], base: list[str], can_double: bool = False
) -> list[list[str]]:
    if base[-1] == "end":
        return [base]
    paths = []
    for branch in nodes[base[-1]]:
        if branch.isupper() or branch not in base:
            paths.extend(build_paths_to_end(nodes, base + [branch], can_double))
        elif branch != "start" and can_double:
            paths.extend(build_paths_to_end(nodes, base + [branch], can_double=False))
    return paths


def part_two(nodes: dict[str, set[str]]) -> int:
    return len(build_paths_to_end(nodes, ["start"], can_double=True))


@pytest.fixture
def example_one():
    input_lines = [
        "start-A",
        "start-b",
        "A-c",
        "A-b",
        "b-d",
        "A-end",
        "b-end",
    ]
    return digest_input(input_lines)


def test_part_one(example_one):
    assert part_one(example_one) == 10


def test_build_paths_to_end(example_one):
    paths = build_paths_to_end(example_one, ["start"])
    assert len(paths) == 10


def test_part_two(example_one):
    assert part_two(example_one) == 36


def test_build_paths_to_end_part_two(example_one):
    paths = build_paths_to_end(example_one, ["start"], True)
    assert len(paths) == 36
