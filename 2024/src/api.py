from pathlib import Path
import re
from time import sleep

import requests

HOST = "https://adventofcode.com"
CACHE_DIR = ".cache"
README = Path(__file__).parent.parent / "README.md"

# Load cookie
with open(".cookie") as f:
    SESSION_COOKIE = f.read().strip()


def get_input(year: int, day: int) -> str:
    cached_input = Path(f"{CACHE_DIR}/{year}/{day}/input.txt")
    if cached_input.exists():
        return cached_input.read_text()
    url = f"{HOST}/{year}/day/{day}/input"
    response = requests.get(url, headers={"cookie": f"session={SESSION_COOKIE}"})
    response.raise_for_status()
    cached_input.parent.mkdir(parents=True, exist_ok=True)
    cached_input.write_text(response.text)
    return response.text


def submit_answer(year: int | str, day: int, part: int, answer: int):
    if _check_solved(year, day, part):
        print("Already solved")
        return True

    url = f"{HOST}/{year}/day/{day}/answer"
    response = requests.post(
        url,
        headers={"cookie": f"session={SESSION_COOKIE}"},
        data={"level": part, "answer": answer},
    )
    response.raise_for_status()
    # Get the line with the main article
    article = re.search(r"<article><p>(.*?)</p></article>", response.text, re.DOTALL).group(1)

    if "That's the right answer" in article:
        print("That's the right answer")
        _update_readme_calendar(year)
        return True
    if "That's not the right answer" in article:
        print("That's not the right answer")
        return False
    if "You gave an answer too recently" in article:
        wait_time = int(re.search(r"\d+", article).group()) + 1
        print(f"Waiting {wait_time} seconds..")
        sleep(wait_time)
        return submit_answer(year, day, part, answer)
    if "You don't seem to be solving the right level" in article:
        raise ValueError("Part is invalid, already solved or not yet unlocked")


def _check_solved(year: int | str, day: int, part: int):
    calendar = _get_calendar(year)
    if calendar[day - 1] >= part:
        return True
    return False


def _get_calendar(year: int | str):
    url = f"{HOST}/{year}"
    response = requests.get(url, headers={"cookie": f"session={SESSION_COOKIE}"})
    response.raise_for_status()
    days = [0] * 25
    for match in re.finditer(r"Day (\d\d?)(?:, (one|two)?)?", response.text):
        day = int(match.group(1))
        assert 0 < day < 26, f"Invalid day: {day}"
        if match.group(2):
            days[day - 1] = 1 if match.group(2) == "one" else 2
    return days


def _update_readme_calendar(year: int):
    days = _get_calendar(year)
    # Generate table with current stars
    table = ["| Day | Part 1 | Part 2 |", "| :---: | :---: | :---: |"]
    for day_index, stars in enumerate(days):
        star1 = "⭐" if stars > 0 else " "
        star2 = "⭐" if stars > 1 else " "
        table.append(f"| [Day {day_index + 1}](https://adventofcode.com/2024/day/{day_index + 1}) | {star1} | {star2} |")

    # Replace the section between the  "<!--- advent_readme_stars --->" comments in the readme with the new table
    divider_comment = "<!--- advent_readme_stars --->"
    new_table = f"{divider_comment}\n{'\n'.join(table)}\n{divider_comment}"
    table_pattern = rf"{divider_comment}\n[\s\S]*\n{divider_comment}"
    with open(README, "r+") as f:
        readme = f.read()
        new_readme = re.sub(table_pattern, new_table, readme)
        f.seek(0)
        f.write(new_readme)
