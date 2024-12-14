import re

def part1(input_file):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()

    # pad input with . to avoid idx nound checks
    puzzle_input = [(len(puzzle_input[0]) - 1) * "." + "\n"] + puzzle_input
    for line in puzzle_input:
        line = "." + re.sub("\n", "", line) + ".\n"

    x = 0
    y = 0
    steps = 0
    current_char = "S"
    direction = 0  # 0,1,2,3 -> top,left,down,right
    # find Start
    for i in range(len(puzzle_input)):
        s_idx = puzzle_input[i].find("S")
        if s_idx != -1:
            y = i
            x = s_idx
            break

    start_pos_x = x
    start_pos_y = y
    while True:
        # treat first move differently, cause we don't know which symbol is under 'S'
        if x == start_pos_x and y == start_pos_y:
            below = puzzle_input[y + 1][x]
            above = puzzle_input[y - 1][x]
            right = puzzle_input[y][x + 1]
            left = puzzle_input[y][x - 1]

            if above in "|7F":
                y -= 1
                direction = "|7.F".find(above)
            elif left in ["-", "F", "L"]:
                x -= 1
                direction = "L-F.".find(left)
            elif below in ["|", "J", "L"]:
                y += 1
                direction = ".J|L".find(below)
            elif right in "7J-":
                x += 1
                direction = "J.7-".find(right)
        else:
            if direction == 0:
                y -= 1
                direction = "|7.F".find(puzzle_input[y][x])
            elif direction == 1:
                x -= 1
                direction = "L-F.".find(puzzle_input[y][x])
            elif direction == 2:
                y += 1
                direction = ".J|L".find(puzzle_input[y][x])
            elif direction == 3:
                x += 1
                direction = "J.7-".find(puzzle_input[y][x])
        steps += 1
        if x == start_pos_x and y == start_pos_y:
            break

    result = int(steps / 2)
    return result


def part2(input_file):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()

    linelen = len(puzzle_input[0]) - 1
    # pad input with dots to avoid index bound checking
    puzzle_input = [linelen * "." + "\n"] + puzzle_input
    for line in puzzle_input:
        line = "." + re.sub("\n", "", line) + ".\n"
    linelen = len(puzzle_input[0]) - 1

    x = 0
    y = 0
    steps = 0
    current_char = "S"
    direction = 0  # 0,1,2,3 -> top,left,down,right

    # find Start
    for i in range(len(puzzle_input)):
        s_idx = puzzle_input[i].find("S")
        if s_idx != -1:
            y = i
            x = s_idx
            break
    start_pos_x = x
    start_pos_y = y
    # get list of coordinates of loop
    loop_coordinates = []
    while True:
        loop_coordinates.append((x, y))
        if x == start_pos_x and y == start_pos_y:
            below = puzzle_input[y + 1][x]
            above = puzzle_input[y - 1][x]
            right = puzzle_input[y][x + 1]
            left = puzzle_input[y][x - 1]

            if above in "|7F":
                y -= 1
                direction = "|7.F".find(above)
            elif left in ["-", "F", "L"]:
                x -= 1
                direction = "L-F.".find(left)
            elif below in ["|", "J", "L"]:
                y += 1
                direction = ".J|L".find(below)
            elif right in "7J-":
                x += 1
                direction = "J.7-".find(right)
        else:
            if direction == 0:
                y -= 1
                direction = "|7.F".find(puzzle_input[y][x])
            elif direction == 1:
                x -= 1
                direction = "L-F.".find(puzzle_input[y][x])
            elif direction == 2:
                y += 1
                direction = ".J|L".find(puzzle_input[y][x])
            elif direction == 3:
                x += 1
                direction = "J.7-".find(puzzle_input[y][x])
        steps += 1
        if x == start_pos_x and y == start_pos_y:
            break

    result = 0
    count_mask = [False] * linelen
    for y in range(len(puzzle_input)):
        line = puzzle_input[y]
        for x in range(linelen):
            if count_mask[x] and not (x, y) in loop_coordinates:
                result += 1
            if (x, y) in loop_coordinates and line[x] not in "S|J7":
                count_mask[x] = not count_mask[x]

    return result
