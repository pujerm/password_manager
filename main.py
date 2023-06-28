from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def password_generator():
    password_entry.delete(0, END)

    letters_list = [choice(letters) for char in range(randint(8, 10))]
    symbol_list = [choice(symbols) for char in range(randint(2, 4))]
    numbers_list = [choice(numbers) for char in range(randint(2, 4))]

    password_list = letters_list + symbol_list + numbers_list

    shuffle(password_list)

    password = "".join(password_list)

    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def saving_passwords():
    website = website_entry.get().title()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }
    add_button.config(background="blue")
    if website == "" or email == "" or password == "":

        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")

    else:

        is_ok = messagebox.askokcancel(title=website, message=f'These are the details entered: \nEmail: {email}'
                                                              f'\nPassword: {password} \nIs it ok to save?')
        add_button.config(background="blue")
        if is_ok:

            try:
                with open("data.json", "r") as data_file:

                    # reading new data
                    data = json.load(data_file)
                    # updating old data with new data
                    data.update(new_data)

                with open("data.json", "w") as data_file:
                    # saving updated data
                    json.dump(data, data_file, indent=4)

            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)

            website_entry.delete(0, END)
            password_entry.delete(0, END)
    add_button.config(background="white")

# ---------------------------- LOAD PASSWORD ------------------------------- #


def searching_password():
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)

        search_button.config(background="blue")
        messagebox.showinfo(title=website_entry.get().title(), message=f'Email: {data[website_entry.get().title()]["email"]} \nPassword: {data[website_entry.get().title()]["password"]}')
    except KeyError:
        messagebox.showinfo(title="Attention", message=f'No items in the database.\nAre you sure about the website: {website_entry.get().title()}?')

    except FileNotFoundError:
        messagebox.showinfo(title="Attention", message="The password database does not exist. Add first item.")

    search_button.config(background="white")
# ---------------------------- UI SETUP ------------------------------- #


windows = Tk()
windows.title("Password Manager")
windows.config(pady=50, padx=50, bg="white")

canvas = Canvas(width=200, height=200, bg="white", highlightthickness=0)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

website_label = Label(text="Website:", bg="white")
website_label.grid(row=1, column=0)

email_label = Label(text="Email/Username:", bg="white")
email_label.grid(row=2, column=0)

password_label = Label(text="Password:", bg="white")
password_label.grid(row=3, column=0)

website_entry = Entry(width=32)
website_entry.grid(row=1, column=1)
website_entry.focus()

email_entry = Entry(width=50)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "mateusz.pujer@gmail.com")

password_entry = Entry(width=32)
password_entry.grid(row=3, column=1)

generate_button = Button(text="Generate Password", bg="white", activebackground="blue", command=password_generator)
generate_button.grid(row=3, column=2)

add_button = Button(text="Add", bg="white", width=43, command=saving_passwords)
add_button.grid(row=4, column=1, columnspan=2)

search_button = Button(text="Search", bg="white", width=14, command=searching_password)
search_button.grid(row=1, column=2)

windows.mainloop()
