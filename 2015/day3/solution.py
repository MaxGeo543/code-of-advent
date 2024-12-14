def part1(input_file):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()
    puzzle_input = "".join(puzzle_input)

    # calculate result
    # simply keep track of the current coordinates and visited coordinates using a set to ignore multiplicity
    # at the end return the length of the set
    visited_houses = set()
    x, y = (0, 0)
    visited_houses.add((x, y))
    for c in puzzle_input:
        match c:
            case ">":
                x += 1
            case "<":
                x -= 1
            case "^":
                y += 1
            case "v":
                y -= 1
        visited_houses.add((x, y))
    result = len(visited_houses)
    
    # return result
    return result

def part2(input_file):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()
    puzzle_input = "".join(puzzle_input)

    # calculate result
    # this time we keep track of the current position by having x and y coordinates be a list (one entry for each "mover" aka santa & robo santa)
    # the variable mover keeps track of who is moving, in the loop mover increments and goes back to 0 if its out of bounds for indexing x
    visited_houses = set()
    x = [0, 0]
    y = [0, 0]
    mover = 0
    visited_houses.add((x[mover], y[mover]))
    for c in puzzle_input:
        match c:
            case ">":
                x[mover] += 1
            case "<":
                x[mover] -= 1
            case "^":
                y[mover] += 1
            case "v":
                y[mover] -= 1
        visited_houses.add((x[mover], y[mover]))
        mover = (mover + 1)%len(x)
    result = len(visited_houses)

    # return result
    return result
