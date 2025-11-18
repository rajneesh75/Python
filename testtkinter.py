import tkinter as tk
from tkinter import messagebox


def handle_selection(choice):
    messagebox.showinfo("Selection", f"You selected: {choice}")
    root.destroy()


# Create the main window
root = tk.Tk()
root.title("Menu")

# Define the list of options
options = ["Option 1", "Option 2", "Option 3"]

# Create buttons for each option
for option in options:
    button = tk.Button(root, text=option, command=lambda o=option: handle_selection(o))
    button.pack(pady=5)

# Run the main event loop
root.mainloop()
