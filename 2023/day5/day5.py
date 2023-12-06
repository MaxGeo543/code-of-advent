'''
--- Day 5: If You Give A Seed A Fertilizer ---

You take the boat and find the gardener right where you were told he would be: managing a giant "garden" that looks more to you like a farm.

"A water source? Island Island is the water source!" You point out that Snow Island isn't receiving any water.

"Oh, we had to stop the water because we ran out of sand to filter it with! Can't make snow with dirty water. Don't worry, I'm sure we'll get more sand soon; we only turned off the water a few days... weeks... oh no." His face sinks into a look of horrified realization.

"I've been so busy making sure everyone here has food that I completely forgot to check why we stopped getting more sand! There's a ferry leaving soon that is headed over in that direction - it's much faster than your boat. Could you please go check it out?"

You barely have time to agree to this request when he brings up another. "While you wait for the ferry, maybe you can help us with our food production problem. The latest Island Island Almanac just arrived and we're having trouble making sense of it."

The almanac (your puzzle input) lists all of the seeds that need to be planted. It also lists what type of soil to use with each kind of seed, what type of fertilizer to use with each kind of soil, what type of water to use with each kind of fertilizer, and so on. Every type of seed, soil, fertilizer and so on is identified with a number, but numbers are reused by each category - that is, soil 123 and fertilizer 123 aren't necessarily related to each other.

For example:

seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4

The almanac starts by listing which seeds need to be planted: seeds 79, 14, 55, and 13.

The rest of the almanac contains a list of maps which describe how to convert numbers from a source category into numbers in a destination category. That is, the section that starts with seed-to-soil map: describes how to convert a seed number (the source) to a soil number (the destination). This lets the gardener and his team know which soil to use with which seeds, which water to use with which fertilizer, and so on.

Rather than list every source number and its corresponding destination number one by one, the maps describe entire ranges of numbers that can be converted. Each line within a map contains three numbers: the destination range start, the source range start, and the range length.

Consider again the example seed-to-soil map:

50 98 2
52 50 48

The first line has a destination range start of 50, a source range start of 98, and a range length of 2. This line means that the source range starts at 98 and contains two values: 98 and 99. The destination range is the same length, but it starts at 50, so its two values are 50 and 51. With this information, you know that seed number 98 corresponds to soil number 50 and that seed number 99 corresponds to soil number 51.

The second line means that the source range starts at 50 and contains 48 values: 50, 51, ..., 96, 97. This corresponds to a destination range starting at 52 and also containing 48 values: 52, 53, ..., 98, 99. So, seed number 53 corresponds to soil number 55.

Any source numbers that aren't mapped correspond to the same destination number. So, seed number 10 corresponds to soil number 10.

So, the entire list of seed numbers and their corresponding soil numbers looks like this:

seed  soil
0     0
1     1
...   ...
48    48
49    49
50    52
51    53
...   ...
96    98
97    99
98    50
99    51

With this map, you can look up the soil number required for each initial seed number:

    Seed number 79 corresponds to soil number 81.
    Seed number 14 corresponds to soil number 14.
    Seed number 55 corresponds to soil number 57.
    Seed number 13 corresponds to soil number 13.

The gardener and his team want to get started as soon as possible, so they'd like to know the closest location that needs a seed. Using these maps, find the lowest location number that corresponds to any of the initial seeds. To do this, you'll need to convert each seed number through other categories until you can find its corresponding location number. In this example, the corresponding types are:

    Seed 79, soil 81, fertilizer 81, water 81, light 74, temperature 78, humidity 78, location 82.
    Seed 14, soil 14, fertilizer 53, water 49, light 42, temperature 42, humidity 43, location 43.
    Seed 55, soil 57, fertilizer 57, water 53, light 46, temperature 82, humidity 82, location 86.
    Seed 13, soil 13, fertilizer 52, water 41, light 34, temperature 34, humidity 35, location 35.

So, the lowest location number in this example is 35.

What is the lowest location number that corresponds to any of the initial seed numbers?

--- Part Two ---

Everyone will starve if you only plant such a small number of seeds. Re-reading the almanac, it looks like the seeds: line actually describes ranges of seed numbers.

The values on the initial seeds: line come in pairs. Within each pair, the first value is the start of the range and the second value is the length of the range. So, in the first line of the example above:

seeds: 79 14 55 13

This line describes two ranges of seed numbers to be planted in the garden. The first range starts with seed number 79 and contains 14 values: 79, 80, ..., 91, 92. The second range starts with seed number 55 and contains 13 values: 55, 56, ..., 66, 67.

Now, rather than considering four seed numbers, you need to consider a total of 27 seed numbers.

In the above example, the lowest location number can be obtained from seed number 82, which corresponds to soil 84, fertilizer 84, water 84, light 77, temperature 45, humidity 46, and location 46. So, the lowest location number is 46.

Consider all of the initial seed numbers listed in the ranges on the first line of the almanac. What is the lowest location number that corresponds to any of the initial seed numbers?
'''

import re

from pathlib import Path
mod_path = Path(__file__).parent
PUZZLE_INPUT_PATH = Path(mod_path, "puzzle_input.txt")
TEST_INPUT_PATH = Path(mod_path, "test_input.txt")

def map(dst_start, src_start, length, x):
    if src_start > x or src_start+length <= x:
        return x
    
    return dst_start + x - src_start

def num_in_range(ra, num):
    if num >= ra[0] and num < ra[0]+ra[1]:
        return True
    return False


def map_range(mapping, ra):

    ra_first = ra[0]
    ra_last = ra[0]+ra[1]-1
    ma_first = mapping[1]
    ma_last = mapping[1]+mapping[2]-1

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
    mappings.sort(key=lambda x: x[1]) # sort by src_start
    
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
            else: # c[1] == ra
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

    print(result)
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
            seed_ranges = [(seed_ranges[i], seed_ranges[i+1]) for i in range(0, len(seed_ranges), 2)]
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
    print(result)
    return result

if __name__ == "__main__":
    assert part1(TEST_INPUT_PATH) == 35
    assert part2(TEST_INPUT_PATH) == 46

    part1(PUZZLE_INPUT_PATH) # returned 486613012
    # part2 took me way longer than all other puzzles so far
    # first I underestimated how big the numbers were
    # working with range() and checking all numbers was no longer an option
    # then I created my map_range() function to work with ranges instead
    # at first I struggled to put that together in a logical way
    # but at some point I got it so that the test input passed
    # however I forgot a case so the assert Passed but the actual result was 0
    # this took me roughly a whole day to make it work but now it finally does
    part2(PUZZLE_INPUT_PATH) # returned 56931769