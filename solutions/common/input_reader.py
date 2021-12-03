import os

INPUTS_DIRECTORY = os.path.dirname(__file__) + "/../../inputs"


def get_input_lines(day_number: int) -> list[str]:
    input_path = os.path.join(INPUTS_DIRECTORY, f"{str(day_number).zfill(2)}.txt")
    with open(input_path) as input_file:
        return [line.replace("\n", "") for line in input_file.readlines()]
