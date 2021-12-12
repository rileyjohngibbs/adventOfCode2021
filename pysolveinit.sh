mkdir solutions/day$1 && touch solutions/day$1/__init__.py
echo "Created package solutions.day$1"

cat >> solutions/day$1/alpha.py <<EOF
def digest_input(input_lines: list[str]) -> list[str]:
    return input_lines


# def part_one(input_lines: list[str]) -> int:


# def part_two(input_lines: list[str]) -> int:
EOF
