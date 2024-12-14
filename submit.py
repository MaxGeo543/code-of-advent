from util.util import load_session_id
from datetime import datetime
import os
import sys
from rich import print
import importlib.util

from util.util import test as _test, submit as _submit, update_description as _update_description

def print_usage():
    print("Usage:")
    print("  python submit.py <year> <day> [session_id]")
    print()
    print("Arguments:")
    print("  <year>       The year of the puzzle (e.g., 2024)")
    print("  <day>        The day of the puzzle (1-25, for December puzzles)")
    print("  [session_id] Optional session ID for authentication (if not provided, it will load a saved session ID)")
    print()
    print("Description:")
    print("  This script tests and submits solutions Advent of Code.")
    print("  If no arguments are provided, it will attempt to get today's date, but only if it is between December 1 and 25.")
    print()
    print("Examples:")
    print("  python submit.py 2024 1")
    print("  python submit.py 2024 1 YOUR_SESSION_ID")

def load_function(year: int, day: int, part: int):
    """
    loads the part<part> function from ./year/day<day>/solution.py
    returns None if it was not found
    """
    directory = os.path.dirname(__file__)
    day_directory = os.path.join(directory, str(year), f"day{day}")
    if not os.path.exists(day_directory):
        print("[red]Directory for specified day does not exist![/red]")
        quit(1)
    part_path = os.path.join(day_directory, f"solution.py")
    if not os.path.exists(part_path):
        return None
    spec = importlib.util.spec_from_file_location(f"part{part}", part_path)
    part_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(part_module)

    if hasattr(part_module, f"part{part}"):
        return getattr(part_module, f"part{part}")
    else:
        return None

def load_tests(year: int, day: int, part: int):
    """
    loads the PART_<part>_TESTS constants from ./year/day<day>/tests.py
    returns None if it was not found
    """
    directory = os.path.dirname(__file__)
    day_directory = os.path.join(directory, str(year), f"day{day}")
    if not os.path.exists(day_directory):
        print("[red]Directory for specified day does not exist![/red]")
        quit(1)
    tests_path = os.path.join(day_directory, f"tests.py")
    if not os.path.exists(tests_path):
        return None
    spec = importlib.util.spec_from_file_location(f"tests", tests_path)
    tests_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tests_module)

    if hasattr(tests_module, f"PART_{part}_TESTS"):
        return getattr(tests_module, f"PART_{part}_TESTS")
    else:
        return None

def submit(year: int, day: int, session_id: str):
    """submit a solution for a specific day in a year"""
    directory = os.path.dirname(__file__)
    day_directory = os.path.join(directory, str(year), f"day{day}")

    part1 = load_function(year, day, 1)
    part2 = load_function(year, day, 2)
    part_1_tests = load_tests(year, day, 1)
    part_2_tests = load_tests(year, day, 2)

    puzzle_input_path = os.path.join(day_directory, "puzzle_input.txt")
    puzzle_description_path = os.path.join(day_directory, "puzzle_description.txt")
    test = lambda part: _test([part1, part2][part - 1], [part_1_tests, part_2_tests][part - 1])
    submit_solution = lambda part: _submit([part1, part2][part-1](puzzle_input_path), year, day,  part, session_id)
    update_description = lambda: _update_description(puzzle_description_path, year, day, session_id)

    # Part I
    if part1 is None:
        print("[red]No function for part I found.[/red]")
        return
    if part_1_tests is None:
        print("[red]No tests for part I found.[/red]")
        return
    print("[bold][underline]Part I[/underline][/bold]")
    print("Executing tests for part I")
    if test(1):
        print("[green]All tests successful![/green]")
    else:
        print("[red]Some Tests had wrong results. Try again![/red]")
        quit()
    print()
    print("Submitting part I")
    if submit_solution(1):
        print("[green]Correct result![/green]")
    else:
        print("[red]Your result is wrong, try again...[/red]")
        quit()
    print()

    update_description()

    # Part II
    if part2 is None:
        print("[red]No function for part II found.[/red]")
        return
    if part_2_tests is None:
        print("[red]No tests for part II found.[/red]")
        return
    print("[bold][underline]Part II[/underline][/bold]")
    print("Executing tests for part II")
    if test(2):
        print("[green]All tests successful![/green]")
    else:
        print("[red]Some Tests had wrong results. Try again![/red]")
        quit()
    print()
    print("Submitting part II")
    if submit_solution(2):
        print("[green]Correct result![/green]")
    else:
        print("[red]Your result is wrong, try again...[/red]")
        quit()
    print()

    print("[green]Both results are correct![/green]")
    with open(os.path.join(day_directory, "#done"), "w") as f:
        pass

def main(argc: int, argv: list):
    session_id = None

    if argc > 1:
        # error handling
        if argc < 3 or argc > 4:
            print_usage()
            exit(1)

        # parse the date
        year = int(argv[1])
        day = int(argv[2])

        # load the session_id
        if argc == 4:
            session_id = argv[3]
        else:
            session_id = load_session_id()
    else:
        # get todays date
        year, month, day = [int(s) for s in datetime.today().strftime('%Y-%m-%d').split("-")]
        session_id = load_session_id()

        # error handling
        if month != 12:
            print("It's not december yet. Return in december")
            exit(1)
        if day > 25:
            print(f"Christmas is over. Return in {year + 1}")
            exit(1)

    cwd = os.path.dirname(__file__)
    day_dir = os.path.join(cwd, str(year), "day" + str(day))
    if not os.path.exists(day_dir):
        print(f"[red]The day you're trying to submit a solution for doesn't exist yet. [/red]")
        quit(1)

    submit(year, day, session_id)

if __name__ == "__main__":
    main(len(sys.argv), sys.argv)