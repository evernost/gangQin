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
from tkinter import ttk
from PIL import ImageGrab, ImageTk, Image



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
  def __init__(self, canvasArray) :
    self.canvasArray = canvasArray
    self.rulerLeft  = canvasArray[4].create_line(0, 0, 0, 1, fill = "black", width = 1, dash = (1, 10))
    self.rulerRight = canvasArray[4].create_line(0, 0, 0, 1, fill = "black", width = 1, dash = (1, 10))
    self.rulerUp    = canvasArray[4].create_line(0, 0, 0, 1, fill = "black", width = 1, dash = (1, 10))
    self.rulerDown  = canvasArray[4].create_line(0, 0, 0, 1, fill = "black", width = 1, dash = (1, 10))

    self.handleLeft  = self.canvasArray[3].create_rectangle(0, 0, 0, 1, fill = "green", outline = "green")
    self.handleRight = self.canvasArray[3].create_rectangle(0, 0, 0, 1, fill = "green", outline = "green")

    self.canvasArray[3].tag_bind(self.handleLeft, '<Button-1>', self.on_click)
    self.canvasArray[3].tag_bind(self.handleLeft, '<B1-Motion>', self.on_drag)
    self.canvasArray[3].tag_bind(self.handleLeft, '<ButtonRelease-1>', self.on_release)

    self.drag_data = {"x": 0, "y": 0}


  def updateAfterResize(self) :
    canvasArray[4].coords(self.rulerUp,     (0, 50, canvasArray[4].winfo_width(), 50))
    canvasArray[4].coords(self.rulerDown,   (0, canvasArray[4].winfo_height()-50, canvasArray[4].winfo_width(), canvasArray[4].winfo_height()-50))
    canvasArray[4].coords(self.rulerLeft,   (50, 0, 50, canvasArray[4].winfo_height()))
    canvasArray[4].coords(self.rulerRight,  (canvasArray[4].winfo_width()-50, 0, canvasArray[4].winfo_width()-50, canvasArray[4].winfo_height()))

    canvasArray[3].coords(self.handleLeft,  (80, 45, 99, 55))


  def on_click(self, event):
    self.drag_data["x"] = event.x
    self.drag_data["y"] = event.y

  def on_drag(self, event):
    dy = event.y - self.drag_data["y"]
    self.canvasArray[3].move(self.handleLeft, 0, dy)
    self.canvasArray[4].move(self.rulerUp, 0, dy)

    self.drag_data["x"] = event.x
    self.drag_data["y"] = event.y

  def on_release(self, event):
    pass






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
print("- 's'                : take snapshot")
print("- 'q'                : exit app")








# Create the main window
root = tk.Tk()
root.geometry("1000x500")
root.title("scoreShot - Capture (database) v0.1 [ALPHA] (September 2024)")
root.resizable(0, 0)

content = ttk.Frame(root, padding = 20)

availableLbl = ttk.Label(content, text = "Snapshots:")
trackListVar = tk.StringVar(value = [])
trackLst = tk.Listbox(content, listvariable = trackListVar, width = 50, font = ("Consolas", 10))
img = ImageTk.PhotoImage(Image.open("screenshot.png"))
imgbox = tk.Label(root, image = img)



content.grid(column = 0, row = 0)

availableLbl.grid(column = 0, row = 0, columnspan = 1, rowspan = 1, sticky = "w")
trackLst.grid(column = 0, row = 1, columnspan = 1, rowspan = 1)
imgbox.grid(column = 1, row = 1, columnspan = 1, rowspan = 1)



captureWin = tk.Toplevel(root)
captureWin.geometry("1250x440")
captureWin.title("scoreShot - Capture (tool) v0.1 [ALPHA] (September 2024)")


# Capture window is always on top
captureWin.attributes("-topmost", True)






# Set fixed sizes for the first and last columns, and let the middle column take the rest
BORDER_SIZE = 100
captureWin.grid_columnconfigure(0, minsize = BORDER_SIZE)
captureWin.grid_columnconfigure(1, weight = 1)
captureWin.grid_columnconfigure(2, minsize = BORDER_SIZE)

# Set fixed sizes for the first and last rows, and let the middle row take the rest
captureWin.grid_rowconfigure(0, minsize = BORDER_SIZE)
captureWin.grid_rowconfigure(1, weight = 1)
captureWin.grid_rowconfigure(2, minsize = BORDER_SIZE)






# Define a set of distinct colors for the 9 frames
colors = ["lightblue", "lightgreen", "lightcoral", "lightyellow", 
          "red", "lightgray", "lightcyan", "lightgoldenrod", "lightsteelblue"]




canvasArray = []
for row in range(3):
    for col in range(3):
        color_index = row * 3 + col
        if ((row == 0) or (row == 2) or (col == 0) or (col == 2)) :
          c = tk.Canvas(captureWin, bg = colors[color_index], highlightthickness = 0, width = BORDER_SIZE, height = BORDER_SIZE)
        else: 
          c = tk.Canvas(captureWin, bg = colors[color_index], highlightthickness = 0)
        c.grid(row = row, column = col, sticky = "nsew")
        canvasArray.append(c)



ruler = Ruler(canvasArray)


def on_resize(event) :
  ruler.updateAfterResize()


captureWin.attributes("-transparentcolor", "red")

captureWin.bind('<Up>', on_moveWindow)
captureWin.bind('<Down>', on_moveWindow)
captureWin.bind('<Left>', on_moveWindow)
captureWin.bind('<Right>', on_moveWindow)
captureWin.bind('<MouseWheel>', on_mouseWheel)
captureWin.bind('<Configure>', on_resize)
captureWin.bind('<s>', take_screenshot)
captureWin.bind('<q>', on_quit)



# update_mouse_position()

root.protocol("WM_DELETE_WINDOW", on_quit)


root.mainloop()
