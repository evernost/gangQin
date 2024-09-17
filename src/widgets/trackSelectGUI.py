# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : trackSelectGUI
# File name     : trackSelectGUI.py
# Purpose       : provides GUI to select the tracks in a MIDI file.
# Author        : QuBi (nitrogenium@hotmail.com)
# Creation date : September 17th, 2024
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# External libs
# =============================================================================
# Project specific constants
#from commons import *

import tkinter as tk
from tkinter import ttk



# =============================================================================
# Unit tests
# =============================================================================
if (__name__ == "__main__") :
  print("[INFO] There are no unit tests available for 'trackSelectGUI.py'")



# =============================================================================
# Main code
# =============================================================================
def centerWindow(container) :
  
  # Ensure widgets are updated before calculating size
  container.update_idletasks()
  
  w = container.winfo_reqwidth()
  h = container.winfo_reqheight()

  screen_width = container.winfo_screenwidth()
  screen_height = container.winfo_screenheight()

  x = (screen_width - w) // 2
  y = (screen_height - h) // 2

  container.geometry(f"{w}x{h}+{x}+{y}")



def on_button_click() : 
  print("That's all folks.")
  root.destroy()


root = tk.Tk()
root.title("Track selection")
root.resizable(0, 0)

content = ttk.Frame(root, padding = 20)

choices = [f"{'Track 1' : <20}{'[LEFT]' : >7}",
           f"{'Track 1' : <20}{'[RIGHT]' : >7}",
           "Track 3: prout"]
choicesvar = tk.StringVar(value = choices)

# frame = ttk.Frame(content, width=200, height=500)
availableLbl = ttk.Label(content, text = "Available tracks:")
trackLst = tk.Listbox(content, listvariable = choicesvar, width = 50, font = ("Consolas", 10))
# name = ttk.Entry(content)

setLeftButton = ttk.Button(content, text = "Assign track to Left hand")
setRightButton = ttk.Button(content, text = "Assign track to Right hand")

generateButton = ttk.Button(content, text = "Generate", command = on_button_click, default = "active")
quitButton = ttk.Button(content, text = "Quit")

content.grid(column = 0, row = 0)

availableLbl.grid(column = 0, row = 0, columnspan = 3, rowspan = 1, sticky = (tk.W))
trackLst.grid(column = 0, row = 1, columnspan = 3, rowspan = 1)
setLeftButton.grid(column = 0, row = 3, sticky = (tk.W, tk.N), pady = (10, 30))
setRightButton.grid(column = 2, row = 3, sticky = (tk.E, tk.N), pady = (10, 30))
quitButton.grid(column = 0, row = 4, sticky = (tk.W, tk.S))
generateButton.grid(column = 2, row = 4, sticky = (tk.E, tk.S))


# Bindings
root.bind("<Return>", lambda event = None : generateButton.invoke())


centerWindow(root)


root.mainloop()