from rich import print
import os
import re
import requests
from bs4 import BeautifulSoup
from typing import List, Tuple, Sequence, Any, Callable, Iterable
import inspect
import importlib

def get_puzzle_input(year: int, day: int, session_token: str) -> str | None:
    """get the input of the puzzle"""
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    cookies = {"session": session_token}
    response = requests.get(url, cookies=cookies)

    if "Please log in" in response.text:
        return None

    return response.text

def get_puzzle_description(year: int, day: int, part: int, session_token: str) -> str | None:
    """get the description of the puzzle"""
    url = f"https://adventofcode.com/{year}/day/{day}"
    cookies = {"session": session_token}
    response = requests.get(url, cookies=cookies)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        target_elements = soup.findAll("article", "day-desc")
        if target_elements is not None:
            if 0 <= part - 1 < len(target_elements):
                target_element = target_elements[part - 1]
                text: str = target_element.text
                idx = text.find(" ---") + 4
                text = text[:idx] + "\n" + text[idx:]

                return text
            else:
                return None
    else:
        # error getting the content
        return None

def update_description(file_path: str, year: int, day: int, session_token: str):
    description2 = get_puzzle_description(year, day, 2, session_token)
    if description2 is None: return

    with open(file_path, "a+") as file:
        file.seek(0)
        if "Part Two" not in file.read():
            file.write("\n")
            file.write(description2)

def submit(result, year: int, day: int, part: int, session_token: str) -> bool:
    """submit a result"""
    # Get result
    to_submit = str(result)
    print(f"Your result: {to_submit}")

    # Make POST request to Advent of Code API
    url = f"https://adventofcode.com/{year}/day/{day}/answer"
    payload = {"level": str(part), "answer": to_submit}
    cookies = {"session": session_token}
    response = requests.post(url, data=payload, cookies=cookies)

    # wrong result
    if response.status_code != 200:
        return False

    # correct result
    if "s the right answer" in response.text:
        print(f"[green]Your result '{to_submit}' is correct![/green]")
        return True
    elif "not the right answer" in response.text:
        print(f"[red]Your answer '{to_submit}' is wrong.[/red]")
        if "low" in response.text: print("[red]Your answer is too low.[/red]")
        elif "high" in response.text: print("[red]Your answer is too high.[/red]")
        return False

    if "have to wait" in response.text:
        s_match = re.search(r'(\d+)s', response.text)
        m_match = re.search(r'(\d+)m', response.text)

        wait_time = ""
        if m_match:
            wait_time += " " + m_match.group(1) + "m"
        if s_match:
            wait_time += " " + s_match.group(1) + "s"
        if wait_time == "":
            wait_time = " a bit"
        print(f"[yellow]Your result: {to_submit}[/yellow]")
        print(f"[yellow]You submitted an answer too recently. You'll have to wait a{wait_time}.[/yellow]")
        return False


    if "Funny seeing you here" in response.text:
        print("[yellow]Couldn't submit answer, maybe the puzzle was already solved?[/yellow]")
        if is_already_solved(result, year, day, part, session_token):
            print(f"[green]Your result: {to_submit}[/green]")
            return True
        else:
            print(f"[red]Your result: {to_submit}[/red]")
            print("[red]Couldn't retrieve answer. You might have made a mistake...[/red]")
            return False

    # different
    print(f"[red]Your result: {to_submit}[/red]")
    print("[red]Something went wrong.[/red]")
    return False

def is_already_solved(result, year: int, day: int, part: int, session_token: str):
    url = f"https://adventofcode.com/{year}/day/{day}"
    cookies = {"session": session_token}
    response = requests.get(url, cookies=cookies)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        answers = [p.code.text for p in soup.find_all('p') if 'Your puzzle answer was' in p.text]
        if len(answers) < part:
            return False
        return str(result) == answers[part - 1]
    else:
        # error getting the content
        return False

def _make_caller(func: Callable[..., Any], debug_value: bool = True) -> Callable[..., Any]:
    """
    Returns a wrapper that injects debug=debug_value iff the function accepts it.
    Caches the signature check once.
    """
    try:
        params = inspect.signature(func).parameters
        supports_debug = "debug" in params
    except (TypeError, ValueError):  # some callables may not have inspectable signatures
        supports_debug = False

    def call(*args: Any, **kwargs: Any) -> Any:
        if supports_debug and "debug" not in kwargs:
            kwargs["debug"] = debug_value
        return func(*args, **kwargs)

    return call

def _normalize_scenario(scenario: Sequence[Any]) -> Tuple[str, Any, tuple, dict]:
    """
    Normalizes:
      - old format: (file, expected) where expected is int|str
      - old format: (file, (expected, *params))
      - new format: (file, expected, args_or_kwargs)
      - new format: (file, expected, args, kwargs) (order can be swapped)
    into: (file, expected, args_tuple, kwargs_dict)
    """
    if len(scenario) == 2:
        file, second = scenario
        if isinstance(second, tuple):
            expected = second[0]
            args = tuple(second[1:])
            kwargs = {}
        else:
            expected = second
            args = ()
            kwargs = {}
        return file, expected, args, kwargs

    if len(scenario) == 3:
        file, expected, third = scenario
        if isinstance(third, dict):
            return file, expected, (), dict(third)
        if isinstance(third, (list, tuple)):
            return file, expected, tuple(third), {}
        raise TypeError(f"Invalid 3-item scenario third element: {type(third)!r}")

    if len(scenario) == 4:
        file, expected, a, b = scenario
        # allow swapping
        if isinstance(a, dict) and isinstance(b, (list, tuple)):
            kwargs, args = dict(a), tuple(b)
        elif isinstance(b, dict) and isinstance(a, (list, tuple)):
            kwargs, args = dict(b), tuple(a)
        else:
            raise TypeError(
                "4-item scenario must be (file, expected, args, kwargs) "
                "where args is list/tuple and kwargs is dict (order can be swapped)."
            )
        return file, expected, args, kwargs

    raise TypeError(f"Scenario must have 2, 3, or 4 elements; got {len(scenario)}")

def test(
    func: Callable[..., Any],
    test_data: Iterable[Sequence[Any]]
) -> bool:
    """
    Runs test scenarios, prints result lines, returns True if all passed.

    - coerce_to_str: keeps your previous behavior (string compare).
      If False, compares with == (preferred).
    - stop_on_fail: bail out early on first failure/exception.
    """
    call = _make_caller(func, debug_value=True)
    passed_all = True

    for i, raw in enumerate(test_data, start=1):
        file, expected, args, kwargs = _normalize_scenario(raw)
        print(f"#{i}: file={file!r}, args={args or ()!r}, kwargs={kwargs or {}!r}")
        
        try:
            got = call(file, *args, **kwargs)
            ok = str(got) == str(expected)
        except Exception as e:
            ok = False
            got = f"{type(e).__name__}: {e}"

        if ok:
            print(f"[green]#{i} got: {got}, expected: {expected}[/green]")
        else:
            print(f"[red]#{i} got: {got}, expected: {expected}[/red]")
            passed_all = False

    return passed_all

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
