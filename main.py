# https://realpython.com/python-gui-tkinter/
import random
import tkinter as tk
import requests

num_poets = 1
num_poems = 2
poem_num_lines = 3
titles_url = "https://poetrydb.org/author/{}/title"
poem_text_url = "https://poetrydb.org/title/{}/lines.json"
poets_url = "https://poetrydb.org/author"


def get_poets() -> list:
    resp = requests.get(poets_url).json()  # TODO: handle non-200
    return resp["authors"]


poet_options = get_poets()


def get_poem() -> str:
    print(poet_choice.get())
    all_lines = []
    for poet in [poet_choice.get()]:  # TODO: adjust when supporting more than one poet
        titles = get_titles(poet)
        print("Found {} titles for this author. Randomly picking {}\n".format(len(titles), num_poems))
        rand_poems = pick_from_list(titles, num_poems)
        for title in rand_poems:
            lines = get_poem_lines(title)
            all_lines = all_lines + lines
    result = pick_from_list(all_lines, poem_num_lines)
    clean_output_lines(result)
    print(result)
    return '\n\n'.join(result)


def get_titles(poet):
    resp = requests.get(titles_url.format(poet))  # TODO: handle non-200
    titles = []
    for title in resp.json():
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
    return filter_poem_lines(resp.json()[0]["lines"])


def clean_output_lines(lines: list):
    for i in range(len(lines)):
        lines[i] = lines[i].replace("\xad", "- ")


def show_poem():
    poem_text.set(get_poem())
    label.config(text=poem_text.get())


def save():
    with open('created.txt', 'a') as f:
        f.write("{}\n\n--{}\n\n\n\n\n\n".format(poem_text.get(), poet_choice.get()))
        f.close()


window = tk.Tk()
window.title("Poem Mixer :)")
poet_choice = tk.StringVar()
poet_choice.set("Ambrose Bierce")
poem_text = tk.StringVar()
label = tk.Label(text=poem_text.get())
label.pack()
poet_dropdown = tk.OptionMenu(window, poet_choice, *poet_options)
poet_dropdown.pack()
generate_button = tk.Button(
    text="Generate",
    command=show_poem,
    width=25,
    height=5,
    bg="white",
    fg="black",
)
generate_button.pack()
save_button = tk.Button(
    text="Save poem",
    command=save,
    width=25,
    height=5,
    bg="white",
    fg="black",
)
save_button.pack()
window.mainloop()  # listen for events
