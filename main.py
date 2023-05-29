import pdb
from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

FONT_NAME = "Times New Roman"
TEXT_SIZE = 12
TEXT_TYPE = ["normal", "bold", "italic"]
USER_EMAIL = "GMAIL_USER@gmail.com"
JSON_DATA_FILE = "data.json"


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    # print("*** PC LOAD LETTER ***")
    # time.sleep(3)
    # print("Task failed successfully")

    input_password.delete(0, END)

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
    # symbols_restricted = ["+", "=", "#", "?", "*", "$", "!", "_", "-"]

    list_final_password = [random.choice(letters) for _ in range(random.randint(8, 10))] + \
                          [random.choice(symbols) for _ in range(random.randint(4, 6))] + \
                          [random.choice(numbers) for _ in range(random.randint(4, 6))]

    random.shuffle(list_final_password)
    password = ''.join(list_final_password)

    pyperclip.copy(password)
    input_password.insert(0, password)


# ---------------------------- FIND PASSWORD ------------------------------- #

def create_and_write_to_new_json_file(new_data, filename=JSON_DATA_FILE):
    with open(filename, 'w') as data_file:
        json.dump(new_data, data_file, indent=4)


def find_password():
    if len(input_website.get()) == 0:
        messagebox.showerror(title="Website empty", message="Cannot search, website box is empty")
        input_website.focus()
    else:
        # print("and I still haven't found what I'm looking for...")
        try:
            with open(JSON_DATA_FILE, 'r') as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            messagebox.showinfo(title="FILE NOT FOUND", message=f"File: {JSON_DATA_FILE} does not exist.")
        else:
            website = input_website.get()
            if website in data:
                file_username = data[website]['email']
                file_password = data[website]['password']
                copy_password = messagebox.askyesno(title=website, message=f"Email/Username:  {file_username} "
                                                                           f"\nPassword:  {file_password} "
                                                                           f"\n\nCopy password to clipboard?")
                if copy_password:
                    pyperclip.copy(file_password)
            else:
                messagebox.showinfo(title="Website not in file", message=f"No stored details for {website} exists.")

            # # pdb.set_trace()
            #
            # try:
            #     file_username = data[f'{website}']['email']
            #     file_password = data[f'{website}']['password']
            # except KeyError:
            #     messagebox.showinfo(title="Website not in file", message=f"No stored details for {website} exists.")
            # else:
            #     copy_password = messagebox.askyesno(title=website, message=f"Email/Username:  {file_username} "
            #                                                f"\nPassword:  {file_password} "
            #                                                f"\n\nCopy password to clipboard?")
            #
            #     if copy_password:
            #         pyperclip.copy(file_password)


def save_password():
    website = input_website.get()
    username = input_email_uname.get()
    password = input_password.get()
    new_data = {
        website: {
            "email": username,
            "password": password,
        }
    }

    no_fields_blank = len(website) > 0 and len(username) > 0 and len(password) > 0

    if not no_fields_blank:
        messagebox.showinfo("Ooops!", message="All fields are required!")
    else:
        # is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: "
        #                                            f"\nEmail/username:  {username} "
        #                                            f"\nPassword:  {password} "
        #                                            f"\n Is it ok to save?")

        # if is_ok:
        try:
            with open(JSON_DATA_FILE, 'r') as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            print(f"File: {JSON_DATA_FILE} does not exist.  Creating it")
            create_and_write_to_new_json_file(new_data)
        else:
            data.update(new_data)
            with open(JSON_DATA_FILE, 'w') as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            input_website.delete(0, END)
            input_password.delete(0, END)
            input_website.focus()
            # print(data)

        messagebox.showinfo(title="SUCCESS!!", message=f"Password for {website} saved successfully")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

canvas_logo = Canvas(width=200, height=200, highlightthickness=0)
image_logo = PhotoImage(file="logo.png")
canvas_logo.create_image(50, 100, image=image_logo)
canvas_logo.grid(column=1, row=0)

