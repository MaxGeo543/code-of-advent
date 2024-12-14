def part1(input_file):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()

    # set the initial value of the result to 0
    result = 0
    # loop over all lines
    for line in puzzle_input:
        # set initial value of the number as a string to be empty
        num = ""

        # go through all chars front to back and add the first digit found to num
        for c in line:
            if c.isdigit():
                num += c
                break

        # go through all chars back to front and add the first digit found to num
        for c in line[::-1]:
            if c.isdigit():
                num += c
                break
        # add the number to the result
        result += int(num)

    # print the final result
    return result

def part2(input_file):
    def get_digit(text, start=0):
        digits = [
            "one",
            "two",
            "three",
            "four",
            "five",
            "six",
            "seven",
            "eight",
            "nine"
        ]

        if text[start].isdigit():
            return text[start]
        for i in range(9):
            if text.find(digits[i], start) == start:
                return str(i + 1)

        return None

    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()

    # set the initial value of the result to 0
    result = 0

    # loop over all lines
    for line in puzzle_input:

        # set initial value of the number as a string to be empty
        num = ""

        # go through all chars front to back
        i = 0
        while i < len(line):
            digit = get_digit(line, i)
            if not digit == None:
                num += digit
                break
            i += 1

        # go through all chars back to front and add the first digit found to num
        i = len(line) - 1
        while i >= 0:
            digit = get_digit(line, i)
            if not digit == None:
                num += digit
                break
            i -= 1

        # add the number to the result
        result += int(num)

    # print the final result
    return result
