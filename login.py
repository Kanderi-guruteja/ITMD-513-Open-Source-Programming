from tkinter import *
import sqlite3
from tkinter import messagebox

window = Tk()

# Welcome message
welcome_label = Label(window, text="Enter Your Details To Login", font=("Arial", 13))
welcome_label.pack(pady=(30, 10))  # Adjust the top and bottom padding

# Connecting to sqlite3
connection = sqlite3.connect("registered_users_db")
c = connection.cursor()


def open_login_window():
    window.destroy()
    '''This function will allow the user to return to this window from another window'''
    pass


def login_verification():
    # Get entries from entry fields
    e = (emailE.get())
    p = (passwordE.get())

    # This list will be used to make sure that all entries have values before submitting
    rule = [
        len(e) > 0,
        len(p) > 0
    ]

    if all(rule) == True:
        # Connecting to SQLite3 db
        with sqlite3.connect("registered_users_db") as db:
            c = db.cursor()

        # Check if user is registered
        find_user = ("SELECT * FROM users WHERE email = ? AND password = ?")
        c.execute(find_user, [(e), (p)])
        result = c.fetchall()

        if result:
            # This will open a new window once credentials are correct
            open_login_window()
            return_menu = messagebox.askyesno(title="Login successful", message="Click yes to return to main menu")
            # If user clicks the Yes button, the current window will close and the main window will open
            if return_menu == True:
                connection.close()
                window.destroy()
                # Used to import and run the function from the main window
                from main import return_to_main
            else:
                pass
        else:
            messagebox.showerror(title="Invalid User", message="User not found")
    else:
        messagebox.showerror(title="Missing Entries", message="Please fill in all entries")


def clear_entries():
    '''This function will clear all entries in entry fields'''
    emailE.delete(0, "end")
    passwordE.delete(0, "end")


# Email
emailL = Label(window, text="Enter Email: ")
emailL.place(x=88, y=130)

emailE = Entry(window, width=44)
emailE.place(x=90, y=160)

# Password
passwordL = Label(window, text="Enter Password: ")
passwordL.place(x=88, y=190)

passwordE = Entry(window, width=44)
passwordE.place(x=90, y=220)

# Login button
loginBtn = Button(window, text="Login", width=16, height=3, command=login_verification)
loginBtn.place(x=88, y=280)

# Clear button
clearBtn = Button(window, text="Clear", width=16, height=3, command=clear_entries)
clearBtn.place(x=236, y=280)

# Exit button
exitBtn = Button(window, text="Exit", width=16, height=3, command=exit_application)
exitBtn.place(x=385, y=280)

# Set the window dimensions and position
window_width = 440
window_height = 440
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 8
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Window configs
window.title("Chart Analysis For Crime In Chicago: Login")
window.resizable(0, 0)
window.attributes("-topmost", True)
window.mainloop()
