# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : editorGUI
# File name     : editorGUI.py
# Purpose       : 
# Author        : QuBi (nitrogenium@hotmail.com)
# Creation date : Sunday, 07 October 2024
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================



# =============================================================================
# Tasks
# =============================================================================
# None listed yet.



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


BORDER_SIZE = 100



# =============================================================================
# Main code
# =============================================================================
class EditorGUI :

  """
  Class for the main GUI of the scoreShot (capture) app.
  """  
  def __init__(self, root) :
    
    self.root = root
    
    # Main window properties
    self.root.geometry("1500x500")
    self.root.title("scoreShot - Capture database v0.1 [ALPHA] (September 2024)")
    self.root.resizable(0, 0)

    # Add widgets
    self.availableLbl = ttk.Label(self.root, text = "Snapshots:")
    self.captureListBox = tk.Listbox(self.root, width = 30, font = ("Consolas", 10))
    # x = ImageTk.PhotoImage(Image.open(f"{SCORE_DB_DIR}/screenshot_0.png"))
    # imgbox = tk.Label(root, image = x)
    self.imgbox = tk.Label(self.root, text = "*** No signal ***")
    
    # captureList = []
    # for fileName in os.listdir(SCORE_DB_DIR) :
    #   if fileName.endswith(".png"):
    #     captureList.append(fileName)
    # captureListVar = tk.StringVar(value = captureList)
    # captureListBox = tk.Listbox(root, listvariable = captureListVar, width = 30, font = ("Consolas", 10))

    # Main window layout
    self.root.grid_columnconfigure(0, minsize = 100)
    self.root.grid_columnconfigure(1, weight = 1)
    self.availableLbl.grid(column = 0, row = 0, columnspan = 1, rowspan = 1, sticky = "sw")
    self.captureListBox.grid(column = 0, row = 1, columnspan = 1, rowspan = 1)
    self.imgbox.grid(column = 1, row = 1, columnspan = 1, rowspan = 1)



    # Capture window properties
    self.captureWin = tk.Toplevel(self.root)
    self.captureWin.geometry("1250x440")
    self.captureWin.title("scoreShot - Capture tool v0.1 [ALPHA] (October 2024)")

    # Make it always on top
    self.captureWin.attributes("-topmost", True)

    # Capture window layout
    
    self.captureWin.grid_columnconfigure(0, minsize = BORDER_SIZE)
    self.captureWin.grid_columnconfigure(1, weight = 1)
    self.captureWin.grid_columnconfigure(2, minsize = BORDER_SIZE)

    self.captureWin.grid_rowconfigure(0, minsize = BORDER_SIZE)
    self.captureWin.grid_rowconfigure(1, weight = 1)
    self.captureWin.grid_rowconfigure(2, minsize = BORDER_SIZE)

    colors = ["lightsteelblue", "lightblue", "lightsteelblue", "lightblue", 
          "red", "lightblue", "lightsteelblue", "lightblue", "lightsteelblue"]

    self.canvasArray = []
    for row in range(3):
      for col in range(3):
        color_index = row * 3 + col
        
        # The "border" canvases have a fixed size
        if ((row == 0) or (row == 2) or (col == 0) or (col == 2)) :
          c = tk.Canvas(self.captureWin, bg = colors[color_index], highlightthickness = 0, width = BORDER_SIZE, height = BORDER_SIZE)
        
        # The middle canvas (capture aperture) has a variable size
        elif ((row == 1) and (col == 1)) :
          c = tk.Canvas(self.captureWin, bg = colors[color_index], highlightthickness = 2, highlightbackground = "blue")
        else :
          c = tk.Canvas(self.captureWin, bg = colors[color_index], highlightthickness = 0)
        c.grid(row = row, column = col, sticky = "nsew")
        self.canvasArray.append(c)

    # Bind the red color (unused in the palette) with the transparency property.
    self.captureWin.attributes("-transparentcolor", "red")

    x = ImageTk.PhotoImage(Image.open(f"{SCORE_DB_DIR}/screenshot_0.png"))
    recallImg = tk.Label(self.captureWin, image = x)
    recallImg.grid(row = 1, column = 1, sticky = "nsew")
    recallImg.lower()


    # Keyboard bindings
    self.captureWin.bind("<Up>", on_moveWindow)
    self.captureWin.bind("<Down>", on_moveWindow)
    self.captureWin.bind("<Left>", on_moveWindow)
    self.captureWin.bind("<Right>", on_moveWindow)
    self.captureWin.bind("<MouseWheel>", on_mouseWheel)
    self.captureWin.bind("<Configure>", on_resize)
    self.captureWin.bind('<KeyPress>', on_keyPress)
    self.captureWin.bind('<KeyRelease>', on_keyRelease)
    self.captureWin.bind("<s>", on_screenshot)
    self.captureWin.bind("<q>", on_quit)

    captureListBox.bind("<<ListboxSelect>>", on_snapshotSel)



    self.ruler = ruler.Ruler(self.canvasArray)












    # Keyboard bindings
    self.root.bind('<q>', self.CLBK_onQuit)


    self.root.protocol("WM_DELETE_WINDOW", self.CLBK_onQuit)






  
  def CLBK_onQuit(self, event = None) : 
    print("Exiting app...")
    self.root.destroy()



  def CLBK_onMouseWheel(self, event) :
    # Get the current coordinates of the snapshot window
    x = self.captureWin.winfo_x()
    y = self.captureWin.winfo_y()

    # Shift key + mousewheel
    if (event.state & 0x0001) : 
      if (event.delta > 0) :
        self.captureWin.geometry(f"+{x-1}+{y}")
      elif (event.delta < 0) :
        self.captureWin.geometry(f"+{x+1}+{y}")
    
    # Mousewheel
    else :
      if (event.delta > 0) :
        self.captureWin.geometry(f"+{x}+{y-1}")
      elif (event.delta < 0) :
        self.captureWin.geometry(f"+{x}+{y+1}")



  def CLBK_onScreenshot(self, event) :
    # Define the coordinates of the aperture 
    x1 = self.canvasArray[4].winfo_rootx()*SCREEN_SCALING
    y1 = self.canvasArray[4].winfo_rooty()*SCREEN_SCALING
    x2 = x1 + self.canvasArray[4].winfo_width()*SCREEN_SCALING
    y2 = y1 + self.canvasArray[4].winfo_height()*SCREEN_SCALING

    # Turn off the rulers, we don't want them in the screenshot.
    self.rulerObj.visible = False
    self.canvasArray[4].config(highlightthickness = 0)

    self.captureWin.update()

    screenshot = ImageGrab.grab((x1,y1,x2,y2))
    screenshot.save(f"{SCORE_DB_DIR}/screenshot_{captureCount}.png")
    
    # Turn the rulers back on
    self.rulerObj.visible = True
    self.canvasArray[4].config(highlightthickness = 2)

    print(f"[DEBUG] Screenshot saved as 'screenshot_{captureCount}.png'")



  def CLBK_onMoveWindow(self, event) :
    x = self.captureWin.winfo_x()
    y = self.captureWin.winfo_y()

    if (event.keysym == "Up") :
      self.captureWin.geometry(f"+{x}+{y-1}")
    elif (event.keysym == "Down") :
      self.captureWin.geometry(f"+{x}+{y+1}")
    elif (event.keysym == "Left") :
      self.captureWin.geometry(f"+{x-1}+{y}")
    elif (event.keysym == "Right") :
      self.captureWin.geometry(f"+{x+1}+{y}")











  # ---------------------------------------------------------------------------
  # METHOD Database._makeDatabaseFileName()
  # ---------------------------------------------------------------------------





      

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





