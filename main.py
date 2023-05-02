# https://realpython.com/python-gui-tkinter/
import random
import tkinter as tk
import requests

num_poets = 1
num_poems = 2
max_lines = 5
titles_url = "https://poetrydb.org/author/{}/title"
poem_text_url = "https://poetrydb.org/title/{}/lines.json"
poets_url = "https://poetrydb.org/author"
saved = False  # prevents saving poem more than once


def get_poets() -> list:
    resp = requests.get(poets_url)
    if resp.status_code != 200:
        print("Failed with status {}, please try again.".format(resp.status_code))
        return []

    resp_json = resp.json()  # TODO: catch errors
    if "authors" not in resp_json:
        return []

    return resp_json["authors"]


poet_options = get_poets()


def get_poem() -> str:
    global saved
    all_lines = []
    for poet in [poet_choice.get()]:  # TODO: adjust when supporting more than one poet
        titles = get_titles(poet)
        # print("Found {} titles for this author. Randomly picking {}\n".format(len(titles), num_poems))
        rand_poems = pick_from_list(titles, num_poems)
        for title in rand_poems:
            lines = get_poem_lines(title)
            all_lines = all_lines + lines
    result = pick_from_list(all_lines, int(num_lines.get()[0]))
    clean_output_lines(result)
    saved = False
    return '\n\n'.join(result)


def get_titles(poet) -> list:
    resp = requests.get(titles_url.format(poet))
    if resp.status_code != 200:
        return []

    titles = []
    for title in resp.json():  # TODO: catch errors here
        titles.append(title["title"])

    return titles


# pick_from_list: returns cnt unique random items in the list
def pick_from_list(options: list, cnt: int) -> list:
    options_copy = options.copy()  # don't shuffle input list
    random.shuffle(options_copy)
    return options_copy[:cnt]


def filter_poem_lines(lines: list) -> list:
    output = []
    for line in lines:
        if len(line) != 0:
            output.append(line)

    return output


def get_poem_lines(name: str) -> list:
    resp = requests.get(poem_text_url.format(name))
    if resp.status_code != 200:
        print("Failed to get poems- please try again")
        return []

    return filter_poem_lines(resp.json()[0]["lines"])  # TODO: catch errors here


def clean_output_lines(lines: list):
    for i in range(len(lines)):
        lines[i] = lines[i].replace("\xad", "- ")


def show_poem():
    poem_text.set(get_poem())
    label.config(text=poem_text.get())


def save():
    global saved
    if saved:
        return
    with open('created.txt', 'a') as f:
        f.write("{}\n\n--{}\n\n\n\n\n\n".format(poem_text.get(), poet_choice.get()))
        f.close()
    saved = True


window = tk.Tk()
window.title("Poem Remixer")
window.geometry("800x800")
poet_choice = tk.StringVar()
poet_choice.set("Ambrose Bierce")
poem_text = tk.StringVar()

num_lines = tk.StringVar()
num_lines.set("3 lines")
line_number_options = ["1 line"]
for i in range(2, max_lines+1):
    line_number_options.append("{} lines".format(i))

num_lines_dropdown = tk.OptionMenu(window, num_lines, *line_number_options)
num_lines_dropdown.grid(row=0, column=1)

poem_frame = tk.Frame(window, padx=200, width=400, height=400, highlightbackground="blue", highlightthickness=2)
poem_frame.grid(row=1, column=0)

label = tk.Label(window, text=poem_text.get())
label.grid(row=1, column=0)

poet_dropdown = tk.OptionMenu(window, poet_choice, *poet_options)
poet_dropdown.grid(row=0, column=0, pady=30)
generate_button = tk.Button(
    text="Generate",
    command=show_poem,
    width=25,
    height=5,
    bg="white",
    fg="black",
)
generate_button.grid(row=2, column=0)
save_button = tk.Button(
    text="Save poem",
    command=save,
    width=25,
    height=5,
    bg="white",
    fg="black",
)
save_button.grid(row=3, column=0)

try:
    window.mainloop()  # listen for events
except KeyboardInterrupt:
    print("Exiting.")
