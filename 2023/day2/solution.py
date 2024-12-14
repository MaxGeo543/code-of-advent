import re

def parse_game(text):
    game_id, draws = text.split(":")

    game_id = int(re.sub("[A-Za-z \n]*", "", game_id))
    draws = [c.split(",") for c in draws.split(";")]
    for i  in range(len(draws)):
        draw = draws[i]
        normalized_draw = [0,0,0]
        for color in draw:
            if "red" in color:
                normalized_draw[0] = int(re.sub("[A-Za-z \n]*", "", color))
            if "green" in color:
                normalized_draw[1] = int(re.sub("[A-Za-z \n]*", "", color))
            if "blue" in color:
                normalized_draw[2] = int(re.sub("[A-Za-z \n]*", "", color))
        draws[i] = normalized_draw

    return game_id, draws


def part1(input_file):
    # order is r, g, b
    bag = [12, 13, 14]

    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()

    result = 0
    for line in puzzle_input:
        game_id, draws = parse_game(line)
        max_red = max([draw[0] for draw in draws])
        max_green = max([draw[1] for draw in draws])
        max_blue = max([draw[2] for draw in draws])

        if max_red <= bag[0] and max_green <= bag[1] and max_blue <= bag[2]:
            result += game_id

    return result

def part2(input_file):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()

    result = 0
    for line in puzzle_input:
        game_id, draws = parse_game(line)
        max_red = max([draw[0] for draw in draws])
        max_green = max([draw[1] for draw in draws])
        max_blue = max([draw[2] for draw in draws])

        result += max_red * max_green * max_blue

    return result

