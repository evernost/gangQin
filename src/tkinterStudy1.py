# -*- coding: utf-8 -*-
# =============================================================================
# Module name     : tkinterStudy1
# File name       : tkinterStudy1.py
# Purpose         : projet gangQin
# Author          : Quentin Biache
# Creation date   : September 21st, 2023
# =============================================================================
import tkinter as tk

def on_select(event):
    selected_option.set(var.get())

root = tk.Tk()
root.title("Dropdown Menu Example")

# Set the window size
root.geometry("400x200")  # Width x Height

var = tk.StringVar(root)
selected_option = tk.StringVar(root)

options = ["Option 1", "Option 2", "Option 3"]

# Create an OptionMenu and position it
dropdown = tk.OptionMenu(root, var, *options)
dropdown.place(x=50, y=50)  # Adjust the 'x' and 'y' coordinates as needed

var.set("Select an option")
selected_option.set("Selected option: None")

submit_button = tk.Button(root, text="Submit", command=lambda: on_select(None))
submit_button.pack()

label = tk.Label(root, textvariable=selected_option)
label.pack()

root.mainloop()
