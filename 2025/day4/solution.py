def neighborhood(grid, x, y):
    neighbors = [
        (-1,-1), (0, -1), (1, -1),
        (-1, 0),          (1,  0),
        (-1, 1), (0,  1), (1,  1)
    ]

    return [grid[y+_y][x+_x] for (_x, _y) in neighbors if 0 <= x+_x < len(grid[0]) and 0 <= y+_y < len(grid)]

def clear(grid):
    result = 0
    for y, line in enumerate(grid):
        for x, cell in enumerate(line):
            if cell == 0: continue
            

            num_neighbors = sum(neighborhood(grid, x, y))
            if num_neighbors < 4:
                grid[y][x] = 0
                result += 1
    
    if result != 0: 
        result += clear(grid)
    return result

def part1(input_file, debug=False):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()
    
    puzzle_input_bin = [[1 if c == "@" else 0 for c in line.strip()] for line in puzzle_input]
    puzzle_input = [[c for c in line.strip()] for line in puzzle_input]
    
    # calculate result
    result = 0
    for y, line in enumerate(puzzle_input_bin):
        for x, cell in enumerate(line):
            if cell == 0: continue
            

            num_neighbors = sum(neighborhood(puzzle_input_bin, x, y))
            if num_neighbors < 4:
                puzzle_input[y][x] = "x"
                result += 1
    
    # return result
    return result

def part2(input_file, debug=False):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()
    
    puzzle_input_bin = [[1 if c == "@" else 0 for c in line.strip()] for line in puzzle_input]

    # calculate result
    result = clear(puzzle_input_bin)
    
    # return result
    return result
