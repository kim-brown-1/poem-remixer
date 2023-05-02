import requests
from random import *

poets_url = "https://poetrydb.org/author"
titles_url = "https://poetrydb.org/author/{}/title"
poem_text_url = "https://poetrydb.org/title/{}/lines.json"
saved = False


def get_poets() -> list:
    resp = requests.get(poets_url)
    if resp.status_code != 200:
        print("Failed with status {}, please try again.".format(resp.status_code))
        return []

    resp_json = resp.json()  # TODO: catch errors
    if "authors" not in resp_json:
        return []

    return resp_json["authors"]


def get_titles(poet) -> list:
    resp = requests.get(titles_url.format(poet))
    if resp.status_code != 200:
        return []

    titles = []
    for title in resp.json():  # TODO: catch errors here
        titles.append(title["title"])

    return titles


def get_poem(num_poems, num_lines: int, poet_choices: list) -> str:
    global saved
    all_lines = []
    for poet in poet_choices:
        titles = get_titles(poet)
        rand_poems = pick_from_list(titles, num_poems)
        for title in rand_poems:
            lines = get_poem_lines(title)
            all_lines = all_lines + lines
    result = pick_from_list(all_lines, num_lines)
    clean_output_lines(result)
    saved = False
    poem_text = '\n\n'.join(result)
    return "{}\n\n\n--{}, {}".format(poem_text, poet_choices[0], poet_choices[1])  # TODO: support arbitrary num authors


# pick_from_list: returns cnt unique random items in the list
def pick_from_list(options: list, cnt: int) -> list:
    options_copy = options.copy()  # don't shuffle input list
    shuffle(options_copy)
    return options_copy[:cnt]


def clean_output_lines(lines: list):
    for i in range(len(lines)):
        lines[i] = lines[i].replace("\xad", "- ").replace("\"", "")
    last_line = lines[len(lines)-1]
    last_char = last_line[len(last_line)-1]
    if last_char == "," or last_char == ";":
        lines[len(lines)-1] = last_line[:-1]


def get_poem_lines(name: str) -> list:
    resp = requests.get(poem_text_url.format(name))
    if resp.status_code != 200:
        print("Failed to get poems- please try again")
        return []

    return filter_poem_lines(resp.json()[0]["lines"])  # TODO: catch errors here


def filter_poem_lines(lines: list) -> list:
    output = []
    for line in lines:
        stripped_line = line.strip()
        if len(stripped_line) > 5:  # filter out most roman numerals
            output.append(stripped_line)

    return output


def save(poem_text, poet: str):
    global saved
    if saved:
        return
    with open('created.txt', 'a') as f:
        f.write("{}\n--------------\n".format(poem_text, poet))
        f.close()
    saved = True
