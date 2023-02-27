from tkinter import *
import pandas
import random
BACKGROUND_COLOR = "#B1DDC6"
word_pair = {}
data_list = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    data_list = original_data.to_dict(orient="records")
else:
    data_list = data.to_dict(orient="records")


def change_card():
    canvas.itemconfig(canvas_img, image=card_back)
    canvas.itemconfig(title, text="English", fill="white")
    canvas.itemconfig(word, text=word_pair["English"], fill="white")


def generate_word():
    global word_pair, flip_timer
    window.after_cancel(flip_timer)
    canvas.itemconfig(title, text="French", fill="black")
    word_pair = random.choice(data_list)
    french_word = word_pair["French"]
    canvas.itemconfig(word, text=french_word, fill="black")
    canvas.itemconfig(canvas_img, image=card_front)
    flip_timer = window.after(3000, func=change_card)

def clicked_right():
    data_list.remove(word_pair)
    to_learn = pandas.DataFrame(data_list)
    to_learn.to_csv("data/words_to_learn.csv", index=False)
    generate_word()

def clicked_wrong():
    generate_word()



window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=change_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
canvas_img = canvas.create_image(400, 264, image=card_front)
title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
word = canvas.create_text(400, 286, text="", font=("Ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

right_img = PhotoImage(file="images/right.png")
right_but = Button(image=right_img, highlightthickness=0, command=clicked_right)
right_but.grid(column=1, row=1)
wrong_img = PhotoImage(file="images/wrong.png")
wrong_but = Button(image=wrong_img, highlightthickness=0, command=clicked_wrong)
wrong_but.grid(column=0, row=1)

generate_word()

window.mainloop()