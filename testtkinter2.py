import tkinter as tk
from tkinter import ttk, messagebox


def submit_form():
    name = name_var.get()
    gender = gender_var.get()
    country = country_var.get()
    hobbies = []
    if reading_var.get():
        hobbies.append("Reading")
    if sports_var.get():
        hobbies.append("Sports")
    if music_var.get():
        hobbies.append("Music")

    comments = comments_box.get("1.0", tk.END).strip()

    msg = f"Name: {name}\nGender: {gender}\nCountry: {country}\nHobbies: {', '.join(hobbies)}\nComments: {comments}"
    messagebox.showinfo("Submitted Information", msg)


# Create main window
root = tk.Tk()
root.title("User Info Form")
root.geometry("400x500")
root.resizable(False, False)

# Variables
name_var = tk.StringVar()
gender_var = tk.StringVar(value="Male")
country_var = tk.StringVar()
reading_var = tk.BooleanVar()
sports_var = tk.BooleanVar()
music_var = tk.BooleanVar()

# Title label
title_label = ttk.Label(root, text="User Information Form", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

# Name
ttk.Label(root, text="Name:").pack(anchor="w", padx=20)
ttk.Entry(root, textvariable=name_var, width=30).pack(padx=20, pady=5)

# Gender
ttk.Label(root, text="Gender:").pack(anchor="w", padx=20)
gender_frame = ttk.Frame(root)
gender_frame.pack(padx=20, pady=5, anchor="w")

ttk.Radiobutton(gender_frame, text="Male", variable=gender_var, value="Male").pack(side="left", padx=5)
ttk.Radiobutton(gender_frame, text="Female", variable=gender_var, value="Female").pack(side="left", padx=5)
ttk.Radiobutton(gender_frame, text="Other", variable=gender_var, value="Other").pack(side="left", padx=5)

# Country
ttk.Label(root, text="Country:").pack(anchor="w", padx=20)
country_box = ttk.Combobox(root, textvariable=country_var, values=["India", "USA", "UK", "Canada", "Australia"])
country_box.pack(padx=20, pady=5)
country_box.current(0)

# Hobbies
ttk.Label(root, text="Hobbies:").pack(anchor="w", padx=20)
hobbies_frame = ttk.Frame(root)
hobbies_frame.pack(padx=20, pady=5, anchor="w")

ttk.Checkbutton(hobbies_frame, text="Reading", variable=reading_var).pack(side="left", padx=5)
ttk.Checkbutton(hobbies_frame, text="Sports", variable=sports_var).pack(side="left", padx=5)
ttk.Checkbutton(hobbies_frame, text="Music", variable=music_var).pack(side="left", padx=5)

# Comments
ttk.Label(root, text="Comments:").pack(anchor="w", padx=20)
comments_box = tk.Text(root, width=40, height=5)
comments_box.pack(padx=20, pady=5)

# Submit button
ttk.Button(root, text="Submit", command=submit_form).pack(pady=15)

# Run the app
root.mainloop()
