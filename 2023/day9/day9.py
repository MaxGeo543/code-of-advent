'''
--- Day 9: Mirage Maintenance ---
You ride the camel through the sandstorm and stop where the ghost's maps told you to stop. The sandstorm subsequently subsides, somehow seeing you standing at an oasis!
The camel goes to get some water and you stretch your neck. As you look up, you discover what must be yet another giant floating island, this one made of metal! That must be where the parts to fix the sand machines come from.
There's even a hang glider partially buried in the sand here; once the sun rises and heats up the sand, you might be able to use the glider and the hot air to get all the way up to the metal island!
While you wait for the sun to rise, you admire the oasis hidden here in the middle of Desert Island. It must have a delicate ecosystem; you might as well take some ecological readings while you wait. Maybe you can report any environmental instabilities you find to someone so the oasis can be around for the next sandstorm-worn traveler.
You pull out your handy Oasis And Sand Instability Sensor and analyze your surroundings. The OASIS produces a report of many values and how they are changing over time (your puzzle input). Each line in the report contains the history of a single value. For example:
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45

To best protect the oasis, your environmental report should include a prediction of the next value in each history. To do this, start by making a new sequence from the difference at each step of your history. If that sequence is not all zeroes, repeat this process, using the sequence you just generated as the input sequence. Once all of the values in your latest sequence are zeroes, you can extrapolate what the next value of the original history should be.
In the above dataset, the first history is 0 3 6 9 12 15. Because the values increase by 3 each step, the first sequence of differences that you generate will be 3 3 3 3 3. Note that this sequence has one fewer value than the input sequence because at each step it considers two numbers from the input. Since these values aren't all zero, repeat the process: the values differ by 0 at each step, so the next sequence is 0 0 0 0. This means you have enough information to extrapolate the history! Visually, these sequences can be arranged like this:
0   3   6   9  12  15
  3   3   3   3   3
    0   0   0   0

To extrapolate, start by adding a new zero to the end of your list of zeroes; because the zeroes represent differences between the two values above them, this also means there is now a placeholder in every sequence above it:
0   3   6   9  12  15   B
  3   3   3   3   3   A
    0   0   0   0   0

You can then start filling in placeholders from the bottom up. A needs to be the result of increasing 3 (the value to its left) by 0 (the value below it); this means A must be 3:
0   3   6   9  12  15   B
  3   3   3   3   3   3
    0   0   0   0   0

Finally, you can fill in B, which needs to be the result of increasing 15 (the value to its left) by 3 (the value below it), or 18:
0   3   6   9  12  15  18
  3   3   3   3   3   3
    0   0   0   0   0

So, the next value of the first history is 18.
Finding all-zero differences for the second history requires an additional sequence:
1   3   6  10  15  21
  2   3   4   5   6
    1   1   1   1
      0   0   0

Then, following the same process as before, work out the next value in each sequence from the bottom up:
1   3   6  10  15  21  28
  2   3   4   5   6   7
    1   1   1   1   1
      0   0   0   0

So, the next value of the second history is 28.
The third history requires even more sequences, but its next value can be found the same way:
10  13  16  21  30  45  68
   3   3   5   9  15  23
     0   2   4   6   8
       2   2   2   2
         0   0   0

So, the next value of the third history is 68.
If you find the next value for each history in this example and add them together, you get 114.
Analyze your OASIS report and extrapolate the next value for each history. What is the sum of these extrapolated values?

--- Part Two ---

Of course, it would be nice to have even more history included in your report. Surely it's safe to just extrapolate backwards as well, right?

For each history, repeat the process of finding differences until the sequence of differences is entirely zero. Then, rather than adding a zero to the end and filling in the next values of each previous sequence, you should instead add a zero to the beginning of your sequence of zeroes, then fill in new first values for each previous sequence.

In particular, here is what the third example history looks like when extrapolating back in time:

5  10  13  16  21  30  45
  5   3   3   5   9  15
   -2   0   2   4   6
      2   2   2   2
        0   0   0

Adding the new values on the left side of each sequence from bottom to top eventually reveals the new left-most history value: 5.

Doing this for the remaining example data above results in previous values of -3 for the first history and 0 for the second history. Adding all three new values together produces 2.

Analyze your OASIS report again, this time extrapolating the previous value for each history. What is the sum of these extrapolated values?

'''

import subprocess
import os
import requests
import re
from pathlib import Path

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

def predict_next_value(seq):
    seq_len = len(seq) + 1
    derivatives = [seq]
    while not all(n == 0 for n in derivatives[-1]):
        last_seq = derivatives[-1]
        derivatives.append([last_seq[i]-last_seq[i-1] for i in range(1, len(last_seq))])
    
    for der in derivatives:
        der += (seq_len-len(der))*[0]
    
    derivatives.reverse()

    for i in range(1, len(derivatives)):
        for j in range(1, seq_len):
            derivatives[i][j] = derivatives[i][j-1] + derivatives[i-1][j-1]
    return derivatives[-1][-1]


def part1(input_file):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()
    
    sequences = []
    # parse puzzle input
    for line in puzzle_input:
        sequences.append([int(s.strip()) for s in line.split(" ")])
    
    result = 0
    for seq in sequences:
        result += predict_next_value(seq)

    print(result)
    return result

def part2(input_file):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()
    
    sequences = []
    # parse puzzle input
    for line in puzzle_input:
        sequences.append(list(reversed([int(s.strip()) for s in line.split(" ")])))
    
    result = 0
    for seq in sequences:
        result += predict_next_value(seq)

    print(result)
    return result

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


if __name__ == "__main__":
    DIRECTORY = os.path.dirname(__file__)
    PUZZLE_INPUT_PATH = os.path.join(DIRECTORY, "puzzle_input.txt")
    TEST_INPUT_PATH = os.path.join(DIRECTORY, "test_input.txt")
    SESSION_ID = load_session_id(DIRECTORY)
    
    # part 1
    assert part1(TEST_INPUT_PATH) == 114
    P1_SOLUTION = part1(PUZZLE_INPUT_PATH)

    # part 2
    assert part2(TEST_INPUT_PATH) == 2
    P2_SOULUTION = part2(PUZZLE_INPUT_PATH)

    # submit solution
    # submit(P2_SOLUTION)