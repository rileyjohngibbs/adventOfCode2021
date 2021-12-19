from abc import ABC, abstractmethod
from enum import Enum
from functools import reduce

import pytest


class Operator(Enum):
    SUM = 0
    PRODUCT = 1
    MINIMUM = 2
    MAXIMUM = 3
    LITERAL = 4
    GREATER = 5
    LESS = 6
    EQUAL = 7


def digest_input(input_lines: list[str]) -> str:
    return "".join(bin(int(char, 16))[2:].zfill(4) for char in input_lines[0])


def part_one(bit_string: str) -> int:
    index = 0
    packets: list[Packet] = []
    while any(b != "0" for b in bit_string[index:]):
        packet, index_bump = parse_next_packet(bit_string[index:])
        packets.append(packet)
        index += index_bump
    return sum(p.version_sum() for p in packets)


def part_two(bit_string: str) -> int:
    index = 0
    packets: list[Packet] = []
    while any(b != "0" for b in bit_string[index:]):
        packet, index_bump = parse_next_packet(bit_string[index:])
        packets.append(packet)
        index += index_bump
    return sum(p.evaluate() for p in packets)


def parse_next_packet(bits) -> tuple["Packet", int]:
    index = 0
    version = int(bits[index:index + 3], 2)
    index += 3
    operator_code = int(bits[index:index + 3], 2)
    index += 3
    packet_class: type[Packet]
    if operator_code == 4:
        packet_class = Literal
        operator = Operator.LITERAL
    else:
        packet_class = OperationPacket
        operator = Operator(operator_code)
    packet = packet_class(version, operator)
    index += packet.parse_body(bits[index:])
    return packet, index


class Packet(ABC):
    version: int
    operator: "Operator"

    def __init__(self, version: int, operator: Operator):
        self.version = version
        self.operator = operator

    @abstractmethod
    def version_sum(self) -> int: ...

    @abstractmethod
    def parse_body(self, bits: str) -> int: ...

    @abstractmethod
    def evaluate(self) -> int: ...


class Literal(Packet):
    value: int

    def __init__(self, version: int, operator: Operator):
        super().__init__(version, operator)
        self.value = 0

    def version_sum(self) -> int:
        return self.version

    def evaluate(self) -> int:
        return self.value

    def parse_body(self, bits: str) -> int:
        """Returns number of bits consumed."""
        index = 0
        last_group = False
        self.value = 0
        while not last_group:
            last_group = bits[index] == "0"
            self.value = 16 * self.value + int(bits[index + 1:index + 5], 2)
            index += 5
        return index


class OperationPacket(Packet):
    sub_packets: list["Packet"]

    def __init__(self, version: int, operator: Operator):
        super().__init__(version, operator)
        self.sub_packets: list[Packet] = []

    def version_sum(self) -> int:
        return sum(sp.version_sum() for sp in self.sub_packets) + self.version

    def evaluate(self) -> int:
        args = tuple(p.evaluate() for p in self.sub_packets)
        if self.operator is Operator.SUM:
            return sum(args)
        elif self.operator is Operator.PRODUCT:
            return reduce(lambda a, b: a * b, args, 1)
        elif self.operator is Operator.MINIMUM:
            return min(args)
        elif self.operator is Operator.MAXIMUM:
            return max(args)
        elif self.operator is Operator.GREATER:
            a, b = args
            return int(a > b)
        elif self.operator is Operator.LESS:
            a, b = args
            return int(a < b)
        elif self.operator is Operator.EQUAL:
            a, b = args
            return int(a == b)
        else:
            raise ValueError(self.operator)

    def parse_body(self, bits: str) -> int:
        """Returns number of bits consumed."""
        index = 0
        length_by_bits = bits[0] == "0"
        if length_by_bits:
            total_length = int(bits[1:16], 2) + 16
            index = 16
            while index < total_length:
                packet, index_bump = parse_next_packet(bits[index:])
                self.sub_packets.append(packet)
                index += index_bump
        else:
            packets_count = int(bits[1:12], 2)
            index = 12
            for _ in range(packets_count):
                packet, index_bump = parse_next_packet(bits[index:])
                self.sub_packets.append(packet)
                index += index_bump
        return index
        

"""
GRAMMAR

packet: version packet_body packet_tail

packet_tail: 0 packet_tail
packet_tail: -

version: BIT BIT BIT

packet_body: "100" literal_value
packet_body: operator 0 sub_packets_length sub_packets
packet_body: operator 1 sub_packets_count sub_packets

literal_value: 1 BIT BIT BIT BIT literal_value
literal_value: 0 BIT BIT BIT BIT

operator: BIT BIT BIT

sub_packets_length: BIT (x15)

sub_packets_count: BIT (x11)

sub_packets: packet sub_packets
sub_packets: -
"""


EXAMPLE_A = ["8A004A801A8002F478"]
EXAMPLE_B = ["620080001611562C8802118E34"]
EXAMPLE_C = ["C0015000016115A2E0802F182340"]
EXAMPLE_D = ["A0016C880162017C3686B18A3D4780"]

@pytest.mark.parametrize("hexstring, version_sum", [
    (EXAMPLE_A, 16),
    (EXAMPLE_B, 12),
    (EXAMPLE_C, 23),
    (EXAMPLE_D, 31),
])
def test_part_one(hexstring, version_sum):
    assert part_one(digest_input(hexstring)) == version_sum


EXAMPLES_TWO = [
    (["C200B40A82"], 3),
    (["04005AC33890"], 54),
    (["880086C3E88112"], 7),
    (["CE00C43D881120"], 9),
    (["D8005AC2A8F0"], 1),
    (["F600BC2D8F"], 0),
    (["9C005AC2F8F0"], 0),
    (["9C0141080250320F1802104A08"], 1),
    (["0200808021102100802104204"], 15),
]


@pytest.mark.parametrize("hexstring, value", EXAMPLES_TWO)
def test_part_two(hexstring, value):
    assert part_two(digest_input(hexstring)) == value


LITERAL_8 = (
    "000"
    "100"
    "01000"
)
LITERAL_4 = (
    "000"
    "100"
    "00100"
)
SUM_12 = (
    "000"
    "000"
    "1"
    "00000000010"
    + LITERAL_8 + LITERAL_4
)
SUM_24 = (
    "000"
    "000"
    "1"
    "00000000010"
    + SUM_12 + SUM_12
)
LITERAL_44 = (
    "000"
    "100"
    "10010"
    "01100"
)
TEST_PACKETS = [
    (LITERAL_8, Operator.LITERAL, 8),
    (LITERAL_4, Operator.LITERAL, 4),
    (SUM_12, Operator.SUM, 12),
    (SUM_24, Operator.SUM, 24),
    (LITERAL_44, Operator.LITERAL, 44),
]


@pytest.mark.parametrize("bitstring, operator, value", TEST_PACKETS)
def test_parse_packet(bitstring, operator, value):
    packet, index = parse_next_packet(bitstring)
    assert index == len(bitstring)
    assert packet.operator == operator
    assert packet.evaluate() == value


def test_parse_body():
    packet = OperationPacket(0, Operator.SUM)
    index = packet.parse_body(SUM_12[6:])
    assert index == len(SUM_12) - 6
