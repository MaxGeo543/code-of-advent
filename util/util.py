from rich import print
import os
import re
import requests
from bs4 import BeautifulSoup

def get_puzzle_input(year: int, day: int, session_token: str) -> str|None:
    """get the input of the puzzle"""
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    cookies = {"session": session_token}
    response = requests.get(url, cookies=cookies)

    if "Please log in" in response.text:
        return None

    return response.text

def get_puzzle_description(year: int, day: int, part: int, session_token: str) -> str|None:
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

def load_session_id() -> str|None:
    """returns the session id from the file session.txt located in the same directory"""
    # get path of the session file
    session_file = os.path.join(os.path.dirname(__file__), "..", "session.txt")

    # error_handling
    if not os.path.exists(session_file):
        return None

    # read the session id
    with open(session_file, "r") as file:
        session_id = file.read().strip()

    return session_id

def update_description(file_path: str, year: int, day: int, session_token: str):
    description2 = get_puzzle_description(year, day, 2, session_token)
    if description2 is None: return

    with open(file_path, "a+") as file:
        file.seek(0)
        if "Part Two" not in file.read():
            file.write(description2)

def submit(result, year: int, day: int, part: int, session_token: str) -> bool:
    """submit a result"""
    # Get result
    to_submit = str(result)
    print(result)
    if input("Press enter to submit!") != "": quit()

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
        print(f"[green]Your result: {to_submit}[/green]")
        return True
    elif "not the right answer" in response.text:
        print(f"[red]Your result: {to_submit}[/red]")
        print("[red]Your answer is wrong.[/red]")
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
        print(f"[yellow]You submitted an answer to recently. You'll have to wait a{wait_time}.[/yellow]")
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

def test(func, test_data: list[tuple[str,str|int|tuple]]) -> bool:
    result = True
    for file, expected in test_data:
        if isinstance(expected, int) or isinstance(expected, str):
            test_result = func(file)
            if test_result == expected:
                print(f"[green]got: {test_result}, expected: {expected}[/green]")
            else:
                print(f"[red]got: {test_result}, expected: {expected}[/red]")
                result = False
        elif isinstance(expected, tuple):
            params = expected[1:]
            test_result = func(file, *expected[1:])
            if test_result == expected[0]:
                print(f"[green]got: {test_result}, expected: {expected[0]}[/green]")
            else:
                print(f"[red]got: {test_result}, expected: {expected[0]}[/red]")
                result = False

    return result