'''
puzzle description
'''

# get paths of input files
from pathlib import Path
mod_path = Path(__file__).parent
PUZZLE_INPUT_PATH = Path(mod_path, "puzzle_input.txt")
TEST_INPUT_PATH = Path(mod_path, "test_input.txt")


def part1(input_file):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()
    
    # print(result)
    # return result


if __name__ == "__main__":
    # assert part1(TEST_INPUT_PATH)
    
    # part1(PUZZLE_INPUT_PATH)