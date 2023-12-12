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

def part1(input_file):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()
    
    # print(result)
    # return result



if __name__ == "__main__":
    DIRECTORY = os.path.dirname(__file__)
    PUZZLE_INPUT_PATH = os.path.join(DIRECTORY, "puzzle_input.txt")
    TEST_INPUT_PATH = os.path.join(DIRECTORY, "test_input.txt")
    SESSION_ID = load_session_id(DIRECTORY)
    
    # part 1
    # assert part1(TEST_INPUT_PATH) == 114
    # P1_SOLUTION = part1(PUZZLE_INPUT_PATH)

    # submit solution
    # submit(P1_SOLUTION, SESSION_ID, 1)