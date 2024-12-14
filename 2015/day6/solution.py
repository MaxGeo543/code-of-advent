def parse_line(line: str):
    a, c2 = line.split("through")

    a = a.strip().split(" ")
    if len(a) == 2:
        operation, c1 = a
    else:
        operation = f"{a[0]} {a[1]}"
        c1 = a[2]
    c1 = [int(n) for n in c1.strip().split(",")]
    c2 = [int(n) for n in c2.strip().split(",")]

    return operation, c1, c2

def part1(input_file):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()

    grid = [[0 for _ in range(1000)] for _ in range(1000)]

    # calculate result
    for line in puzzle_input:
        op, p0, p1 = parse_line(line)
        x0, y0 = p0
        x1, y1 = p1
        for x in range(x0, x1 + 1, 1 if x0 <= x1 else -1):
            for y in range(y0, y1 + 1, 1 if y0 <= y1 else -1):
                match op:
                    case "toggle":
                        grid[y][x] += 1
                        grid[y][x] %= 2
                    case "turn on":
                        grid[y][x] = 1
                    case "turn off":
                        grid[y][x] = 0
                    case _:
                        print("WHAT??")

    result = sum(sum(row) for row in grid)

    # return result
    return result

def part2(input_file):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()

    grid = [[0 for _ in range(1000)] for _ in range(1000)]

    # calculate result
    for line in puzzle_input:
        op, p0, p1 = parse_line(line)
        x0, y0 = p0
        x1, y1 = p1
        for x in range(x0, x1 + 1, 1 if x0 <= x1 else -1):
            for y in range(y0, y1 + 1, 1 if y0 <= y1 else -1):
                match op:
                    case "toggle":
                        grid[y][x] += 2
                    case "turn on":
                        grid[y][x] += 1
                    case "turn off":
                        grid[y][x] -= 1
                        if grid[y][x] < 0: grid[y][x] = 0
                    case _:
                        print("WHAT??")

    result = sum(sum(row) for row in grid)

    # return result
    return result
