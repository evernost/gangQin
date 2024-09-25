# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : scoreShot_capture
# File name     : scoreShot_capture.py
# Purpose       : application entry point for the scoreShot capturing tool
# Author        : QuBi (nitrogenium@hotmail.com)
# Creation date : Monday, 24 September 2024
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# External libs 
# =============================================================================
import tkinter as tk
from PIL import ImageGrab



# =============================================================================
# Main code
# =============================================================================



def take_screenshot(event):
  
  x = root.winfo_x()
  y = root.winfo_y()
  width = root.winfo_width()
  height = root.winfo_height()
  
  
  bbox = (x, y, x + width, y + height)
  
  
  screenshot = ImageGrab.grab(bbox)
  screenshot.save("screenshot.png")
  print("[DEBUG] Screenshot saved as 'screenshot.png'.")




def update_mouse_position():
  x, y = root.winfo_pointerxy()
  print(f"Mouse Position: X: {x}, Y: {y}")
  
  root.after(200, update_mouse_position)

def on_quit(event) : 
  print("Exiting app...")
  root.destroy()






# Create the main window
root = tk.Tk()
root.geometry("800x300")
root.title("scoreShot - Capture v0.1 [ALPHA] (September 2024)")
root.attributes('-topmost', True)



# Set fixed sizes for the first and last columns, and let the middle column take the rest
root.grid_columnconfigure(0, minsize=100)  # First column fixed at 100 pixels
root.grid_columnconfigure(1, weight=1)     # Middle column flexible, takes the remaining space
root.grid_columnconfigure(2, minsize=100)  # Last column fixed at 100 pixels

# Set fixed sizes for the first and last rows, and let the middle row take the rest
root.grid_rowconfigure(0, minsize=100)     # First row fixed at 100 pixels
root.grid_rowconfigure(1, weight=1)        # Middle row flexible, takes the remaining space
root.grid_rowconfigure(2, minsize=100)     # Last row fixed at 100 pixels






# Define a set of distinct colors for the 9 frames
colors = ["lightblue", "lightgreen", "lightcoral", "lightyellow", 
          "lightpink", "lightgray", "lightcyan", "lightgoldenrod", "lightsteelblue"]

# Create and place 9 frames in a 3x3 grid
frames = []
for row in range(3):
    for col in range(3):
        color_index = row * 3 + col  # Calculate the index for the color list
        frame = tk.Frame(root, bg=colors[color_index])
        frame.grid(row=row, column=col, sticky="nsew")
        frames.append(frame)


root.attributes("-transparentcolor", "red")



# Create a canvas widget
canvas = tk.Canvas(frames[4], bg = "red", highlightthickness = 0)
canvas.pack(fill = "both", expand = True)

# Draw a line with specified coordinates (x1, y1, x2, y2)
# Replace these coordinates with your own
x1, y1 = 50, 50
x2, y2 = 150, 50
canvas.create_line(x1, y1, x2, y2, fill = "black", width = 1)



root.bind('<s>', take_screenshot)
root.bind('<q>', on_quit)

update_mouse_position()

root.mainloop()
