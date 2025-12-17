def part1(input_file):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()
    
    # calculate result
    result = 0
    dial = 50
    for line in puzzle_input:
        line = line.strip()
        d = line[0]
        n = int(line[1:])
        if d == "R":
            dial = (dial + n)%100
        else:
            dial = (dial - n)%100
        
        if dial == 0:
            result += 1
    
    # return result
    return result

def part2(input_file, start=50):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()

    # calculate result
    result = 0
    dial = start
    for line in puzzle_input:
        line = line.strip()
        d = line[0]
        n = int(line[1:])

        q, r = divmod(n, 100)
        result += q

        if r == 0:
            continue

        if d == "R":
            if dial + r >= 100:
                result += 1
            dial = (dial + r) % 100
        else:
            if dial != 0 and r >= dial:
                result += 1
            dial = (dial - r) % 100

    # return result
    return result