import time
from typing import Callable, Iterator, Optional

import pytest


class Position:
    x: int
    y: int
    risk: int
    neighbors: list["Position"]

    def __init__(self, x: int, y: int, risk: int):
        self.x = x
        self.y = y
        self.risk = risk
        self.neighbors = []

    def __repr__(self) -> str:
        return f"Position<({self.x}, {self.y}), {self.risk}>"

    def __eq__(self, other: object) -> bool:
        if type(other) == Position:
            return self.address == other.address and self.risk == other.risk
        return False

    def add_neighbor(self, neighbor: "Position"):
        if neighbor not in self.neighbors:
            self.neighbors.append(neighbor)
            neighbor.add_neighbor(self)

    @property
    def address(self) -> tuple[int, int]:
        return (self.x, self.y)


class Path:
    positions: list["Position"]
    risk: int

    def __init__(self, positions: list[Position], risk: Optional[int] = None):
        self.positions = positions
        self.risk = risk if risk is not None else sum(p.risk for p in positions)

    def __repr__(self) -> str:
        start = self.positions[0]
        end = self.positions[-1]
        if len(self.positions) < 3:
            return f"Path<({start.x}, {start.y}), ({end.x}, {end.y})>"
        return (
            f"Path<({start.x}, {start.y}), "
            f"[{len(self.positions) - 2}], "
            f"({end.x}, {end.y})>"
        )

    @property
    def tail(self) -> "Position":
        return self.positions[-1]

    def copy(self, new_position: "Position") -> "Path":
        new_path = Path(self.positions[:], self.risk)
        new_path.append(new_position)
        return new_path

    def append(self, position: "Position"):
        if position not in self.positions[-1].neighbors:
            raise ValueError(
                f"{position} not a valid neighbor of "
                f"{self.positions[-1]} at end of path"
            )
        self.positions.append(position)
        self.risk += position.risk

    def next_positions(self) -> Iterator["Position"]:
        return (n for n in self.tail.neighbors if n not in self.positions)


def digest_input(input_lines: list[str]) -> list[Position]:
    positions_dict = {
        (x, y): Position(x, y, int(risk))
        for y, row in enumerate(input_lines)
        for x, risk in enumerate(row)
    }
    for address, position in positions_dict.items():
        x, y = address
        for neighbor_address in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            neighbor = positions_dict.get(neighbor_address)
            if neighbor is not None:
                position.add_neighbor(neighbor)
    return list(positions_dict.values())


def part_one(positions: list[Position]) -> int:
    pathfinder = Pathfinder(positions)
    pathfinder.seek_least_risk_to_end()
    return pathfinder.get_risk_to_end()


class Pathfinder:
    start: Position
    end: Position
    visited: dict[tuple[int, int], int]
    paths: list[Path]

    def __init__(self, positions: list[Position]):
        self.start = min(positions, key=lambda p: p.address)
        self.end = max(positions, key=lambda p: p.address)
        self.size = len(positions)
        self.visited: dict[tuple[int, int], int] = {
            p.address: self.size for p in positions
        }
        self.visited[self.start.address] = 0
        self.paths = [Path([self.start], 0)]

    def heuristic(self, path: Path) -> int:
        return path.risk + (self.end.y - path.tail.y + self.end.x - path.tail.x)

    def seek_least_risk_to_end(self):
        time_start = time.time()
        count = 0
        done = False
        while not done:
            path = self.paths.pop(0)
            expansions = self.expand_path(path)
            self.visited.update({exp.tail.address: exp.risk for exp in expansions})
            for exp in expansions:
                sorted_insert(self.paths, exp, self.heuristic)
            done = any(exp.tail == self.end for exp in expansions)
            count += 1
            if count % 1000 == 0:
                reset = time.time()
                print(
                    f"Iterations: {count}; Paths: {len(self.paths)}; "
                    f"Time delta: {reset - time_start}"
                )
                time_start = reset

    def get_risk_to_end(self) -> int:
        path_to_end = next((p for p in self.paths if p.tail == self.end), None)
        if path_to_end is not None:
            return path_to_end.risk
        else:
            raise ValueError("No path found to end")

    def expand_path(self, path: Path) -> list[Path]:
        candidates = path.next_positions()
        return [
            path.copy(c)
            for c in candidates
            if self.visited[c.address] > path.risk + c.risk
        ]


def part_two(positions: list[Position]) -> int:
    positions = expand_five_times(positions)
    pathfinder = Pathfinder(positions)
    pathfinder.seek_least_risk_to_end()
    return pathfinder.get_risk_to_end()


