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
# Tasks
# =============================================================================
# - TODO: find the relation between Imagegrab and the window coordinates
# - TODO: find how to show an image (what container)
# - TODO: test how immediate a screenshot loading is
# - TODO: see how to implement the drag and drop of the rulers



# =============================================================================
# External libs 
# =============================================================================
import database
import os
from PIL import ImageGrab, ImageTk, Image
import ruler
import tkinter as tk
from tkinter import ttk




# =============================================================================
# Constants pool
# =============================================================================
# Some high resolution screens use a scaling factor that messes with the 
# coordinates of 'Imagegrab'.
# Zoom factor 100%: SCREEN_SCALING = 1.0
# Zoom factor 250%: SCREEN_SCALING = 2.5
SCREEN_SCALING = 1.0

SCORE_DB_DIR = "./songs/scoreShotDB"



# =============================================================================
# Main code
# =============================================================================

# Callback functions
def on_screenshot(event) :
  global captureCount

  # Define the coordinates of the aperture 
  x1 = canvasArray[4].winfo_rootx()*SCREEN_SCALING
  y1 = canvasArray[4].winfo_rooty()*SCREEN_SCALING
  x2 = x1 + canvasArray[4].winfo_width()*SCREEN_SCALING
  y2 = y1 + canvasArray[4].winfo_height()*SCREEN_SCALING

  # Turn off the rulers, we don't want them in the screenshot
  rulerObj.visible = False
  canvasArray[4].config(highlightthickness = 0)

  captureWin.update()

  screenshot = ImageGrab.grab((x1,y1,x2,y2))
  screenshot.save(f"{SCORE_DB_DIR}/screenshot_{captureCount}.png")
  
  # Turn the rulers back on
  rulerObj.visible = True
  canvasArray[4].config(highlightthickness = 2)

  print(f"[DEBUG] Screenshot saved as 'screenshot_{captureCount}.png'")
  captureCount += 1

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
        captureWin.geometry(f"+{x-1}+{y}")
      elif (event.delta < 0) :
        captureWin.geometry(f"+{x+1}+{y}")
    else :
      if (event.delta > 0) :
        captureWin.geometry(f"+{x}+{y-1}")
      elif (event.delta < 0) :
        captureWin.geometry(f"+{x}+{y+1}")
    

def on_snapshotSel(event) :
  index = captureListBox.curselection()
  if index :
    imgName = captureListBox.get(index)

    x = ImageTk.PhotoImage(Image.open(f"{SCORE_DB_DIR}/{imgName}"))

    # TODO: resize so that the picture occupies the same real estate no
    # matter what (even if there was some screen scaling)
    # ...


    imgbox.config(image = x)
    imgbox.image = x
    

def on_keyPress(event) :
  if (event.char == 'r') :
    recallImg.lift()

def on_keyRelease(event) :
  if (event.char == "r") :
    recallImg.lower()

def on_resize(event) :
  rulerObj.update()


def on_quit(event = None) : 
  print("Exiting app...")
  root.destroy()




print(f"================================================================================")
print(f"SCORESHOT CAPTURE - v0.1 (September 2024)")
print(f"================================================================================")
print("Shortcuts:")
print("- Left/Right/Up/Down     : move the capture window pixel by pixel")
print("- Mouse wheel up         : move the capture window position up by 1 pixel")
print("- Mouse wheel down       : move the capture window position down by 1 pixel")
print("- Alt + Mouse wheel up   : move the capture window position left by 1 pixel")
print("- Alt + Mouse wheel down : move the capture window position right by 1 pixel")
print("- 'r'                    : temporarily recall the last snaphost")
print("- 's'                    : take snapshot")
print("- 'q'                    : exit app")




# -----------------------------------------------------------------------------
# Main window definition
# -----------------------------------------------------------------------------
root = tk.Tk()
root.geometry("1500x500")
root.title("scoreShot - Capture database v0.1 [ALPHA] (September 2024)")
root.resizable(0, 0)

# Main window layout
root.grid_columnconfigure(0, minsize = 100)
root.grid_columnconfigure(1, weight = 1)


