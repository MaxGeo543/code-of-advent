'''
--- Day 10: Pipe Maze ---
You use the hang glider to ride the hot air from Desert Island all the way up to the floating metal island. This island is surprisingly cold and there definitely aren't any thermals to glide on, so you leave your hang glider behind.
You wander around for a while, but you don't find any people or animals. However, you do occasionally find signposts labeled "Hot Springs" pointing in a seemingly consistent direction; maybe you can find someone at the hot springs and ask them where the desert-machine parts are made.
The landscape here is alien; even the flowers and trees are made of metal. As you stop to admire some metal grass, you notice something metallic scurry away in your peripheral vision and jump into a big pipe! It didn't look like any animal you've ever seen; if you want a better look, you'll need to get ahead of it.
Scanning the area, you discover that the entire field you're standing on is densely packed with pipes; it was hard to tell at first because they're the same metallic silver color as the "ground". You make a quick sketch of all of the surface pipes you can see (your puzzle input).
The pipes are arranged in a two-dimensional grid of tiles:

| is a vertical pipe connecting north and south.
- is a horizontal pipe connecting east and west.
L is a 90-degree bend connecting north and east.
J is a 90-degree bend connecting north and west.
7 is a 90-degree bend connecting south and west.
F is a 90-degree bend connecting south and east.
. is ground; there is no pipe in this tile.
S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.

Based on the acoustics of the animal's scurrying, you're confident the pipe that contains the animal is one large, continuous loop.
For example, here is a square loop of pipe:
.....
.F-7.
.|.|.
.L-J.
.....

If the animal had entered this loop in the northwest corner, the sketch would instead look like this:
.....
.S-7.
.|.|.
.L-J.
.....

In the above diagram, the S tile is still a 90-degree F bend: you can tell because of how the adjacent pipes connect to it.
Unfortunately, there are also many pipes that aren't connected to the loop! This sketch shows the same loop as above:
-L|F7
7S-7|
L|7||
-L-J|
L|-JF

In the above diagram, you can still figure out which pipes form the main loop: they're the ones connected to S, pipes those pipes connect to, pipes those pipes connect to, and so on. Every pipe in the main loop connects to its two neighbors (including S, which will have exactly two pipes connecting to it, and which is assumed to connect back to those two pipes).
Here is a sketch that contains a slightly more complex main loop:
..F7.
.FJ|.
SJ.L7
|F--J
LJ...

Here's the same example sketch with the extra, non-main-loop pipe tiles also shown:
7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ

If you want to get out ahead of the animal, you should find the tile in the loop that is farthest from the starting position. Because the animal is in the pipe, it doesn't make sense to measure this by direct distance. Instead, you need to find the tile that would take the longest number of steps along the loop to reach from the starting point - regardless of which way around the loop the animal went.
In the first example with the square loop:
.....
.S-7.
.|.|.
.L-J.
.....

You can count the distance each tile in the loop is from the starting point like this:
.....
.012.
.1.3.
.234.
.....

In this example, the farthest point from the start is 4 steps away.
Here's the more complex loop again:
..F7.
.FJ|.
SJ.L7
|F--J
LJ...

Here are the distances for each tile on that loop:
..45.
.236.
01.78
14567
23...

Find the single giant loop starting at S. How many steps along the loop does it take to get from the starting position to the point farthest from the starting position?

--- Part Two ---

You quickly reach the farthest point of the loop, but the animal never emerges. Maybe its nest is within the area enclosed by the loop?

To determine whether it's even worth taking the time to search for such a nest, you should calculate how many tiles are contained within the loop. For example:

...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........

The above loop encloses merely four tiles - the two pairs of . in the southwest and southeast (marked I below). The middle . tiles (marked O below) are not in the loop. Here is the same loop again with those regions marked:

...........
.S-------7.
.|F-----7|.
.||OOOOO||.
.||OOOOO||.
.|L-7OF-J|.
.|II|O|II|.
.L--JOL--J.
.....O.....

In fact, there doesn't even need to be a full tile path to the outside for tiles to count as outside the loop - squeezing between pipes is also allowed! Here, I is still within the loop and O is still outside the loop:

..........
.S------7.
.|F----7|.
.||OOOO||.
.||OOOO||.
.|L-7F-J|.
.|II||II|.
.L--JL--J.
..........

In both of the above examples, 4 tiles are enclosed by the loop.

Here's a larger example:

.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...

The above sketch has many random bits of ground, some of which are in the loop (I) and some of which are outside it (O):

OF----7F7F7F7F-7OOOO
O|F--7||||||||FJOOOO
O||OFJ||||||||L7OOOO
FJL7L7LJLJ||LJIL-7OO
L--JOL7IIILJS7F-7L7O
OOOOF-JIIF7FJ|L7L7L7
OOOOL7IF7||L7|IL7L7|
OOOOO|FJLJ|FJ|F7|OLJ
OOOOFJL-7O||O||||OOO
OOOOL---JOLJOLJLJOOO

In this larger example, 8 tiles are enclosed by the loop.

Any tile that isn't part of the main loop can count as being enclosed by the loop. Here's another example with many bits of junk pipe lying around that aren't connected to the main loop at all:

FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L

Here are just the tiles that are enclosed by the loop marked with I:

FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJIF7FJ-
L---JF-JLJIIIIFJLJJ7
|F|F-JF---7IIIL7L|7|
|FFJF7L7F-JF7IIL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L

In this last example, 10 tiles are enclosed by the loop.

Figure out whether you have time to search for the nest by calculating the area within the loop. How many tiles are enclosed by the loop?

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

# puzzle solution
def part1(input_file):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()
    
    # pad input with . to avoid idx nound checks
    puzzle_input = [(len(puzzle_input[0])-1) * "." + "\n"] + puzzle_input
    for line in puzzle_input:
        line = "." + re.sub("\n", "", line) + ".\n"


    x = 0
    y = 0
    steps = 0
    current_char = "S"
    direction = 0 # 0,1,2,3 -> top,left,down,right
    # find Start
    for i in range(len(puzzle_input)):
        s_idx = puzzle_input[i].find("S")
        if s_idx != -1:
            y = i
            x = s_idx
            break

    start_pos_x = x
    start_pos_y = y
    while True:
        # treat first move differently, cause we don't know which symbol is under 'S'
        if x == start_pos_x and y == start_pos_y:
            below = puzzle_input[y+1][x]
            above = puzzle_input[y-1][x]
            right = puzzle_input[y][x+1]
            left = puzzle_input[y][x-1]
            
            if above in "|7F":
                y -= 1
                direction = "|7.F".find(above)
            elif left in ["-", "F", "L"]:
                x -= 1
                direction = "L-F.".find(left)
            elif below in ["|", "J", "L"]:
                y += 1
                direction = ".J|L".find(below)
            elif right in "7J-":
                x += 1
                direction = "J.7-".find(right)
        else:
            if direction == 0:
                y -= 1
                direction = "|7.F".find(puzzle_input[y][x])
            elif direction == 1:
                x -= 1
                direction = "L-F.".find(puzzle_input[y][x])
            elif direction == 2:
                y += 1
                direction = ".J|L".find(puzzle_input[y][x])
            elif direction == 3:
                x += 1
                direction = "J.7-".find(puzzle_input[y][x])
        steps += 1
        if x == start_pos_x and y == start_pos_y:
            break

    result = int(steps/2)
    print(result)
    return result

def part2(input_file):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()
    
    linelen = len(puzzle_input[0]) - 1
    # pad input with dots to avoid index bound checking
    puzzle_input = [linelen * "." + "\n"] + puzzle_input
    for line in puzzle_input:
        line = "." + re.sub("\n", "", line) + ".\n"
    linelen = len(puzzle_input[0]) - 1

    x = 0
    y = 0
    steps = 0
    current_char = "S"
    direction = 0 # 0,1,2,3 -> top,left,down,right

    # find Start
    for i in range(len(puzzle_input)):
        s_idx = puzzle_input[i].find("S")
        if s_idx != -1:
            y = i
            x = s_idx
            break
    start_pos_x = x
    start_pos_y = y
    # get list of coordinates of loop
    loop_coordinates = []
    while True:
        loop_coordinates.append((x, y))
        if x == start_pos_x and y == start_pos_y:
            below = puzzle_input[y+1][x]
            above = puzzle_input[y-1][x]
            right = puzzle_input[y][x+1]
            left = puzzle_input[y][x-1]
            
            if above in "|7F":
                y -= 1
                direction = "|7.F".find(above)
            elif left in ["-", "F", "L"]:
                x -= 1
                direction = "L-F.".find(left)
            elif below in ["|", "J", "L"]:
                y += 1
                direction = ".J|L".find(below)
            elif right in "7J-":
                x += 1
                direction = "J.7-".find(right)
        else:
            if direction == 0:
                y -= 1
                direction = "|7.F".find(puzzle_input[y][x])
            elif direction == 1:
                x -= 1
                direction = "L-F.".find(puzzle_input[y][x])
            elif direction == 2:
                y += 1
                direction = ".J|L".find(puzzle_input[y][x])
            elif direction == 3:
                x += 1
                direction = "J.7-".find(puzzle_input[y][x])
        steps += 1
        if x == start_pos_x and y == start_pos_y:
            break


    result = 0
    count_mask = [False] * linelen
    for y in range(len(puzzle_input)):
        line = puzzle_input[y]
        for x in range(linelen):
            if count_mask[x] and not (x,y) in loop_coordinates:
                result += 1
            if (x,y) in loop_coordinates and line[x] not in "S|J7":
                count_mask[x] = not count_mask[x]
    
    print(result)
    return result



if __name__ == "__main__":
    DIRECTORY = os.path.dirname(__file__)
    PUZZLE_INPUT_PATH = os.path.join(DIRECTORY, "puzzle_input.txt")
    TEST_INPUT_PATH = os.path.join(DIRECTORY, "test_input.txt")
    TEST_INPUT_PATH_2 = os.path.join(DIRECTORY, "test_input_2.txt")
    SESSION_ID = load_session_id(DIRECTORY)
    
    # part 1
    assert part1(TEST_INPUT_PATH) == 8
    P1_SOLUTION = part1(PUZZLE_INPUT_PATH) # 6956

    # part 2
    assert part2(TEST_INPUT_PATH_2) == 10
    P2_SOLUTION = part2(PUZZLE_INPUT_PATH) # 455 relatively slow though, also there might be a missing edge case I forgot...

    # submit solution
    # submit(P2_SOLUTION, SESSION_ID, 2)