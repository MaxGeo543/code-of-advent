from datetime import datetime
from util.util import load_session_id, get_puzzle_description, get_puzzle_input
import os
import sys
from rich import print

SOLUTION_FILE_TEMPLATE = ("def part1(input_file):",
                          "    # load the puzzle input into a variable",
                          "    with open(input_file, \"r\") as file:",
                          "        puzzle_input = file.readlines()",
                          "    ",
                          "    # calculate result",
                          "    result = \"\"",
                          "    ",
                          "    # return result",
                          "    return result",
                          "",
                          "def part2(input_file):",
                          "    # load the puzzle input into a variable",
                          "    with open(input_file, \"r\") as file:",
                          "        puzzle_input = file.readlines()",
                          "    ",
                          "    # calculate result",
                          "    result = \"\"",
                          "    ",
                          "    # return result",
                          "    return result",
                          "")

TESTS_FILE_TEMPLATE = ("import os",
                       "",
                       "DIRECTORY = os.path.dirname(__file__)",
                       "",
                       "PART_1_TESTS = [",
                       "    # (os.path.join(DIRECTORY, \"test_input.txt\"), 0)",
                       "]",
                       "",
                       "PART_2_TESTS = [",
                       "    # (os.path.join(DIRECTORY, \"test_input.txt\"), 0)",
                       "]",
                       "")

def print_usage():
    print("Usage:")
    print("  python get_puzzle.py <year> <day> [session_id]")
    print("or")
    print("  python get_puzzle.py <year1>-<year2> <day1>-<day2> [session_id]")
    print()
    print("Arguments:")
    print("  <year>       The year of the puzzle (e.g., 2024)")
    print("  <day>        The day of the puzzle (1-25, for December puzzles)")
    print("  [session_id] Optional session ID for authentication (if not provided, it will load a saved session ID)")
    print()
    print("Description:")
    print("  This script sets up files for solving daily puzzles, such as Advent of Code challenges.")
    print(
        "  If no arguments are provided, it will attempt to get today's date, but only if it is between December 1 and 25.")
    print()
    print("Examples:")
    print("  python get_puzzle.py 2024 1")
    print("  python get_puzzle.py 2024 1 YOUR_SESSION_ID")

def main(argc: int, argv: list[str]):
    session_id = None

    dates_to_create = []

    # initialize for specified days
    if argc > 1:
        # error handling
        if argc < 3 or argc > 4:
            print_usage()
            exit(1)

        # parse the date
        # get the years from first arg
        years = argv[1].split("-")
        min_year, max_year = int((years + [years[0]])[0]), int((years + [years[0]])[1])
        # get the days from second arg
        days = argv[2].split("-")
        min_day, max_day = int((days + [days[0]])[0]), int((days + [days[0]])[1])

        # add dates to range
        for year in range(min_year, max_year+1):
            for day in range(min_day, max_day + 1):
                dates_to_create.append((year, day))

        # load the session_id
        if argc == 4:
            session_id = argv[3]
        else:
            session_id = load_session_id()

        # error handling
        if session_id is None:
            print("No session_id found. Please create such a file or provide the Session id as a Command line argument. ")
            exit(1)

    # initialize directory for current day
    else:
        # get today's date
        year, month, day = [int(s) for s in datetime.today().strftime('%Y-%m-%d').split("-")]
        session_id = load_session_id()

        # error handling
        if month != 12:
            print("It's not december yet. Return in december")
            exit(1)
        if day > 25:
            print(f"Christmas is over. Return in {year+1}")
            exit(1)

        dates_to_create.append((year, day))

    # create directories and files
    cwd = os.path.dirname(__file__)

    # loop over all dates
    for date in dates_to_create:
        year, day = date
        day_dir = os.path.join(cwd, str(year), "day"+str(day))

        # if the directory does not exist, create it and initialize all files
        if not os.path.exists(day_dir):
            print(f"Creating directory for {year} day {day}")

            # define file names
            solution_file = os.path.join(day_dir, "solution.py")
            tests_file = os.path.join(day_dir, "tests.py")
            puzzle_input_file = os.path.join(day_dir, "puzzle_input.txt")
            template_file = os.path.join(cwd, "template.py")
            description_file = os.path.join(day_dir, "puzzle_description.txt")

            # puzzle_input file
            puzzle_input = get_puzzle_input(year, day, session_id)
            if puzzle_input is None:
                print("Session expired. please get a new session token.")
                quit(1)

            # description file
            # part I
            description = get_puzzle_description(year, day, 1, session_id)
            if description is None:
                print("Error retrieving puzzle description.")
                quit(1)
            # part II - only if able to fetch it
            description2 = get_puzzle_description(year, day, 2, session_id)
            if description2 is not None:
                description += "\n" + description2

            # create the day directory
            os.makedirs(day_dir)

            # write solution file
            with open(solution_file, "w") as py:
                py_content = "\n".join(SOLUTION_FILE_TEMPLATE)
                py.write(py_content)

            # write tests file
            with open(tests_file, "w") as py:
                py_content = "\n".join(TESTS_FILE_TEMPLATE)
                py.write(py_content)

            # write description file
            with open(description_file, "a") as file:
                content = description
                file.write(content)

            # write input file
            with open(puzzle_input_file, "w") as file:
                file.write(puzzle_input)
        else:
            print(f"[yellow]Directory already exists, skipping year {year} day {day}[/yellow]")

if __name__=="__main__":
    main(len(sys.argv), sys.argv)
