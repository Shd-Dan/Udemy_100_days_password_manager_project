import json
from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip

# ---------------------------- CONSTANTS ------------------------------- #
WHITE = "white"
FONT = font = ("Arial", 10)


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letter = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_numbers + password_symbols + password_letter
    shuffle(password_list)

    password = "".join(password_list)

    password_entry.insert(0, password)

    pyperclip.copy(password)


# ---------------------------- SAVE AND FIND PASSWORD ------------------------------- #

def save():
    new_data = {website_entry.get():
                    {"email": email_entry.get(),
                     "password": password_entry.get()}}

    if email_entry.get() is None or password_entry.get() is None:
        messagebox.showinfo(title="Oops!", message="Please do not leave any fields empty!")
    else:
        # is_ok = messagebox.askokcancel(title=website_entry.get(),
        #                                message=f"You have entered: \nE-mail: {email_entry.get()} "
        #                                        f"\nPassword: {password_entry.get()} \nIs it ok to save?")

        # if is_ok:
        try:
            with open("data.json", "r") as data_file:
                # read the data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # updating new info
            data.update(new_data)

            with open("data.json", "w") as data_file:
                # saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            clear_entry()


def clear_entry():
    entries = [website_entry, password_entry]
    for entry in entries:
        entry.delete(0, 'end')


def find_password():
    website = website_entry.get()
    try:
        with open('data.json', 'r') as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="No File!", message="No Data File Found")
    else:
        # Alternative way is to use if else statements
        try:
            messagebox.showinfo(title=f"Your password for {website}",
                                message=f"E-mail: {data[website]['email']}\n"
                                        f"Password: {data[website]['password']}")

        except KeyError:
            messagebox.showinfo(title="Not Found!", message="No details for the website exists")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=40, pady=40, bg=WHITE)
# window.grid_columnconfigure(2, minsize=40)

canvas = Canvas(width=200, height=200, bg=WHITE, highlightthickness=0)
logo_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_image)
canvas.grid(column=1, row=0)

# Labels
label_website = Label(text="Website:", bg=WHITE, font=FONT)
label_website.grid(column=0, row=1)
label_email = Label(text="Email/Username:", bg=WHITE, font=FONT)
label_email.grid(column=0, row=2)
label_password = Label(text="Password", bg=WHITE, font=FONT)
label_password.grid(column=0, row=3)

# Entries
website_entry = Entry(width=57)
website_entry.grid(column=1, row=1, columnspan=2, sticky=W)
website_entry.focus()
email_entry = Entry(width=30)
email_entry.grid(column=1, row=2, columnspan=2, sticky=W)
email_entry.insert(0, "big_bob_roof@mail.ru")
password_entry = Entry(width=30)
password_entry.grid(column=1, row=3, sticky=W)

# Buttons
generate_password_button = Button(text="Generate Password", bg=WHITE, width=19, command=generate_password)
generate_password_button.grid(row=3, column=2)
add_button = Button(text="Add", bg=WHITE, width=48, command=save)
add_button.grid(column=1, row=4, columnspan=2)
search_button = Button(text="Search", bg=WHITE, width=19, command=find_password)
search_button.grid(column=2, row=2)

window.mainloop()
