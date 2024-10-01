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
import os
import tkinter as tk
from tkinter import ttk
from PIL import ImageGrab, ImageTk, Image



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
    
    # Lines for the rulers
    # Coordinates can't be specified at that point: they depend on the window properties
    # that is not initialised yet
    self.rulerLeft  = self.canvasArray[4].create_line(0, 0, 0, 1, fill = "black", width = 1, dash = (1, 10))
    self.rulerRight = self.canvasArray[4].create_line(0, 0, 0, 1, fill = "black", width = 1, dash = (1, 10))
    self.rulerUp    = self.canvasArray[4].create_line(0, 0, 0, 1, fill = "black", width = 1, dash = (1, 10))
    self.rulerDown  = self.canvasArray[4].create_line(0, 0, 0, 1, fill = "black", width = 1, dash = (1, 10))

    # Handles to drag and drop the rulers
    self.handleLeft   = self.canvasArray[3].create_rectangle(0, 0, 0, 1, fill = "grey", outline = "grey")
    self.handleRight  = self.canvasArray[5].create_rectangle(0, 0, 0, 1, fill = "grey", outline = "grey")
    self.handleUp     = self.canvasArray[1].create_rectangle(0, 0, 0, 1, fill = "grey", outline = "grey")
    self.handleDown   = self.canvasArray[7].create_rectangle(0, 0, 0, 1, fill = "grey", outline = "grey")

    # Attach a management function to each handle 
    self.bindHandle(self.handleLeft, canvasId = 3)
    self.bindHandle(self.handleRight, canvasId = 5)
    self.bindHandle(self.handleUp, canvasId = 1)
    self.bindHandle(self.handleDown, canvasId = 7)
    self.dragData = {"x": 0, "y": 0, "id": None}

    # Visible property
    self._visible = True




  def update(self) :
    apHeight = self.canvasArray[4].winfo_height()
    apWidth = self.canvasArray[4].winfo_width()
    self.canvasArray[4].coords(self.rulerUp,     (0, 50, apWidth, 50))
    self.canvasArray[4].coords(self.rulerDown,   (0, apHeight-50, apWidth, apHeight-50))
    self.canvasArray[4].coords(self.rulerLeft,   (50, 0, 50, apHeight))
    self.canvasArray[4].coords(self.rulerRight,  (apWidth-50, 0, apWidth-50, apHeight))

    self.canvasArray[1].coords(self.handleUp,    (50-5, 80, 50+5, 99))
    self.canvasArray[7].coords(self.handleDown,  (apWidth-50-5, 0, apWidth-50+5, 19))
    self.canvasArray[3].coords(self.handleLeft,  (80, 45, 99, 55))
    self.canvasArray[5].coords(self.handleRight, (0, apHeight-50-5, 19, apHeight-50+5))
    
  def bindHandle(self, handle, canvasId) :
    self.canvasArray[canvasId].tag_bind(handle, '<Button-1>', lambda event, id = canvasId : self.on_click(event, id))
    self.canvasArray[canvasId].tag_bind(handle, '<B1-Motion>', lambda event, id = canvasId : self.on_drag(event, id))

  def on_click(self, event, canvasId):
    self.dragData["x"] = event.x
    self.dragData["y"] = event.y
    self.dragData["id"] = canvasId

  def on_drag(self, event, canvasId):
    dx = event.x - self.dragData["x"]
    dy = event.y - self.dragData["y"]
    
    if (canvasId == 1) :
      self.canvasArray[1].move(self.handleUp, dx, 0)
      self.canvasArray[4].move(self.rulerLeft, dx, 0)
    elif (canvasId == 3) :
      self.canvasArray[3].move(self.handleLeft, 0, dy)
      self.canvasArray[4].move(self.rulerUp, 0, dy)
    elif (canvasId == 5) :
      self.canvasArray[5].move(self.handleRight, 0, dy)
      self.canvasArray[4].move(self.rulerDown, 0, dy)
    elif (canvasId == 7) :
      self.canvasArray[7].move(self.handleDown, dx, 0)
      self.canvasArray[4].move(self.rulerRight, dx, 0)

    self.dragData["x"] = event.x
    self.dragData["y"] = event.y

  @property
  def visible(self) :
    return self._visible

  @visible.setter
  def visible(self, val) :
    
    if val :
      self.canvasArray[4].itemconfig(self.rulerLeft, state = "normal")
      self.canvasArray[4].itemconfig(self.rulerRight, state = "normal")
      self.canvasArray[4].itemconfig(self.rulerUp, state = "normal")
      self.canvasArray[4].itemconfig(self.rulerDown, state = "normal")
      
      self.canvasArray[3].itemconfig(self.handleLeft, state = "normal")
      self.canvasArray[5].itemconfig(self.handleRight, state = "normal")
      self.canvasArray[1].itemconfig(self.handleUp, state = "normal")
      self.canvasArray[7].itemconfig(self.handleDown, state = "normal")
    else :
      self.canvasArray[4].itemconfig(self.rulerLeft, state = "hidden")
      self.canvasArray[4].itemconfig(self.rulerRight, state = "hidden")
      self.canvasArray[4].itemconfig(self.rulerUp, state = "hidden")
      self.canvasArray[4].itemconfig(self.rulerDown, state = "hidden")
      
      self.canvasArray[3].itemconfig(self.handleLeft, state = "hidden")
      self.canvasArray[5].itemconfig(self.handleRight, state = "hidden")
      self.canvasArray[1].itemconfig(self.handleUp, state = "hidden")
      self.canvasArray[7].itemconfig(self.handleDown, state = "hidden")
    
    self._visible = val





