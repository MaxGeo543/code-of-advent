import os
import sys
from rich import print
DIRECTORY = os.path.dirname(__file__)
PUZZLE_INPUT_PATH = os.path.join(DIRECTORY, "puzzle_input.txt")
PUZZLE_DESCRIPTION_PATH = os.path.join(DIRECTORY, "description.txt")
sys.path.append(os.path.join(DIRECTORY, "../../"))
from util.util import load_session_id, submit as _submit, test as _test, update_description as _update_description
submit = lambda part: _submit([part1, part2][part-1](PUZZLE_INPUT_PATH), *[int(c.replace("day", "")) for c in os.path.dirname(__file__).replace(os.sep, '/').split("/")[-2:]], part, load_session_id())
test = lambda part: _test([part1, part2][part-1], [PART_1_TESTS, PART_2_TESTS][part-1])
update_description = lambda: _update_description(PUZZLE_DESCRIPTION_PATH, *[int(c.replace("day", "")) for c in os.path.dirname(__file__).replace(os.sep, '/').split("/")[-2:]], load_session_id())
# ------------------------------------------------
# Code above this should not be edited
# ------------------------------------------------

# ------------------------------------------------
# Tests will be performed before submitting
# This is optional, you may clear the dictionaries
# ------------------------------------------------
PART_1_TESTS = {
    # os.path.join(DIRECTORY, "test_input.txt"): 0
}

PART_2_TESTS = {
    # os.path.join(DIRECTORY, "test_input.txt"): 0
}
# ------------------------------------------------

def part1(input_file):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()

    # calculate result
    result = ""

    # return result
    return result

def part2(input_file):
    # load the puzzle input into a variable
    with open(input_file, "r") as file:
        puzzle_input = file.readlines()

    # calculate result
    result = ""

    # return result
    return result


if __name__ == "__main__":
    # Part I
    print("[bold][underline]Part I[/underline][/bold]")
    print("Executing tests for part I")
    if test(1):
        print("[green]All tests successful![/green]")
    else:
        print("[red]Some Tests had wrong results. Try again![/red]")
        quit()
    print()
    print("Submitting part I")
    if submit(1):
        print("[green]Correct result![/green]")
    else:
        print("[red]Your result is wrong, try again...[/red]")
        quit()
    print()

    update_description()

    # Part II
    print("[bold][underline]Part II[/underline][/bold]")
    print("Executing tests for part II")
    if test(2):
        print("[green]All tests successful![/green]")
    else:
        print("[red]Some Tests had wrong results. Try again![/red]")
        quit()
    print()
    print("Submitting part II")
    if submit(2):
        print("[green]Correct result![/green]")
    else:
        print("[red]Your result is wrong, try again...[/red]")
        quit()
    print()

    print("[green]Both results are correct![/green]")
    with open(os.path.join(DIRECTORY, "#done"), "w") as f: pass