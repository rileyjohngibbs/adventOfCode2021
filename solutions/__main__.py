from importlib import import_module
import sys

from solutions.common.input_reader import get_input_lines


day_num = sys.argv[1]
if len(sys.argv) > 2:
    implementation = sys.argv[2]
else:
    implementation = "alpha"

solution_module = import_module(f"solutions.day{day_num.zfill(2)}.{implementation}")
input_lines = get_input_lines(int(day_num))
digester = getattr(solution_module, "digest_input", lambda x: x)
digested_lines = digester(input_lines)

part_one = getattr(solution_module, "part_one", lambda x: "(solution pending)")
solution_one = part_one(digested_lines)
print(f"Part One: {solution_one}")

part_two = getattr(solution_module, "part_two", lambda x: "(solution pending)")
solution_two = part_two(digested_lines)
print(f"Part One: {solution_two}")
