'''
--- Day 1: Trebuchet?! ---

Something is wrong with global snow production, and you've been selected to take a look. The Elves have even given you a map; on it, they've used stars to mark the top fifty locations that are likely to be having problems.

You've been doing this long enough to know that to restore snow operations, you need to check all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

You try to ask why they can't just use a weather machine ("not powerful enough") and where they're even sending you ("the sky") and why your map looks mostly blank ("you sure ask a lot of questions") and hang on did you just say the sky ("of course, where do you think snow comes from") when you realize that the Elves are already loading you into a trebuchet ("please hold still, we need to strap you in").

As they're making the final adjustments, they discover that their calibration document (your puzzle input) has been amended by a very young Elf who was apparently just excited to show off her art skills. Consequently, the Elves are having trouble reading the values on the document.

The newly-improved calibration document consists of lines of text; each line originally contained a specific calibration value that the Elves now need to recover. On each line, the calibration value can be found by combining the first digit and the last digit (in that order) to form a single two-digit number.

For example:

1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet

In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding these together produces 142.

Consider your entire calibration document. What is the sum of all of the calibration values?

--- Part Two ---

Your calculation isn't quite right. It looks like some of the digits are actually spelled out with letters: one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".

Equipped with this new information, you now need to find the real first and last digit on each line. For example:

two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen

In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these together produces 281.

What is the sum of all of the calibration values?
'''

from pathlib import Path
mod_path = Path(__file__).parent
PUZZLE_INPUT_PATH = Path(mod_path, "puzzle_input.txt")
TEST_INPUT_1_PATH = Path(mod_path, "test_input_1.txt")
TEST_INPUT_2_PATH = Path(mod_path, "test_input_2.txt")

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
    print(result)
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
                return str(i+1)
        
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
            if not digit  == None:
                num += digit
                break
            i += 1

        # go through all chars back to front and add the first digit found to num
        i = len(line) - 1
        while i >= 0:
            digit = get_digit(line, i)
            if not digit  == None:
                num += digit
                break
            i -= 1
        
        # add the number to the result
        result += int(num)

    # print the final result
    print(result)
    return result

if __name__ == "__main__":
    assert part1(TEST_INPUT_1_PATH) == 142
    assert part2(TEST_INPUT_2_PATH) == 281
    
    part1(PUZZLE_INPUT_PATH) # returns 55386
    part2(PUZZLE_INPUT_PATH) # returns 54824