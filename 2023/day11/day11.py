'''
--- Day 11: Cosmic Expansion ---You continue following signs for "Hot Springs" and eventually come across an observatory. The Elf within turns out to be a researcher studying cosmic expansion using the giant telescope here.
He doesn't know anything about the missing machine parts; he's only visiting for this research project. However, he confirms that the hot springs are the next-closest area likely to have people; he'll even take you straight there once he's done with today's observation analysis.
Maybe you can help him with the analysis to speed things up?
The researcher has collected a bunch of data and compiled the data into a single giant image (your puzzle input). The image includes empty space (.) and galaxies (#). For example:
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....

The researcher is trying to figure out the sum of the lengths of the shortest path between every pair of galaxies. However, there's a catch: the universe expanded in the time it took the light from those galaxies to reach the observatory.
Due to something involving gravitational effects, only some space expands. In fact, the result is that any rows or columns that contain no galaxies should all actually be twice as big.
In the above example, three columns and two rows contain no galaxies:
   v  v  v
 ...#......
 .......#..
 #.........
>..........<
 ......#...
 .#........
 .........#
>..........<
 .......#..
 #...#.....
   ^  ^  ^

These rows and columns need to be twice as big; the result of cosmic expansion therefore looks like this:
....#........
.........#...
#............
.............
.............
........#....
.#...........
............#
.............
.............
.........#...
#....#.......

Equipped with this expanded universe, the shortest path between every pair of galaxies can be found. It can help to assign every galaxy a unique number:
....1........
.........2...
3............
.............
.............
........4....
.5...........
............6
.............
.............
.........7...
8....9.......

In these 9 galaxies, there are 36 pairs. Only count each pair once; order within the pair doesn't matter. For each pair, find any shortest path between the two galaxies using only steps that move up, down, left, or right exactly one . or # at a time. (The shortest path between two galaxies is allowed to pass through another galaxy.)
For example, here is one of the shortest paths between galaxies 5 and 9:
....1........
.........2...
3............
.............
.............
........4....
.5...........
.##.........6
..##.........
...##........
....##...7...
8....9.......

This path has length 9 because it takes a minimum of nine steps to get from galaxy 5 to galaxy 9 (the eight locations marked # plus the step onto galaxy 9 itself). Here are some other example shortest path lengths:

Between galaxy 1 and galaxy 7: 15
Between galaxy 3 and galaxy 6: 17
Between galaxy 8 and galaxy 9: 5

In this example, after expanding the universe, the sum of the shortest path between all 36 pairs of galaxies is 374.
Expand the universe, then find the length of the shortest path between every pair of galaxies. What is the sum of these lengths?

--- Part Two ---

The galaxies are much older (and thus much farther apart) than the researcher initially estimated.

Now, instead of the expansion you did before, make each empty row or column one million times larger. That is, each empty row should be replaced with 1000000 empty rows, and each empty column should be replaced with 1000000 empty columns.

(In the example above, if each empty row or column were merely 10 times larger, the sum of the shortest paths between every pair of galaxies would be 1030. If each empty row or column were merely 100 times larger, the sum of the shortest paths between every pair of galaxies would be 8410. However, your universe will need to expand far beyond these values.)

Starting with the same initial image, expand the universe according to these new rules, then find the length of the shortest path between every pair of galaxies. What is the sum of these lengths?

'''

import subprocess
import os
import requests
import re


def submit(result, session_id, part):
    # Get current directory
    current_directory = os.path.dirname(__file__).replace(os.sep, '/')
    
    # Extract YEAR and DAYOFMONTH from the current directory
    year = current_directory.split("/")[-2]
    day_of_month = re.sub("day", "", current_directory.split("/")[-1])
    
    print(f"YEAR IS {year}")
    print(f"DAY IS {day_of_month}")
    
    # Get clipboard content
    tosubmit = str(result)
    print(f"GOING TO SUBMIT {tosubmit}")

    # Make POST request to Advent of Code API
    url = f"https://adventofcode.com/{year}/day/{day_of_month}/answer"
    payload = {"level": str(part), "answer": tosubmit}
    cookies = {"session": session_id}
    response = requests.post(url, data=payload, cookies=cookies)

    if response.status_code != 200:
        print("Error posting answer. ")
        print(response.text)
        return False

    if "s the right answer" in response.text:
        print("CORRECT ANSWER")
        return True
    print(response.text)
    print("Something went wrong. Maybe you already solved this puzzle or you can't solve this puzzle yet. ")
    return False

