import re

def part1(input_file):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()

    result = 0
    for line_idx, line in enumerate(puzzle_input):
        number_lists = line.split(":")[1].split("|")
        winning_numbers = [re.sub("\n", "", num) for num in number_lists[0].split(" ") if num != ""]
        your_numbers = [re.sub("\n", "", num) for num in number_lists[1].split(" ") if num != ""]

        score = 0
        for num in your_numbers:
            if num in winning_numbers:
                if score == 0:
                    score += 1
                else:
                    score *= 2
        result += score

    return result

def part2(input_file):
    # returns the number of matching numbers, given a line of the puzzle input
    def matching_nums(text):
        number_lists = text.split(":")[1].split("|")
        winning_numbers = [re.sub("\n", "", num) for num in number_lists[0].split(" ") if num != ""]
        your_numbers = [re.sub("\n", "", num) for num in number_lists[1].split(" ") if num != ""]

        score = 0
        for num in your_numbers:
            if num in winning_numbers:
                score += 1
        return score

    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()

    scratchcards = [1 for line in puzzle_input]
    for line_idx, line in enumerate(puzzle_input):
        mult = scratchcards[line_idx]
        matches = matching_nums(line)
        for i in range(matches):
            scratchcards[line_idx + i + 1] += mult

    result = sum(scratchcards)
    return result