# -----------------------------------------------------------------------------
# Capture window definition
# -----------------------------------------------------------------------------
# captureWin = tk.Toplevel(root)
# captureWin.geometry("1250x440")
# captureWin.title("scoreShot - Capture tool v0.1 [ALPHA] (October 2024)")

# Capture window is always on top
# captureWin.attributes("-topmost", True)

# Capture window layout
# BORDER_SIZE = 100
# captureWin.grid_columnconfigure(0, minsize = BORDER_SIZE)
# captureWin.grid_columnconfigure(1, weight = 1)
# captureWin.grid_columnconfigure(2, minsize = BORDER_SIZE)

# captureWin.grid_rowconfigure(0, minsize = BORDER_SIZE)
# captureWin.grid_rowconfigure(1, weight = 1)
# captureWin.grid_rowconfigure(2, minsize = BORDER_SIZE)




# # Define a set of distinct colors for the 9 frames
# colors = ["lightsteelblue", "lightblue", "lightsteelblue", "lightblue", 
#           "red", "lightblue", "lightsteelblue", "lightblue", "lightsteelblue"]

# canvasArray = []
# for row in range(3):
#   for col in range(3):
#     color_index = row * 3 + col
    
#     # The "border" canvases have a fixed size
#     if ((row == 0) or (row == 2) or (col == 0) or (col == 2)) :
#       c = tk.Canvas(captureWin, bg = colors[color_index], highlightthickness = 0, width = BORDER_SIZE, height = BORDER_SIZE)
    
#     # The middle canvas (capture aperture) has a variable size
#     elif ((row == 1) and (col == 1)) :
#       c = tk.Canvas(captureWin, bg = colors[color_index], highlightthickness = 2, highlightbackground = "blue")
#     else :
#       c = tk.Canvas(captureWin, bg = colors[color_index], highlightthickness = 0)
#     c.grid(row = row, column = col, sticky = "nsew")
#     canvasArray.append(c)

# # Bind the red color (unused in the palette) with the transparency property.
# captureWin.attributes("-transparentcolor", "red")

# rulerObj = ruler.Ruler(canvasArray)



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




# import tkinter as tk

# class MyApp:
#     def __init__(self, root):
#         # Create and configure window
#         self.root = root
#         self.root.title("My Tkinter App")
        
#         # Variables for GUI state
#         self.counter = 0
#         self.label_text = tk.StringVar(value="Counter: 0")
        
#         # Create widgets
#         self.label = tk.Label(root, textvariable=self.label_text)
#         self.label.pack(pady=10)
        
#         self.increment_button = tk.Button(root, text="Increment", command=self.increment_counter)
#         self.increment_button.pack(pady=5)
        
#         self.decrement_button = tk.Button(root, text="Decrement", command=self.decrement_counter)
#         self.decrement_button.pack(pady=5)

#         self.quit_button = tk.Button(root, text="Quit", command=root.quit)
#         self.quit_button.pack(pady=20)
        
#         # Bind events (e.g., keyboard and mouse)
#         root.bind("<Up>", self.on_key_press_up)
#         root.bind("<Down>", self.on_key_press_down)
    
#     def increment_counter(self):
#         self.counter += 1
#         self.update_label()
    
#     def decrement_counter(self):
#         self.counter -= 1
#         self.update_label()
    
#     def update_label(self):
#         self.label_text.set(f"Counter: {self.counter}")
    
#     def on_key_press_up(self, event):
#         """Callback for Up arrow key press."""
#         self.increment_counter()
    
#     def on_key_press_down(self, event):
#         """Callback for Down arrow key press."""
#         self.decrement_counter()

# # Main application loop
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = MyApp(root)
#     root.mainloop()







