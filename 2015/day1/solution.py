def part1(input_file):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()
    puzzle_input = "".join(puzzle_input)

    # calculate result
    # open brackets go up one floor (+1) closing brackets go down (-1)
    # subtracting the counts of the 2 should return the final floor
    result = puzzle_input.count("(") - puzzle_input.count(")")
    
    # return result
    return result

def part2(input_file):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()
    puzzle_input = "".join(puzzle_input)

    floor = 0
    for i, c in enumerate(puzzle_input):
        if c == "(": floor += 1
        else: floor -= 1
        if floor < 0:
            return i + 1

    # calculate result
    result = ""
    
    # return result
    return result
