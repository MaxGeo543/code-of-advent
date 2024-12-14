
def is_between(num, a, b):
    return (a < b and a < num and num < b) or (b < a and b < num and num < a)

def part1(input_file):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()

    width = len(puzzle_input[0]) - 1
    height = len(puzzle_input)

    empty_rows = []
    empty_cols = []
    for i in range(height):
        if not "#" in puzzle_input[i]:
            empty_rows.append(i)
    for i in range(width):
        if all(puzzle_input[j][i] != "#" for j in range(height)):
            empty_cols.append(i)

    galaxies = []
    for y in range(height):
        for x in range(width):
            if puzzle_input[y][x] == "#":
                galaxies.append((x, y))

    result = 0
    for i in range(len(galaxies)):
        for j in range(i + 1, len(galaxies)):

            g1 = galaxies[i]
            g2 = galaxies[j]
            distance = abs(g1[0] - g2[0]) + abs(g1[1] - g2[1])
            for row in empty_rows:
                if is_between(row, g1[1], g2[1]):
                    distance += 1
            for col in empty_cols:
                if is_between(col, g1[0], g2[0]):
                    distance += 1
            result += distance

    return result

def part2(input_file, empty_size=1000000):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()

    width = len(puzzle_input[0]) - 1
    height = len(puzzle_input)

    empty_rows = []
    empty_cols = []
    for i in range(height):
        if not "#" in puzzle_input[i]:
            empty_rows.append(i)
    for i in range(width):
        if all(puzzle_input[j][i] != "#" for j in range(height)):
            empty_cols.append(i)

    galaxies = []
    for y in range(height):
        for x in range(width):
            if puzzle_input[y][x] == "#":
                galaxies.append((x, y))

    result = 0
    for i in range(len(galaxies)):
        for j in range(i + 1, len(galaxies)):

            g1 = galaxies[i]
            g2 = galaxies[j]
            distance = abs(g1[0] - g2[0]) + abs(g1[1] - g2[1])
            for row in empty_rows:
                if is_between(row, g1[1], g2[1]):
                    distance += empty_size - 1
            for col in empty_cols:
                if is_between(col, g1[0], g2[0]):
                    distance += empty_size - 1
            result += distance

    return result
