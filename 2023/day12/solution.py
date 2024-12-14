import re

def part1(input_file):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()

    springs_groups = []
    # parse input
    for line in puzzle_input:
        springs, groups = re.sub("\n", "", line).split(" ")
        springs = re.sub("\\.+", ".", springs)  # normalize by combining multiple dots to 1 (not necessairy)
        groups = [int(n) for n in groups.split(",")]
        springs_groups.append([springs, groups])

    result = 0
    for s_p in springs_groups:
        springs = s_p[0]
        groups = s_p[1]
        r = get_num_arrangements(springs, groups)
        # print(r)
        result += r

    return result

def part2(input_file):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()

    springs_groups = []
    # parse input
    for line in puzzle_input:
        springs, groups = re.sub("\n", "", line).split(" ")
        springs = re.sub("\\.+", ".", springs)  # normalize by combining multiple dots to 1 (not necessairy)
        springs = "?".join(5 * [springs])
        groups = 5 * [int(n) for n in groups.split(",")]
        springs_groups.append([springs, groups])

    result = 0
    for s_p in springs_groups:
        springs = s_p[0]
        groups = s_p[1]
        r = get_num_arrangements2(springs, groups)
        # print(r)
        result += r

    return result


def get_num_arrangements(springs, groups):
    # base cases
    hash_count = springs.count("#")
    ques_count = springs.count("?")
    sum_groups = sum(groups)
    if hash_count > sum_groups:
        # print(springs)
        return 0
    if ques_count == 0:
        # print(springs)
        if hash_count != sum_groups:
            # print(springs)
            return 0
        springs_matches = re.findall("#+", "".join(springs))
        if len(springs_matches) != len(groups) or any(
                len(springs_matches[i]) != groups[i] for i in range(len(springs_matches))):
            # print(springs)
            return 0
        # print(springs)
        return 1

    tmp_springs = [s for s in springs]
    result = 0
    for i in range(len(tmp_springs)):
        if tmp_springs[i] == "?":
            tmp_springs[i] = "#"
            result += get_num_arrangements(tmp_springs, groups)
            tmp_springs[i] = "."
    result += get_num_arrangements(tmp_springs, groups)

    return result


def get_num_arrangements2(springs, groups):
    # print("".join(springs))
    # base cases
    hash_count = springs.count("#")
    ques_count = springs.count("?")
    sum_groups = sum(groups)
    if hash_count > sum_groups:
        # print(springs)
        return 0
    if ques_count == 0:
        # print(springs)
        if hash_count != sum_groups:
            # print(springs)
            return 0
        springs_matches = re.findall("#+", "".join(springs))
        if len(springs_matches) != len(groups) or any(
                len(springs_matches[i]) != groups[i] for i in range(len(springs_matches))):
            # print(springs)
            return 0
        # print(springs)
        return 1

    groups_idx = 0
    hash_count = 0
    for s in springs:
        if s == "#":
            if hash_count == groups[groups_idx]:
                return 0
            hash_count += 1
            continue
        elif s == "?":
            break
        elif hash_count == 0:
            continue
        elif hash_count == groups[groups_idx]:
            groups_idx += 1
            hash_count = 0
        else:
            return 0

    # print("---")

    tmp_springs = [s for s in springs]
    if hash_count != 0:
        i = "".join(tmp_springs).find("?")
        if i == -1:
            return 0
        for j in range(groups[groups_idx] - hash_count):
            tmp_springs[i + j] = "#"
        return get_num_arrangements(tmp_springs, groups)

    result = 0
    # print(len(tmp_springs), groups[groups_idx], len(tmp_springs) - groups[groups_idx])
    for i in range(len(tmp_springs) - groups[groups_idx]):
        if tmp_springs[i] == "?":
            tmp_springs[i] = "#"
            if all(tmp_springs[i + j] == "?" or tmp_springs[i + j] == "?" for j in range(1, groups[groups_idx])):
                old_chars = []
                for j in range(1, groups[groups_idx]):
                    old_chars.append(tmp_springs[i + j])
                    tmp_springs[i + j] = "#"
                result += get_num_arrangements2(tmp_springs, groups)
                for j in range(1, groups[groups_idx]):
                    tmp_springs[i + j] = old_chars[j - 1]
            tmp_springs[i] = "."
        elif tmp_springs[i] == "#":
            break
    # result += get_num_arrangements(tmp_springs, groups)

    return result