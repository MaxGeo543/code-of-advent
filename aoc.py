from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path
from typing import Optional, Tuple
import aoc_util
import os
from rich import print

DEFAULT_SESSION_FILE = Path("session.txt")
SOLUTION_FILE_TEMPLATE = ("def part1(input_file, debug=False):",
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
                          "def part2(input_file, debug=False):",
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
                       "    # (os.path.join(DIRECTORY, \"test_input.txt\"), 0, [], {}})",
                       "]",
                       "",
                       "PART_2_TESTS = [",
                       "    # (os.path.join(DIRECTORY, \"test_input.txt\"), 0, [], {})",
                       "]",
                       "")


# validations
def _valid_year(value: str) -> int:
    try:
        year = int(value)
    except ValueError as e:
        raise argparse.ArgumentTypeError("year must be an integer") from e
    if year < 2015 or year > 9999:
        raise argparse.ArgumentTypeError("year must be between 2015 and 9999")
    return year

def _valid_day(value: str) -> int:
    try:
        day = int(value)
    except ValueError as e:
        raise argparse.ArgumentTypeError("day must be an integer") from e
    if not (1 <= day <= 25):
        raise argparse.ArgumentTypeError("day must be in 1..25")
    return day

def _valid_part(value: str) -> int:
    try:
        part = int(value)
    except ValueError as e:
        raise argparse.ArgumentTypeError("part must be 1 or 2") from e
    if part not in (1, 2):
        raise argparse.ArgumentTypeError("part must be 1 or 2")
    return part

# session id
def _load_session_id_from_file(path: Path) -> Optional[str]:
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8").strip()
    return text or None

def _resolve_session_id(args: argparse.Namespace) -> Optional[str]:
    if getattr(args, "session_id", None):
        return args.session_id
    session_file = getattr(args, "session_file", DEFAULT_SESSION_FILE)
    return _load_session_id_from_file(Path(session_file))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="aoc", description="Console app CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    def add_common(p: argparse.ArgumentParser) -> None:
        p.add_argument(
            "year",
            nargs="?",
            type=_valid_year,
            help="Year (defaults to today)",
        )
        p.add_argument(
            "day",
            nargs="?",
            type=_valid_day,
            help="Day 1..25 (defaults to today)",
        )
        p.add_argument(
            "--session-id",
            dest="session_id",
            help="Session id (if omitted, read from --session-file)",
        )
        p.add_argument(
            "--session-file",
            default=DEFAULT_SESSION_FILE,
            help=f"File to read session id from (default: {DEFAULT_SESSION_FILE})",
        )

    # get
    p_get = subparsers.add_parser("get", help="Fetch puzzle for a day")
    add_common(p_get)

    # test
    p_test = subparsers.add_parser("test", help="Run tests for a day/part")
    add_common(p_test)
    p_test.add_argument(
        "part",
        nargs="?",
        type=_valid_part,
        choices=(1, 2),
        help="Part to test (1 or 2). If omitted, test both parts.",
    )

    # submit
    p_submit = subparsers.add_parser("submit", help="Submit answers for a day/part")
    add_common(p_submit)
    p_submit.add_argument(
        "part",
        nargs="?",
        type=_valid_part,
        choices=(1, 2),
        help="Part to submit (1 or 2). If omitted, submit both parts.",
    )
    p_submit.add_argument(
        "--pretest",
        action="store_true",
        help="Run tests before submitting (default: false)",
    )

    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    today = dt.date.today()
    year = args.year if args.year is not None else today.year
    day = args.day if args.day is not None else today.day

    session_id = _resolve_session_id(args)

    # Decide which parts to operate on (if applicable).
    parts: Optional[tuple[int, ...]]
    if args.command in ("test", "submit"):
        parts = (args.part,) if args.part in (1, 2) else (1, 2)
    else:
        parts = None

    if args.command == "get":
        get_command(year, day, session_id)
    elif args.command == "test":
        test_command(year, day, parts)
    elif args.command == "submit":
        submit_command(year, day, parts, args.pretest, session_id)

    else:
        parser.error("Unknown command")

    return 0


