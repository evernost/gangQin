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
    
    # Lines for the rulers
    self.rulerLeft  = self.canvasArray[4].create_line(0, 0, 0, 1, fill = "black", width = 1, dash = (1, 10))
    self.rulerRight = self.canvasArray[4].create_line(0, 0, 0, 1, fill = "black", width = 1, dash = (1, 10))
    self.rulerUp    = self.canvasArray[4].create_line(0, 0, 0, 1, fill = "black", width = 1, dash = (1, 10))
    self.rulerDown  = self.canvasArray[4].create_line(0, 0, 0, 1, fill = "black", width = 1, dash = (1, 10))

    # Handles to drag and drop the rulers
    self.handleLeft   = self.canvasArray[3].create_rectangle(0, 0, 0, 1, fill = "grey", outline = "grey")
    self.handleRight  = self.canvasArray[5].create_rectangle(0, 0, 0, 1, fill = "grey", outline = "grey")
    self.handleUp     = self.canvasArray[1].create_rectangle(0, 0, 0, 1, fill = "grey", outline = "grey")
    self.handleDown   = self.canvasArray[7].create_rectangle(0, 0, 0, 1, fill = "grey", outline = "grey")

    # Drag and drop information
    self.bindHandle(self.handleLeft, 3)
    self.bindHandle(self.handleRight, 5)
    self.bindHandle(self.handleUp, 1)
    self.bindHandle(self.handleDown, 7)
    self.dragData = {"x": 0, "y": 0, "id": None}

    # Visible property
    self._visible = True

  def updateAfterResize(self) :
    self.canvasArray[4].coords(self.rulerUp,     (0, 50, self.canvasArray[4].winfo_width(), 50))
    self.canvasArray[4].coords(self.rulerDown,   (0, self.canvasArray[4].winfo_height()-50, self.canvasArray[4].winfo_width(), self.canvasArray[4].winfo_height()-50))
    self.canvasArray[4].coords(self.rulerLeft,   (50, 0, 50, self.canvasArray[4].winfo_height()))
    self.canvasArray[4].coords(self.rulerRight,  (self.canvasArray[4].winfo_width()-50, 0, self.canvasArray[4].winfo_width()-50, self.canvasArray[4].winfo_height()))

    self.canvasArray[1].coords(self.handleUp,    (50-5, 80, 50+5, 99))
    self.canvasArray[7].coords(self.handleDown,  (self.canvasArray[4].winfo_width()-50-5, 0, self.canvasArray[4].winfo_width()-50+5, 19))
    self.canvasArray[3].coords(self.handleLeft,  (80, 45, 99, 55))
    self.canvasArray[5].coords(self.handleRight, (0, self.canvasArray[4].winfo_height()-50-5, 19, self.canvasArray[4].winfo_height()-50+5))
    
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



