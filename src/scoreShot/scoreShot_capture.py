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



# TODO
# - Find the relation between Imagegrab and the window coordinates
# - Find how to show an image (what container)
# - Test how immediate a screenshot loading is
# - See how to implement the drag and drop of the rulers



# =============================================================================
# Constants pool
# =============================================================================
# Some high resolution screens use a scaling factor that messes with the 
# coordinates of 'Imagegrab'.
SCREEN_SCALING = 1.0


# =============================================================================
# Main code
# =============================================================================



class Ruler :

  def __init__(self) :
    
    self.toto = 0
    
    










# Callback functions
def take_screenshot(event):
  x = captureWin.winfo_x()
  y = captureWin.winfo_y()
  width = captureWin.winfo_width()
  height = captureWin.winfo_height()
  
  bbox = (0, 0, captureWin.winfo_screenwidth(), captureWin.winfo_screenheight())
  #bbox = (x+7+100, y+100, x+7+100+root.winfo_width()-100, y+100+root.winfo_height()-100)
  
  screenshot = ImageGrab.grab(bbox)
  screenshot.save("screenshot.png")
  print("[DEBUG] Screenshot saved as 'screenshot.png'.")

def on_moveWindow(event) :
    x = captureWin.winfo_x()
    y = captureWin.winfo_y()

    if (event.keysym == "Up") :
      captureWin.geometry(f"+{x}+{y-1}")
    elif (event.keysym == "Down") :
      captureWin.geometry(f"+{x}+{y+1}")
    elif (event.keysym == "Left") :
      captureWin.geometry(f"+{x-1}+{y}")
    elif (event.keysym == "Right") :
      captureWin.geometry(f"+{x+1}+{y}")

def on_mouseWheel(event) :
    x = captureWin.winfo_x()
    y = captureWin.winfo_y()

    if (event.state & 0x0001) : 
      if (event.delta > 0) :
        captureWin.geometry(f"+{x+1}+{y}")
      elif (event.delta < 0) :
        captureWin.geometry(f"+{x-1}+{y}")
    else :
      if (event.delta > 0) :
        captureWin.geometry(f"+{x}+{y-1}")
      elif (event.delta < 0) :
        captureWin.geometry(f"+{x}+{y+1}")
    
def on_quit(event = None) : 
  print("Exiting app...")
  root.destroy()

def update_mouse_position() :
  x, y = captureWin.winfo_pointerxy()
  print(f"[DEBUG] Mouse: ({x}, {y}) --- Root winfo_x/y: ({captureWin.winfo_x()}, {captureWin.winfo_y()}) --- Root winfo_w/h: ({captureWin.winfo_width()}, {captureWin.winfo_height()})")
  
  captureWin.after(200, update_mouse_position)







print(f"================================================================================")
print(f"SCORESHOT CAPTURE - v0.1 (September 2024)")
print(f"================================================================================")
print("Shortcuts:")
print("- Left/Right/Up/Down : move the capture window pixel by pixel")
print("- 'c'                : take snapshot")
print("- 'q'                : exit app")








# Create the main window
root = tk.Tk()
root.geometry("800x500")
root.title("scoreShot - Capture (database) v0.1 [ALPHA] (September 2024)")

captureWin = tk.Toplevel(root)
captureWin.geometry("800x300")
captureWin.title("scoreShot - Capture (tool) v0.1 [ALPHA] (September 2024)")


# Capture window is always on top
captureWin.attributes("-topmost", True)






# Set fixed sizes for the first and last columns, and let the middle column take the rest
captureWin.grid_columnconfigure(0, minsize = 100)  # First column fixed at 100 pixels
captureWin.grid_columnconfigure(1, weight = 1)     # Middle column flexible, takes the remaining space
captureWin.grid_columnconfigure(2, minsize = 100)  # Last column fixed at 100 pixels

# Set fixed sizes for the first and last rows, and let the middle row take the rest
captureWin.grid_rowconfigure(0, minsize=100)     # First row fixed at 100 pixels
captureWin.grid_rowconfigure(1, weight=1)        # Middle row flexible, takes the remaining space
captureWin.grid_rowconfigure(2, minsize=100)     # Last row fixed at 100 pixels






# Define a set of distinct colors for the 9 frames
colors = ["lightblue", "lightgreen", "lightcoral", "lightyellow", 
          "lightpink", "lightgray", "lightcyan", "lightgoldenrod", "lightsteelblue"]

# Create and place 9 frames in a 3x3 grid
frames = []
for row in range(3):
    for col in range(3):
        color_index = row * 3 + col
        frame = tk.Frame(captureWin, bg = colors[color_index])
        frame.grid(row=row, column=col, sticky="nsew")
        frames.append(frame)


captureWin.attributes("-transparentcolor", "red")



# Create a canvas widget
canvas = tk.Canvas(frames[4], bg = "red", highlightthickness = 0)
canvas.pack(fill = "both", expand = True)


rulerUp = canvas.create_line(50, 50, 150, 50, fill = "black", width = 1)
rulerDown = canvas.create_line(50, 80, 150, 80, fill = "black", width = 1)


captureWin.bind('<Up>', on_moveWindow)
captureWin.bind('<Down>', on_moveWindow)
captureWin.bind('<Left>', on_moveWindow)
captureWin.bind('<Right>', on_moveWindow)
captureWin.bind('<MouseWheel>', on_mouseWheel)
captureWin.bind('<s>', take_screenshot)
captureWin.bind('<q>', on_quit)

update_mouse_position()

root.protocol("WM_DELETE_WINDOW", on_quit)


root.mainloop()
