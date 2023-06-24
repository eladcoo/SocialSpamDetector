import tkinter as tk
from tkinter import ttk


def display_as_table(data):
    window = tk.Tk()

    # Create the Treeview widget
    tree = ttk.Treeview(window)

    # Define the columns
    tree["columns"] = ("score", "mail")

    # Configure column headings
    tree.heading("#0", text="Index", anchor="center")
    tree.heading("score", text="Score", anchor="center")
    tree.heading("mail", text="Email Address", anchor="center")

    for i, row in enumerate(data):
        tree.insert("", "end", text=str(i+1), values=row[0:])

    # Pack the Treeview widget
    tree.pack()

    window.mainloop()
