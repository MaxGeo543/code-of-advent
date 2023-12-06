'''
'''

from pathlib import Path
mod_path = Path(__file__).parent
PUZZLE_INPUT_PATH = Path(mod_path, "puzzle_input.txt")
TEST_INPUT_PATH = Path(mod_path, "test_input.txt")

def part1(input_file):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()

def part2(input_file):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()

if __name__ == "__main__":
    # assert part1(TEST_INPUT_PATH)
    # assert part2(TEST_INPUT_PATH)
    
    part1(PUZZLE_INPUT_PATH)
    part2(PUZZLE_INPUT_PATH)