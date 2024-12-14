import re

def map(dst_start, src_start, length, x):
    if src_start > x or src_start + length <= x:
        return x

    return dst_start + x - src_start


def num_in_range(ra, num):
    if num >= ra[0] and num < ra[0] + ra[1]:
        return True
    return False


def map_range(mapping, ra):
    ra_first = ra[0]
    ra_last = ra[0] + ra[1] - 1
    ma_first = mapping[1]
    ma_last = mapping[1] + mapping[2] - 1

    r_map = lambda x: map(mapping[0], mapping[1], mapping[2], x)

    # if the input range has no special mapping
    if (ra_first < ma_first and ra_last < ma_first) or (ra_first > ma_last and ra_last > ma_last):
        ra_from = ra
        ra_to = ra
        return [(ra_from, ra_to)]

    # if the input mapping is completely mapped
    if (ra_first >= ma_first and ra_last <= ma_last):
        ra_from = (ra[0], ra[1])
        ra_to = (r_map(ra[0]), ra[1])
        return [(ra_from, ra_to)]

    # if the first part of the range gets mapped, but second part not
    if (ra_first >= ma_first and ra_first <= ma_last) and (ra_last > ma_last):
        result = []

        length1 = ma_last - ra_first + 1
        ra_from = (ra_first, length1)
        ra_to = (r_map(ra_first), length1)
        result.append((ra_from, ra_to))

        length2 = ra[1] - length1
        ra_from = (ma_last + 1, length2)
        ra_to = (ma_last + 1, length2)
        result.append((ra_from, ra_to))

        return result

    # if the second part of the range gets mapped, but first part not
    if (ra_first < ma_first) and (ra_last <= ma_last and ra_last >= ma_first):
        result = []

        length1 = ma_first - ra_first
        ra_from = (ra_first, length1)
        ra_to = (ra_first, length1)
        result.append((ra_from, ra_to))

        length2 = ra[1] - length1
        ra_from = (ma_first, length2)
        ra_to = (r_map(ma_first), length2)
        result.append((ra_from, ra_to))

        return result

    # if the beginning and end do not get mapped, but a part in the middle does
    if (ra_first < ma_first and ra_last > ma_last):
        result = []

        length1 = ma_first - ra_first
        ra_from = (ra_first, length1)
        ra_to = (ra_first, length1)
        result.append((ra_from, ra_to))

        length2 = ra_last - ma_last
        ra_from = (ma_last + 1, length2)
        ra_to = (ma_last + 1, length2)
        result.append((ra_from, ra_to))

        length3 = ra[1] - length1 - length2
        ra_from = (ma_first, length3)
        ra_to = (r_map(ma_first), length3)
        result.append((ra_from, ra_to))

        return result

    return []


# map() works perfectly fine for part1 but for part2 there are toooo many seeds due to the ranges
# map2() tries to solve this by taking ranges as input and outputting ranges as well
# mappings is the list of all mappings of a specific type
# input_ranges is a list of ranges as tuples (start, length)
def map_range_multmap(mappings, ra):
    output_ranges = []
    mappings.sort(key=lambda x: x[1])  # sort by src_start

    ranges_to_check = [ra]

    for mapping in mappings:
        cont = map_range(mapping, ra)

        for c in cont:
            if c[0] == c[1] and c[1] != ra:
                rec_out = map_range_multmap(mappings, c[1])
                for ro in rec_out:
                    if not ro in output_ranges:
                        output_ranges.append(ro)
            elif c[1] != ra:
                output_ranges.append(c[1])
            else:  # c[1] == ra
                pass

    if len(output_ranges) == 0:
        return [ra]
    else:
        return output_ranges


def part1(input_file):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()

    # parsing the input
    seeds = []
    mappings = {
        "seed-to-soil": [],
        "soil-to-fertilizer": [],
        "fertilizer-to-water": [],
        "water-to-light": [],
        "light-to-temperature": [],
        "temperature-to-humidity": [],
        "humidity-to-location": [],
    }
    line_idx = 0
    while line_idx < len(puzzle_input):
        line = puzzle_input[line_idx]

        if line.startswith("seeds: "):
            seeds = [int(re.sub("\n", "", num)) for num in line[7:].split(" ")]
        else:
            for key in mappings.keys():
                if line.startswith(key):
                    line_idx += 1
                    while line_idx < len(puzzle_input) and not puzzle_input[line_idx].isspace():
                        mappings[key].append([int(re.sub("\n", "", num)) for num in puzzle_input[line_idx].split(" ")])
                        line_idx += 1
                    break
        line_idx += 1

    # finding lowest location number
    result = -1
    for seed in seeds:
        num = seed
        for key in mappings.keys():
            old_num = num
            for mapping in mappings[key]:
                if num == old_num:
                    num = map(mapping[0], mapping[1], mapping[2], num)
                else:
                    break
        if result == -1:
            result = num
        result = min(num, result)

    return result

def part2(input_file):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()

    # parsing the input
    seed_ranges = []
    mappings = {
        "seed-to-soil": [],
        "soil-to-fertilizer": [],
        "fertilizer-to-water": [],
        "water-to-light": [],
        "light-to-temperature": [],
        "temperature-to-humidity": [],
        "humidity-to-location": [],
    }
    line_idx = 0
    while line_idx < len(puzzle_input):
        line = puzzle_input[line_idx]

        if line.startswith("seeds: "):
            seed_ranges = [int(re.sub("\n", "", num)) for num in line[7:].split(" ")]
            seed_ranges = [(seed_ranges[i], seed_ranges[i + 1]) for i in range(0, len(seed_ranges), 2)]
        else:
            for key in mappings.keys():
                if line.startswith(key):
                    line_idx += 1
                    while line_idx < len(puzzle_input) and not puzzle_input[line_idx].isspace():
                        mappings[key].append([int(re.sub("\n", "", num)) for num in puzzle_input[line_idx].split(" ")])
                        line_idx += 1
                    break
        line_idx += 1

    # finding lowest location number
    final_mappings = []
    for seed_ra in seed_ranges:
        final_mappings.append(seed_ra)
    for key in mappings.keys():
        new_mappings = []
        for s in final_mappings:
            new_mappings.extend(map_range_multmap(mappings[key], s))
        final_mappings = new_mappings

    final_mappings.sort(key=lambda x: x[0])
    result = final_mappings[0][0]
    return result
