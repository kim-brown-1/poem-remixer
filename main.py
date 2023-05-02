# https://realpython.com/python-gui-tkinter/
import tkinter as tk
from poem_generator import *

num_poets = 1
num_poems = 2
max_lines = 5
main_window_width = 900
main_window_height = 800
button_width = 25
button_height = 5

poet_options = get_poets()


def show_poem():
    poem_text.set(get_poem(num_poems, int(num_lines.get()[0]), [poet_1.get(), poet_2.get()]))
    poem_label.config(text=poem_text.get())


def save_poem():
    save(poem_text.get(), "{}, {}".format(poet_1.get(), poet_2.get()))


window = tk.Tk()
window.title("Poem Remixer")
window.geometry("{}x{}".format(main_window_width, main_window_height))
poem_text = tk.StringVar()

line_number_options = ["1 line"]
for i in range(2, max_lines+1):
    line_number_options.append("{} lines".format(i))
num_lines = tk.StringVar()
num_lines.set(line_number_options[2])

num_lines_dropdown = tk.OptionMenu(window, num_lines, *line_number_options)
num_lines_dropdown.grid(row=0, column=2)

generate_button = tk.Button(
    text="Generate",
    command=show_poem,
    width=button_width,
    height=button_height,
    bg="white",
    fg="black",
)
generate_button.grid(row=1, column=1)

poem_frame = tk.Frame(window, width=main_window_width, height=main_window_height/3,
                      highlightbackground="blue", highlightthickness=2)
poem_frame.grid(row=2, column=0, columnspan=3)

poem_label = tk.Label(window, text=poem_text.get())
poem_label.grid(row=2, column=0, columnspan=3)

poet_1 = tk.StringVar()
poet_1.set(poet_options[0])
poet_dropdown_1 = tk.OptionMenu(window, poet_1, *poet_options)
poet_dropdown_1.grid(row=0, column=0)

poet_2 = tk.StringVar()
poet_2.set(poet_options[1])
poet_dropdown_2 = tk.OptionMenu(window, poet_2, *poet_options)
poet_dropdown_2.grid(row=0, column=1)

save_button = tk.Button(
    text="Save poem",
    command=save_poem,
    width=button_width,
    height=button_height,
    bg="white",
    fg="black",
)
save_button.grid(row=3, column=1)

try:
    window.mainloop()  # listen for events
except KeyboardInterrupt:
    print("Exiting.")