def load_session_id(start_dir):
    current_dir = start_dir

    while True:
        session_file_path = os.path.join(current_dir, 'session.txt')

        if os.path.isfile(session_file_path):
            # Found the session.txt file, load its content
            with open(session_file_path, 'r') as session_file:
                session_token = session_file.read().strip()
                return session_token

        # Move to the parent directory
        parent_dir = os.path.dirname(current_dir)

        # Check if we have reached the root directory
        if parent_dir == current_dir:
            break

        current_dir = parent_dir

    # If no session.txt file is found in any parent directory
    return None

def is_between(num, a, b):
    return (a < b and a < num and num < b) or (b < a and b < num and num < a)

def part1(input_file):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()
    
    width = len(puzzle_input[0]) - 1
    height = len(puzzle_input)

    empty_rows = []
    empty_cols = []
    for i in range(height):
        if not "#" in puzzle_input[i]:
            empty_rows.append(i)
    for i in range(width):
        if all(puzzle_input[j][i] != "#" for j in range(height)):
            empty_cols.append(i)
    
    galaxies = []
    for y in range(height):
        for x in range(width):
            if puzzle_input[y][x] == "#":
                galaxies.append((x,y))
    
    result = 0
    for i in range(len(galaxies)):
        for j in range(i+1, len(galaxies)):
            
            g1 = galaxies[i]
            g2 = galaxies[j]
            distance = abs(g1[0] - g2[0]) + abs(g1[1] - g2[1])
            for row in empty_rows:
                if is_between(row, g1[1], g2[1]):
                    distance += 1
            for col in empty_cols:
                if is_between(col, g1[0], g2[0]):
                    distance += 1
            result += distance


    
    print(result)
    return result

def part2(input_file, empty_size=1000000):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()
    
    width = len(puzzle_input[0]) - 1
    height = len(puzzle_input)

    empty_rows = []
    empty_cols = []
    for i in range(height):
        if not "#" in puzzle_input[i]:
            empty_rows.append(i)
    for i in range(width):
        if all(puzzle_input[j][i] != "#" for j in range(height)):
            empty_cols.append(i)
    
    galaxies = []
    for y in range(height):
        for x in range(width):
            if puzzle_input[y][x] == "#":
                galaxies.append((x,y))
    
    result = 0
    for i in range(len(galaxies)):
        for j in range(i+1, len(galaxies)):
            
            g1 = galaxies[i]
            g2 = galaxies[j]
            distance = abs(g1[0] - g2[0]) + abs(g1[1] - g2[1])
            for row in empty_rows:
                if is_between(row, g1[1], g2[1]):
                    distance += empty_size -1
            for col in empty_cols:
                if is_between(col, g1[0], g2[0]):
                    distance += empty_size -1
            result += distance


    
    print(result)
    return result

if __name__ == "__main__":
    DIRECTORY = os.path.dirname(__file__)
    PUZZLE_INPUT_PATH = os.path.join(DIRECTORY, "puzzle_input.txt")
    TEST_INPUT_PATH = os.path.join(DIRECTORY, "test_input.txt")
    SESSION_ID = load_session_id(DIRECTORY)
    
    # part 1
    assert part1(TEST_INPUT_PATH) == 374
    P1_SOLUTION = part1(PUZZLE_INPUT_PATH) # 10490062

    assert part2(TEST_INPUT_PATH, 10) == 1030
    assert part2(TEST_INPUT_PATH, 100) == 8410
    P2_SOLUTION = part2(PUZZLE_INPUT_PATH) # 382979724122

    # submit solution
    # submit(P2_SOLUTION, SESSION_ID, 2)