availableLbl = ttk.Label(root, text = "Snapshots:")
captureList = []
for fileName in os.listdir(SCORE_DB_DIR) :
  if fileName.endswith(".png"):
    captureList.append(fileName)
captureListVar = tk.StringVar(value = captureList)
captureListBox = tk.Listbox(root, listvariable = captureListVar, width = 30, font = ("Consolas", 10))
x = ImageTk.PhotoImage(Image.open(f"{SCORE_DB_DIR}/screenshot_0.png"))
imgbox = tk.Label(root, image = x)



availableLbl.grid(column = 0, row = 0, columnspan = 1, rowspan = 1, sticky = "sw")
captureListBox.grid(column = 0, row = 1, columnspan = 1, rowspan = 1)
imgbox.grid(column = 1, row = 1, columnspan = 1, rowspan = 1)


# Keyboard bindings
root.bind('<q>', on_quit)



# -----------------------------------------------------------------------------
# Capture window definition
# -----------------------------------------------------------------------------
captureWin = tk.Toplevel(root)
captureWin.geometry("1250x440")
captureWin.title("scoreShot - Capture tool v0.1 [ALPHA] (September 2024)")

# Capture window is always on top
captureWin.attributes("-topmost", True)

# Capture window layout
BORDER_SIZE = 100
captureWin.grid_columnconfigure(0, minsize = BORDER_SIZE)
captureWin.grid_columnconfigure(1, weight = 1)
captureWin.grid_columnconfigure(2, minsize = BORDER_SIZE)

captureWin.grid_rowconfigure(0, minsize = BORDER_SIZE)
captureWin.grid_rowconfigure(1, weight = 1)
captureWin.grid_rowconfigure(2, minsize = BORDER_SIZE)




# Define a set of distinct colors for the 9 frames
colors = ["lightsteelblue", "lightblue", "lightsteelblue", "lightblue", 
          "red", "lightblue", "lightsteelblue", "lightblue", "lightsteelblue"]

canvasArray = []
for row in range(3):
  for col in range(3):
    color_index = row * 3 + col
    
    # The "border" canvases have a fixed size
    if ((row == 0) or (row == 2) or (col == 0) or (col == 2)) :
      c = tk.Canvas(captureWin, bg = colors[color_index], highlightthickness = 0, width = BORDER_SIZE, height = BORDER_SIZE)
    
    # The middle canvas (capture aperture) has a variable size
    elif ((row == 1) and (col == 1)) :
      c = tk.Canvas(captureWin, bg = colors[color_index], highlightthickness = 2, highlightbackground = "blue")
    else :
      c = tk.Canvas(captureWin, bg = colors[color_index], highlightthickness = 0)
    c.grid(row = row, column = col, sticky = "nsew")
    canvasArray.append(c)

# Bind the red color (unused in the palette) with the transparency property.
captureWin.attributes("-transparentcolor", "red")

rulerObj = ruler.Ruler(canvasArray)



x = ImageTk.PhotoImage(Image.open(f"{SCORE_DB_DIR}/screenshot_0.png"))
recallImg = tk.Label(captureWin, image = x)
recallImg.grid(row = 1, column = 1, sticky = "nsew")
recallImg.lower()


# Keyboard bindings
captureWin.bind("<Up>", on_moveWindow)
captureWin.bind("<Down>", on_moveWindow)
captureWin.bind("<Left>", on_moveWindow)
captureWin.bind("<Right>", on_moveWindow)
captureWin.bind("<MouseWheel>", on_mouseWheel)
captureWin.bind("<Configure>", on_resize)
captureWin.bind('<KeyPress>', on_keyPress)
captureWin.bind('<KeyRelease>', on_keyRelease)
captureWin.bind("<s>", on_screenshot)
captureWin.bind("<q>", on_quit)

captureListBox.bind("<<ListboxSelect>>", on_snapshotSel)

captureCount = 0

root.protocol("WM_DELETE_WINDOW", on_quit)






# The name of the song file (.pr file) is the only input for this interface.
# It shall come from a selection GUI.
# Only .pr files can be selected.
songFile = "./songs/Rachmaninoff_Moment_Musical_Op_16_No_4.pr"

# Try to load, create a new 















root.mainloop()