class CaptureBeacon :
  def __init__(self, canvasArray) :
    self.canvasArray = canvasArray

    # Top left beacon
    self.topLeft0 = self.canvasArray[3].create_rectangle(98, 0, 99, 1, fill = "#FF8400", width = 0)
    self.topLeft1 = self.canvasArray[3].create_rectangle(99, 0, 100, 1, fill = "#00FF00", width = 0)
    self.topLeft2 = self.canvasArray[3].create_rectangle(98, 1, 99, 2, fill = "#0000FF", width = 0)
    self.topLeft3 = self.canvasArray[3].create_rectangle(99, 1, 100, 2, fill = "#FFFF00", width = 0)
    
    # Bottom right beacon
    self.bottomRight0 = self.canvasArray[5].create_rectangle(0, 1, 0, 1, fill = "#FF8400", width = 0)
    self.bottomRight1 = self.canvasArray[5].create_rectangle(0, 1, 0, 1, fill = "#00FF00", width = 0)
    self.bottomRight2 = self.canvasArray[5].create_rectangle(0, 1, 0, 1, fill = "#0000FF", width = 0)
    self.bottomRight3 = self.canvasArray[5].create_rectangle(0, 1, 0, 1, fill = "#FFFF00", width = 0)
    
    self.pattern = [0, 255, 42, 213]
    self._visible = False

  def updateAfterResize(self) :
    
    # Bottom right beacon
    x0 = 0; y0 = canvasArray[4].winfo_height()-2
    self.canvasArray[5].coords(self.bottomRight0, (x0, y0, x0+1, y0+1))
    self.canvasArray[5].coords(self.bottomRight1, (x0+1, y0, x0+2, y0+1))
    self.canvasArray[5].coords(self.bottomRight2, (x0, y0+1, x0+1, y0+2))
    self.canvasArray[5].coords(self.bottomRight3, (x0+1, y0+1, x0+2, y0+2))

  def find(imagePath) :
    image = Image.open("./songs/scoreShotDB/screenshot_0.png")

  # @property
  # def visible(self) :
  #   return self._visible

  # @visible.setter
  # def visible(self, val) :
    
  #   if val :
  #     self.canvasArray[4].itemconfig(self.rulerLeft, state = "normal")
  #     self.canvasArray[4].itemconfig(self.rulerRight, state = "normal")
  #     self.canvasArray[4].itemconfig(self.rulerUp, state = "normal")
  #     self.canvasArray[4].itemconfig(self.rulerDown, state = "normal")
      
  #     self.canvasArray[3].itemconfig(self.handleLeft, state = "normal")
  #     self.canvasArray[5].itemconfig(self.handleRight, state = "normal")
  #     self.canvasArray[1].itemconfig(self.handleUp, state = "normal")
  #     self.canvasArray[7].itemconfig(self.handleDown, state = "normal")
  #   else :
  #     self.canvasArray[4].itemconfig(self.rulerLeft, state = "hidden")
  #     self.canvasArray[4].itemconfig(self.rulerRight, state = "hidden")
  #     self.canvasArray[4].itemconfig(self.rulerUp, state = "hidden")
  #     self.canvasArray[4].itemconfig(self.rulerDown, state = "hidden")
      
  #     self.canvasArray[3].itemconfig(self.handleLeft, state = "hidden")
  #     self.canvasArray[5].itemconfig(self.handleRight, state = "hidden")
  #     self.canvasArray[1].itemconfig(self.handleUp, state = "hidden")
  #     self.canvasArray[7].itemconfig(self.handleDown, state = "hidden")
    
  #   self._visible = val







# Callback functions
def take_screenshot(event):
  global captureCount

  x = captureWin.winfo_x()
  y = captureWin.winfo_y()
  width = captureWin.winfo_width()
  height = captureWin.winfo_height()
  
  #bbox = (0, 0, captureWin.winfo_screenwidth(), captureWin.winfo_screenheight())
  
  
  #screenshot = ImageGrab.grab(bbox)
  screenshot = ImageGrab.grab()

  width, height = screenshot.size
  for y in range(height):
    for x in range(width):
      (r,g,b) = screenshot.getpixel((x, y))

      if ((r == 255) and (g == 132) and (b == 0)) :
        print(f"x = {x+2}, y = {y}")





  screenshot.save(f"./songs/scoreShotDB/screenshot_{captureCount}.png")
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
root.title("scoreShot - Capture database v0.1 [ALPHA] (September 2024)")
root.resizable(0, 0)

content = ttk.Frame(root, padding = 20)

availableLbl = ttk.Label(content, text = "Snapshots:")
trackListVar = tk.StringVar(value = [])
trackLst = tk.Listbox(content, listvariable = trackListVar, width = 50, font = ("Consolas", 10))
img = ImageTk.PhotoImage(Image.open("./songs/scoreShotDB/screenshot.png"))
imgbox = tk.Label(root, image = img)



content.grid(column = 0, row = 0)

availableLbl.grid(column = 0, row = 0, columnspan = 1, rowspan = 1, sticky = "w")
trackLst.grid(column = 0, row = 1, columnspan = 1, rowspan = 1)
imgbox.grid(column = 1, row = 1, columnspan = 1, rowspan = 1)



captureWin = tk.Toplevel(root)
captureWin.geometry("1250x440")
captureWin.title("scoreShot - Capture tool v0.1 [ALPHA] (September 2024)")


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
beacon = CaptureBeacon(canvasArray)


def on_resize(event) :
  ruler.updateAfterResize()
  beacon.updateAfterResize()


captureWin.attributes("-transparentcolor", "red")

captureWin.bind('<Up>', on_moveWindow)
captureWin.bind('<Down>', on_moveWindow)
captureWin.bind('<Left>', on_moveWindow)
captureWin.bind('<Right>', on_moveWindow)
captureWin.bind('<MouseWheel>', on_mouseWheel)
captureWin.bind('<Configure>', on_resize)
captureWin.bind('<s>', take_screenshot)
captureWin.bind('<q>', on_quit)

captureCount = 0

# update_mouse_position()

root.protocol("WM_DELETE_WINDOW", on_quit)


root.mainloop()
