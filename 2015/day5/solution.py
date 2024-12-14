def part1(input_file):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()

    # calculate result
    nice_count = 0
    for line in puzzle_input:
        if is_nice(line): nice_count += 1
    
    # return result
    return nice_count

def part2(input_file):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()

    # calculate result
    nice_count = 0
    for line in puzzle_input:
        if is_actually_nice(line):
            nice_count += 1

    # return result
    return nice_count


def is_nice(string: str) -> bool:
    vowels = "aeiou"
    forbidden_substrings = ["ab", "cd", "pq", "xy"]
    vowel_count = 0
    double_letter = False
    for i, c in enumerate(string):
        if c in vowels: vowel_count +=1

        if i > 0 and f"{string[i-1]}{c}" in forbidden_substrings:
            return False
        if i > 0 and string[i-1] == c:
            double_letter = True

    if vowel_count < 3: return False
    else: return double_letter

def is_actually_nice(string: str) -> bool:
    letter_sandwich = False
    letter_pairs = {}
    for i in range(len(string)):
        c = string[i]
        # check if there is a sandwich eg. "aka"
        if i > 1 and string[i - 2] == c:
            letter_sandwich = True
        # if the pair appears the first time, calculate the count of it
        if i > 0 and f"{string[i-1]}{c}" not in letter_pairs.keys():
            count = 0
            j = 0
            pair = f"{string[i-1]}{c}"
            while j < len(string) - len(pair):
                if string[j:j + len(pair)] == pair:
                    count += 1
                    j += len(pair)
                else:
                    j += 1
            letter_pairs[f"{string[i-1]}{c}"] = count

    # if any pair appears at least twice
    if any(pair_count >= 2 for pair_count in letter_pairs.values()):
        # return True if a letter sandwich exists
        return letter_sandwich

    # otherwise return False
    return False