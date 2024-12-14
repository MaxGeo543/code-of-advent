def part1(input_file):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()

    # calculate result
    wires: dict[str,tuple[callable, list[str]|int|None]] = {}
    for line in puzzle_input:
        parts = line.strip().split(" ")
        if len(parts) == 3:
            


    if result < 0: result += 2**16
    
    return result

def part2(input_file):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()
    
    # calculate result
    result = ""
    
    # return result
    return result