def expand_five_times(positions: list[Position]) -> list[Position]:
    tile_width = max(p.x for p in positions) + 1
    tile_height = max(p.y for p in positions) + 1
    full_map_dict = {
        (
            position.x + tile_width * big_column,
            position.y + tile_height * big_row,
        ): Position(
            position.x + tile_width * big_column,
            position.y + tile_height * big_row,
            (position.risk - 1 + big_column + big_row) % 9 + 1,
        )
        for big_row in range(5)
        for big_column in range(5)
        for position in positions
    }
    for address, position in full_map_dict.items():
        x, y = address
        for neighbor_address in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if neighbor := full_map_dict.get(neighbor_address):
                position.add_neighbor(neighbor)
    return list(full_map_dict.values())


def sorted_insert(paths: list[Path], new_path: Path, key: Callable[[Path], int]):
    left = 0
    right = len(paths)
    new_path_value = key(new_path)
    while right > left + 1:
        test_index = (right + left) // 2
        if key(paths[test_index]) > new_path_value:
            right = test_index
        else:
            left = test_index
    paths[right:right] = [new_path]


TEST_INPUT = [
    "1163751742",
    "1381373672",
    "2136511328",
    "3694931569",
    "7463417111",
    "1319128137",
    "1359912421",
    "3125421639",
    "1293138521",
    "2311944581",
]
SNAKE_TEST = [
    "11112",
    "99912",
    "11112",
    "19979",
    "11111",
]
COLLISION_TEST = [
    "119",
    "221",
    "921",
]


@pytest.mark.parametrize(
    "input_, expected_risk", [(TEST_INPUT, 40), (SNAKE_TEST, 14), (COLLISION_TEST, 5)]
)
def test_part_one(input_, expected_risk):
    assert part_one(digest_input(input_)) == expected_risk


def test_part_two():
    assert part_two(digest_input(TEST_INPUT)) == 315


EXPANDED_TEST_INPUT = [
    "11637517422274862853338597396444961841755517295286",
    "13813736722492484783351359589446246169155735727126",
    "21365113283247622439435873354154698446526571955763",
    "36949315694715142671582625378269373648937148475914",
    "74634171118574528222968563933317967414442817852555",
    "13191281372421239248353234135946434524615754563572",
    "13599124212461123532357223464346833457545794456865",
    "31254216394236532741534764385264587549637569865174",
    "12931385212314249632342535174345364628545647573965",
    "23119445813422155692453326671356443778246755488935",
    "22748628533385973964449618417555172952866628316397",
    "24924847833513595894462461691557357271266846838237",
    "32476224394358733541546984465265719557637682166874",
    "47151426715826253782693736489371484759148259586125",
    "85745282229685639333179674144428178525553928963666",
    "24212392483532341359464345246157545635726865674683",
    "24611235323572234643468334575457944568656815567976",
    "42365327415347643852645875496375698651748671976285",
    "23142496323425351743453646285456475739656758684176",
    "34221556924533266713564437782467554889357866599146",
    "33859739644496184175551729528666283163977739427418",
    "35135958944624616915573572712668468382377957949348",
    "43587335415469844652657195576376821668748793277985",
    "58262537826937364893714847591482595861259361697236",
    "96856393331796741444281785255539289636664139174777",
    "35323413594643452461575456357268656746837976785794",
    "35722346434683345754579445686568155679767926678187",
    "53476438526458754963756986517486719762859782187396",
    "34253517434536462854564757396567586841767869795287",
    "45332667135644377824675548893578665991468977611257",
    "44961841755517295286662831639777394274188841538529",
    "46246169155735727126684683823779579493488168151459",
    "54698446526571955763768216687487932779859814388196",
    "69373648937148475914825958612593616972361472718347",
    "17967414442817852555392896366641391747775241285888",
    "46434524615754563572686567468379767857948187896815",
    "46833457545794456865681556797679266781878137789298",
    "64587549637569865174867197628597821873961893298417",
    "45364628545647573965675868417678697952878971816398",
    "56443778246755488935786659914689776112579188722368",
    "55172952866628316397773942741888415385299952649631",
    "57357271266846838237795794934881681514599279262561",
    "65719557637682166874879327798598143881961925499217",
    "71484759148259586125936169723614727183472583829458",
    "28178525553928963666413917477752412858886352396999",
    "57545635726865674683797678579481878968159298917926",
    "57944568656815567976792667818781377892989248891319",
    "75698651748671976285978218739618932984172914319528",
    "56475739656758684176786979528789718163989182927419",
    "67554889357866599146897761125791887223681299833479",
]
EXPANSION_TEST = (
    ["5"],
    ["56789", "67891", "78912", "89123", "91234"],
)


@pytest.mark.parametrize(
    "original, expanded",
    [
        (TEST_INPUT, EXPANDED_TEST_INPUT),
        EXPANSION_TEST,
    ],
)
def test_quintupling(original, expanded):
    expanded_original = expand_five_times(digest_input(original))
    expanded_original.sort(key=lambda p: p.address)
    expected = digest_input(expanded)
    expected.sort(key=lambda p: p.address)
    assert expected == expanded_original
