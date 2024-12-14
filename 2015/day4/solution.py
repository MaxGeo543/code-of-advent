import hashlib

def part1(input_file):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()
    key = "".join(puzzle_input)

    # calculate result
    i = 0
    while True:
        s = (key + str(i)).encode('utf-8')
        result = hashlib.md5(s).hexdigest()
        if result.startswith("00000"):
            return i
        i += 1

def part2(input_file):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()
    key = "".join(puzzle_input)

    # calculate result
    i = 254575 # this is the answer from the previous part, we don't have to start from the beginning
    # i = part1(input_file)
    while True:
        s = (key + str(i)).encode('utf-8')
        result = hashlib.md5(s).hexdigest()
        if result.startswith("000000"):
            return i
        i += 1