# ------------- CREATE LABELS ------------------------------ #
label_website = Label(text="Website:", font=(FONT_NAME, TEXT_SIZE, TEXT_TYPE[0]))
label_website.grid(column=0, row=1)
label_email_uname = Label(text="Email/Username:", font=(FONT_NAME, TEXT_SIZE, TEXT_TYPE[0]))
label_email_uname.grid(column=0, row=2)
label_password = Label(text="Password:", font=(FONT_NAME, TEXT_SIZE, TEXT_TYPE[0]))
label_password.grid(column=0, row=3)

# ------------- CREATE INPUT BOXES ------------------------------ #
input_website = Entry(width=21)
input_email_uname = Entry(width=35)
input_password = Entry(width=21)

# ------------- CREATE BUTTONS ------------------------------ #
button_generate_password = Button(text="Generate Password", command=generate_password)
button_add_password = Button(text="Add", command=save_password)
button_search_password = Button(text="Search", command=find_password)

# ------------- PLACE WIDGETS ------------------------------------#
canvas_logo.grid(column=1, row=0)
label_website.grid(column=0, row=1)
label_email_uname.grid(column=0, row=2)
label_password.grid(column=0, row=3)

input_website.grid(column=1, row=1, columnspan=2, sticky="W")
input_email_uname.grid(column=1, row=2, columnspan=2, sticky="EW")
input_password.grid(column=1, row=3, sticky="W")

button_search_password.grid(column=1, row=1, sticky="WE", padx=(135, 0))
button_generate_password.grid(column=1, row=3, sticky="W", padx=(135, 0))
button_add_password.grid(column=1, row=4, pady=5, sticky="EW")

input_website.focus()
input_email_uname.insert(0, USER_EMAIL)

window.mainloop()

# ------------------- CHAT GPT MODIFIED -------------------------- #
# canvas_logo.grid(column=1, row=0)
# label_website.grid(column=0, row=1)
# label_email_uname.grid(column=0, row=2)
# label_password.grid(column=0, row=3)
#
# input_website.grid(column=1, row=1, columnspan=2, sticky="EW")
# input_email_uname.grid(column=1, row=2, columnspan=2, sticky="EW")
# input_password.grid(column=1, row=3, sticky="W")
#
#
# button_add_password.grid(column=1, row=4, columnspan=2, pady=5, sticky="EW")
# button_generate_password.grid(column=2, row=3,sticky="E")

# ---------------------- CHAT GPT 2 -----------------------------#
# canvas_logo.grid(column=1, row=0)
# label_website.grid(column=0, row=1)
# label_email_uname.grid(column=0, row=2)
# label_password.grid(column=0, row=3)
#
# input_website.grid(column=1, row=1, columnspan=2, sticky="EW")
# input_email_uname.grid(column=1, row=2, columnspan=2, sticky="EW")
# input_password.grid(column=1, row=3, sticky="W")
#
# button_generate_password.grid(column=2, row=3, padx=5)
# button_add_password.grid(column=0, row=4, columnspan=3, sticky="EW")

# # ----------------------------- NEW UI ------------------------------- #
#
# window = Tk()
# window.title("Password Manager")
# window.config(padx=50, pady=50)
#
# canvas = Canvas(width=200, height=200)
# logo_img = PhotoImage(file="logo.png")
# canvas.create_image(100, 100, image=logo_img)
# canvas.grid(column=1, row=0)
#
# website_label = Label(text="Website:")
# website_label.grid(column=0, row=1)
#
# website_entry = Entry(width=35)
# website_entry.grid(column=1, row=1, columnspan=2, sticky="EW")
#
# email_label = Label(text="Email/Username:")
# email_label.grid(column=0, row=2)
#
# email_entry = Entry(width=35)
# email_entry.grid(column=1, row=2, columnspan=2, sticky="EW")
#
# password_label = Label(text="Password:")
# password_label.grid(column=0, row=3)
#
# password_entry = Entry(width=24)
# password_entry.grid(column=1, row=3, sticky="W")
#
# password_button = Button(text="Generate Password")
# password_button.grid(column=2, row=3, sticky="EW")
#
# add_button = Button(text="Add", width=36)
# add_button.grid(column=1, row=4, columnspan=2, sticky="EW")
#
# window.mainloop()
