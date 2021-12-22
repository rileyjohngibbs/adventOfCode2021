from importlib import import_module
import sys
import time

from solutions.common.input_reader import get_input_lines


day_num = sys.argv[1]
if len(sys.argv) > 2:
    implementation = sys.argv[2]
else:
    implementation = "alpha"

HLINE_SIZE = 60

print("="*HLINE_SIZE)
print(f"Running solutions to day {day_num}")
print("-"*HLINE_SIZE)

solution_module = import_module(f"solutions.day{day_num.zfill(2)}.{implementation}")
input_lines = get_input_lines(int(day_num))
digester = getattr(solution_module, "digest_input", lambda x: x)
digested_lines = digester(input_lines)

part_one = getattr(solution_module, "part_one", lambda x: "(solution pending)")
start_one = time.time()
digested_lines = digester(input_lines[:])
digest_one = time.time()
solution_one = part_one(digested_lines)
end_one = time.time()
print(f"Part one solution: {solution_one}")

part_two = getattr(solution_module, "part_two", lambda x: "(solution pending)")
start_two = time.time()
digested_lines = digester(input_lines)
digest_two = time.time()
solution_two = part_two(digested_lines)
end_two = time.time()
print(f"Part two solution: {solution_two}")

print("-"*HLINE_SIZE)

print(f"Part one runtime: {end_one - start_one:.6f} ({digest_one - start_one:.6f} digesting)")
print(f"Part two runtime: {end_two - start_two:.6f} ({digest_two - start_two:.6f} digesting)")

print("="*HLINE_SIZE)
