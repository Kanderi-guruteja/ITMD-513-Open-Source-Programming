# register.py
from tkinter import *
import sqlite3
from tkinter import messagebox
import random

window = Tk()

# Welcome message
welcome_label = Label(window, text="Enter Your Details To Sign Up", font=("Arial", 13))
welcome_label.pack(pady=(30, 10))  # Adjust the top and bottom padding

# Connecting to sqlite3
connection = sqlite3.connect("registered_users_db")
c = connection.cursor()
# Creating table "users" if it does not exist in user_db
c.execute("""CREATE TABLE IF NOT EXISTS users (
             ID text,
             Firstname text,
             Lastname text,
             Email text,
             Password text)""")


def open_registration_window():
    window.destroy()
    '''This function will allow the user to return to this window from another window'''
    pass


def complete_register():
    # Get entries from entry fields
    f = (firstnameE.get())
    l = (lastnameE.get())
    e = (emailE.get())
    p = (passwordE.get())

    # This list will be used to make sure that all entries have values before submitting
    rule = [
        len(f) > 0,
        len(l) > 0,
        len(e) > 0,
        len(p) > 0
    ]

    if all(rule) == True:
        # Create primary key id for each user
        num = range(1, 10)
        for _ in num:
            i = (random.randint(000000, 999999))
        user_id = f[0].upper() + l[0].upper() + str(i)

        # Populate db once register button clicked
        c.execute(f"INSERT INTO users VALUES ('{user_id}', '{f}', '{l}', '{e}', '{p}')")
        # Sends a commit to the SQLite server
        connection.commit()

        return_menu = messagebox.askyesno(title="Registration successful", message="Click yes to return to main menu")
        # If user clicks the Yes button, the current window will close and the main window will open
        if return_menu == True:
            connection.close()
            window.destroy()
            # Used to import and run the function from the main window
            from main import return_to_main
        else:
            pass
    else:
        messagebox.showerror(title="Missing Entries", message="Please fill in all entries")


def clear_entries():
    '''This function will clear all entries in entry fields'''
    firstnameE.delete(0, "end")
    lastnameE.delete(0, "end")
    emailE.delete(0, "end")
    passwordE.delete(0, "end")


def exit_application():
    answer = messagebox.askyesno("Exit Confirmation", "Are you sure you want to exit?")
    if answer:
        window.destroy()


# Firstname
firstnameL = Label(window, text="Enter Firstname: ")
firstnameL.place(x=88, y=70)

firstnameE = Entry(window, width=44)
firstnameE.place(x=90, y=100)

# Lastname
lastnameL = Label(window, text="Enter Lastname: ")
lastnameL.place(x=88, y=130)

lastnameE = Entry(window, width=44)
lastnameE.place(x=90, y=160)

# Email
emailL = Label(window, text="Enter Email: ")
emailL.place(x=88, y=190)

emailE = Entry(window, width=44)
emailE.place(x=90, y=220)

# Password
passwordL = Label(window, text="Enter Password: ")
passwordL.place(x=88, y=250)

passwordE = Entry(window, width=44)
passwordE.place(x=90, y=280)

# Register button
registerBtn = Button(window, text="Register", width=16, height=3, command=complete_register)
registerBtn.place(x=88, y=335)

# Clear button
clearBtn = Button(window, text="Clear", width=16, height=3, command=clear_entries)
clearBtn.place(x=236, y=335)

# Exit button
exitBtn = Button(window, text="Exit", width=16, height=3, command=exit_application)
exitBtn.place(x=385, y=335)

# Set the window dimensions and position
window_width = 440
window_height = 440
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 8
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Window configs
window.title("Chart Analysis For Crime In Chicago: Sign Up")
window.resizable(0, 0)
window.attributes("-topmost", True)
window.mainloop()
