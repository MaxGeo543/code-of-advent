def part1(input_file):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()

    result = 0
    for line_idx, line in enumerate(puzzle_input):
        num = ""
        for char_idx, char in enumerate(line):
            if char.isdigit():
                num += char
            elif num != "":
                # check surrounding spaces
                surrounding_chars = []
                num_len = len(num)
                # fill surrounding chars list
                for i in range(char_idx - num_len - 1, char_idx + 1):
                    if i < 0:
                        continue
                    # line above
                    if line_idx > 0:
                        surrounding_chars.append(puzzle_input[line_idx - 1][i])
                    surrounding_chars.append(puzzle_input[line_idx][i])
                    if line_idx < len(puzzle_input) - 1:
                        surrounding_chars.append(puzzle_input[line_idx + 1][i])
                # check surrounding chars list
                if any(not c.isdigit() and c != "." and c != "\n" for c in surrounding_chars):
                    # add to result
                    result += int(num)
                # reset num
                num = ""

    return result

def part2(input_file):
    # given a string and an index, returns the complete number that text[idx] is a part of as well as its starting index
    def get_whole_number(text, idx):
        if not text[idx].isdigit() or idx < 0 or idx >= len(text):
            raise Exception()

        while text[idx].isdigit() and idx != 0:
            idx -= 1

        if not text[idx].isdigit():
            idx += 1

        start_idx = idx
        num = ""
        while text[idx].isdigit() and idx < len(text):
            num += text[idx]
            idx += 1

        return (start_idx, int(num))

    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()

    result = 0
    for line_idx, line in enumerate(puzzle_input):
        for char_idx, char in enumerate(line):
            # skip if char is not a *, we only need to consider *
            if char != "*":
                continue

            # nums is the list of surrounding numbers
            # (actually its a nested tuple with ((line_idx, pos_idx), num)) where line and pos idx are the indeces of the first digit to prevent duplicates)
            nums = []

            # looping over all adjacents, skipping if out of bounds
            i = -1
            while i < 2:
                if i + line_idx < 0 or i + line_idx >= len(puzzle_input):
                    continue
                ii = -1
                while ii < 2:
                    if ii + char_idx < 0 or ii + char_idx >= len(line):
                        continue

                    # what actually happens every iteration
                    maybe_digit = puzzle_input[i + line_idx][ii + char_idx]
                    # if the surrounding char is a digit
                    if maybe_digit.isdigit():
                        # if it is not a duplicate append to nums
                        idx, num = get_whole_number(puzzle_input[i + line_idx], ii + char_idx)
                        if not (i + line_idx, idx) in [n[0] for n in nums]:
                            nums.append(((i + line_idx, idx), num))
                    ii += 1
                i += 1

            # if exactly 2 nums: multiply and add to result
            if len(nums) == 2:
                result += nums[0][1] * nums[1][1]

    return result