# Callback functions
def on_screenshot(event):
  global captureCount

  x1 = canvasArray[4].winfo_rootx()
  y1 = canvasArray[4].winfo_rooty()
  x2 = x1 + canvasArray[4].winfo_width()
  y2 = y1 + canvasArray[4].winfo_height()

  # Turn off the rulers, we don't want them in the screenshot
  ruler.visible = False
  captureWin.update()

  screenshot = ImageGrab.grab((x1,y1,x2,y2))
  screenshot.save(f"./songs/scoreShotDB/screenshot_{captureCount}.png")
  
  # Turn the rulers back on
  ruler.visible = True

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

def on_snapshotSel(event) :
  i = captureListBox.curselection()
    
  if i :
    imgName = captureListBox.get(i)

    x = ImageTk.PhotoImage(Image.open(f"./songs/scoreShotDB/{imgName}"))
    imgbox.config(image = x)
    imgbox.image = x
    




print(f"================================================================================")
print(f"SCORESHOT CAPTURE - v0.1 (September 2024)")
print(f"================================================================================")
print("Shortcuts:")
print("- Left/Right/Up/Down     : move the capture window pixel by pixel")
print("- Mouse wheel up         : move the capture windo position up by 1 pixel")
print("- Mouse wheel down       : move the capture windo position down by 1 pixel")
print("- Alt + Mouse wheel up   : move the capture windo position right by 1 pixel")
print("- Alt + Mouse wheel down : move the capture windo position left by 1 pixel")
print("- 's'                    : take snapshot")
print("- 'q'                    : exit app")








# Create the main window
root = tk.Tk()
root.geometry("1500x500")
root.title("scoreShot - Capture database v0.1 [ALPHA] (September 2024)")
root.resizable(0, 0)
root.bind('<q>', on_quit)




root.grid_columnconfigure(0, minsize = 100)
root.grid_columnconfigure(1, weight = 1)




availableLbl = ttk.Label(root, text = "Snapshots:")
captureList = []
for fileName in os.listdir("./songs/scoreShotDB/") :
  if fileName.endswith(".png"):
    captureList.append(fileName)
captureListVar = tk.StringVar(value = captureList)
captureListBox = tk.Listbox(root, listvariable = captureListVar, width = 30, font = ("Consolas", 10))
x = ImageTk.PhotoImage(Image.open("./songs/scoreShotDB/screenshot_0.png"))
imgbox = tk.Label(root, image = x)


availableLbl.grid(column = 0, row = 0, columnspan = 1, rowspan = 1, sticky = "sw")
captureListBox.grid(column = 0, row = 1, columnspan = 1, rowspan = 1)
imgbox.grid(column = 1, row = 1, columnspan = 1, rowspan = 1)



captureWin = tk.Toplevel(root)
captureWin.geometry("1250x440")
captureWin.title("scoreShot - Capture tool v0.1 [ALPHA] (September 2024)")


# Capture window is always on top
captureWin.attributes("-topmost", True)



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
    if ((row == 0) or (row == 2) or (col == 0) or (col == 2)) :
      c = tk.Canvas(captureWin, bg = colors[color_index], highlightthickness = 0, width = BORDER_SIZE, height = BORDER_SIZE)
    else: 
      c = tk.Canvas(captureWin, bg = colors[color_index], highlightthickness = 0)
    c.grid(row = row, column = col, sticky = "nsew")
    canvasArray.append(c)



ruler = Ruler(canvasArray)



def on_resize(event) :
  ruler.update()



captureWin.attributes("-transparentcolor", "red")

captureWin.bind('<Up>', on_moveWindow)
captureWin.bind('<Down>', on_moveWindow)
captureWin.bind('<Left>', on_moveWindow)
captureWin.bind('<Right>', on_moveWindow)
captureWin.bind('<MouseWheel>', on_mouseWheel)
captureWin.bind('<Configure>', on_resize)
captureWin.bind('<s>', on_screenshot)
captureWin.bind('<q>', on_quit)

captureListBox.bind("<<ListboxSelect>>", on_snapshotSel)

captureCount = 0

#update_mouse_position()

root.protocol("WM_DELETE_WINDOW", on_quit)


root.mainloop()
