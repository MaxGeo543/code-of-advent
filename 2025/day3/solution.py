def find_max_joltage(line: str) -> int:
    result = ""
    max_digit = 0
    max_digit_idx = -1

    for i, digit in enumerate(line[:-1]):
        if int(digit) > max_digit: 
            max_digit = int(digit)
            max_digit_idx = i
        if max_digit == 9: break
    
    result += str(max_digit)
    
    max_digit = 0
    for i, digit in enumerate(line[max_digit_idx+1:]):
        if int(digit) > max_digit: 
            max_digit = int(digit)
        if max_digit == 9: break
    result += str(max_digit)

    return int(result)

def find_max_joltage_n(line: str, n: int = 12) -> int:
    result = ""
    max_digit = 0
    max_digit_idx = -1

    for i, digit in enumerate(line[:-(n-1)] if n > 1 else line):
        if int(digit) > max_digit: 
            max_digit = int(digit)
            max_digit_idx = i
        if max_digit == 9: break
    
    result += str(max_digit)
    
    if n == 1:
        return int(result)

    result += str(find_max_joltage_n(line[max_digit_idx+1:], n-1))

    return int(result)

        

def part1(input_file, debug=False):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()
    
    # calculate result
    result = 0
    for line in puzzle_input:
        line = line.strip()
        m = find_max_joltage_n(line, 2)
        if debug: print(m)
        result += m
    
    # return result
    return result

def part2(input_file, debug=False):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()
    
    # calculate result
    result = 0
    for line in puzzle_input:
        line = line.strip()
        m = find_max_joltage_n(line, 12)
        if debug: print(m)
        result += m
    
    # return result
    return result
