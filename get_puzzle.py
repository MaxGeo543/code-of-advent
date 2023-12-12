from datetime import datetime
import shutil
import subprocess
import os
import requests
import sys
from bs4 import BeautifulSoup

def load_session_id():
    session_file = os.path.join(os.path.dirname(__file__), "session.txt")
    if not os.path.exists(session_file):
        print("'session.txt' not found. please create such a file or provide the Session id as a Command line argument. ")
        print_usage()
        exit(1)
    with open(session_file, "r") as file:
        session_id = file.read().strip()
    return session_id

def print_usage():
    pass

def main(argc, argv):
    if argc > 1:
        if argc < 3 or argc > 4:
            print("USAGE")
            exit(1)
        year = int(argv[1])
        day = int(argv[2])
        if argc == 4:
            SESSION_ID = argv[3]
        else:
            SESSION_ID = load_session_id()
    else:
        year, month, day = [int(s) for s in datetime.today().strftime('%Y-%m-%d').split("-")]
        SESSION_ID = load_session_id()

        if month != 12:
            print("It's not december yet. Return in december")
            exit(1)

        if day > 25:
            print(f"Christmas is over. Return in {year+1}")
            exit(1)

    # create directories and files
    cwd = os.path.dirname(__file__)
    day_dir = os.path.join(cwd, str(year), "day"+str(day))

    if not os.path.exists(day_dir):
        print(f"Creating directory for {year} day {day}")
        day_file = os.path.join(day_dir, "day"+str(day)+".py")
        puzzle_input_file = os.path.join(day_dir, "puzzle_input.txt")
        test_input_file = os.path.join(day_dir, "test_input.txt")
        template_file = os.path.join(cwd, "template.py")
        if not os.path.exists(template_file):
            print("template.py file does not exist. What have you done??")
            exit(1)

        os.makedirs(day_dir)
        
        # write python file
        with open(template_file, "r") as template:
            with open(day_file, "w") as py:
                puzzle_desc = get_puzzle_description(year, day, SESSION_ID)
                py_content = ""
                if puzzle_desc != None:
                    py_content += "'''\n" + puzzle_desc + "'''\n\n"
                py_content += template.read()

                py.write(py_content)

        with open(puzzle_input_file, "w") as file:
            file.write(get_puzzle_input(year, day, SESSION_ID))
    else:
        print("not creating")

def get_puzzle_input(year, day, session_token):
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    cookies = {"session": session_token}
    response = requests.get(url, cookies=cookies)

    return response.text

def get_puzzle_description(year, day, session_token):
    url = f"https://adventofcode.com/{year}/day/{day}"
    cookies = {"session": session_token}
    response = requests.get(url, cookies=cookies)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        target_element = soup.find("article", "day-desc")
        if target_element != None:
            return target_element.text

if __name__=="__main__":
    main(len(sys.argv), sys.argv)