# commands
def test_command(year: int, day: int, parts: Tuple[int, ...]):
    directory = os.path.dirname(__file__)
    day_directory = os.path.join(directory, str(year), f"day{day}")
    puzzle_input_path = os.path.join(day_directory, "puzzle_input.txt")
    puzzle_description_path = os.path.join(day_directory, "puzzle_description.txt")

    for part in parts:
        fn = aoc_util.load_function(year, day, part)
        tests = aoc_util.load_tests(year, day, part)

        if fn is None:
            print(f"[red]No function for part {part} found.[/red]")
            continue

        if tests is None:
            print(f"[red]No tests for part {part} found.[/red]")
            continue
        
        print(f"Executing tests for part {part}")
        if aoc_util.test(fn, tests):
            print("[green]All tests successful![/green]")
        else:
            print("[red]Some Tests had wrong results. Try again![/red]")
        print()

def submit_command(year: int, day: int, parts: Tuple[int, ...], pretest: bool, session_id: str):
    directory = os.path.dirname(__file__)
    day_directory = os.path.join(directory, str(year), f"day{day}")
    puzzle_input_path = os.path.join(day_directory, "puzzle_input.txt")
    puzzle_description_path = os.path.join(day_directory, "puzzle_description.txt")

    for part in parts:
        fn = aoc_util.load_function(year, day, part)
        if fn is None:
            print(f"[red]No function for part {part} found.[/red]")
            continue

        tests_passed = True
        if pretest:
            tests = aoc_util.load_tests(year, day, part)
            if tests:
                print(f"Executing tests for part {part}")
                tests_passed = aoc_util.test(fn, tests)
                if tests_passed: print("[green]All tests successful![/green]")
                else: 
                    print("[red]Some Tests had wrong results. Try again![/red]")
                    continue
                print()
            else:
                print(f"[yellow]No tests for part {part} found.[/yellow]")


        print(f"Submitting part {part}")
        if aoc_util.submit(fn(puzzle_input_path), year, day,  part, session_id):
            if part == 1:
                aoc_util.update_description(puzzle_description_path, year, day, session_id)
                print("[green]Part 2 is now available![/green]")
            else:
                print(f"[green]day {day} is #done![/green]")
                with open(os.path.join(day_directory, "#done"), "w") as f:
                    pass
        else:
            return
    
def get_command(year: int, day: int, session_id: str):
    cwd = os.path.dirname(__file__)
    day_dir = os.path.join(cwd, str(year), "day"+str(day))

    print(f"Creating directory for {year} day {day}")
    os.makedirs(day_dir, exist_ok=True)


    # define file names
    solution_file = os.path.join(day_dir, "solution.py")
    tests_file = os.path.join(day_dir, "tests.py")
    puzzle_input_file = os.path.join(day_dir, "puzzle_input.txt")
    description_file = os.path.join(day_dir, "puzzle_description.txt")

    
    # puzzle_input file
    if not os.path.exists(puzzle_input_file):
        print("Retrieving puzzle input...")
        puzzle_input = aoc_util.get_puzzle_input(year, day, session_id)
        if puzzle_input is None:
            print("[red]Session expired. please get a new session token.[/red]")
            return

        # write input file
        with open(puzzle_input_file, "w") as file:
            file.write(puzzle_input)

        print(f"[green]Puzzle description saved under {puzzle_input_file}[/green]")
    else:
        print(f"Puzzle description already exists at {puzzle_input_file}")


    # description file
    if not os.path.exists(description_file):
        print("Retrieving puzzle description...")
        description = aoc_util.get_puzzle_description(year, day, 1, session_id)
        if description is None:
            print("[red]Error retrieving puzzle description.[/red]")
            return
        

        description2 = aoc_util.get_puzzle_description(year, day, 2, session_id)
        if description2 is not None:
            description += "\n" + description2


        # write input file
        with open(description_file, "w") as file:
            file.write(description)

        print(f"[green]Puzzle description saved under {description_file}[/green]")

    
    # write solution file
    if not os.path.exists(solution_file):
        with open(solution_file, "w") as py:
            py_content = "\n".join(SOLUTION_FILE_TEMPLATE)
            py.write(py_content)
        print(f"[green]New solution template under {solution_file}[/green]")

    # write tests file
    if not os.path.exists(tests_file):
        with open(tests_file, "w") as py:
            py_content = "\n".join(TESTS_FILE_TEMPLATE)
            py.write(py_content)
        print(f"[green]New test template under {solution_file}[/green]")


if __name__ == "__main__":
    raise SystemExit(main())
