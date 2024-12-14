def part1(input_file):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()

    # calculate result
    result = 0
    left = []
    right = []
    for line in puzzle_input:
        r, l = line.split("   ")
        r = int(r.strip())
        l = int(l.strip())
        left.append(l)
        right.append(r)

    right.sort()
    left.sort()

    for i in range(len(left)):
        result += abs(right[i] - left[i])

    # return result
    return result

def part2(input_file):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()
    
    # calculate result
    result = 0
    left = []
    right = []
    for line in puzzle_input:
        r, l = line.split("   ")
        r = int(r.strip())
        l = int(l.strip())
        left.append(l)
        right.append(r)

    for l in left:
        result += l * right.count(l)
    
    # return result
    return result
