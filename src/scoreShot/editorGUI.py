# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : editorGUI
# File name     : editorGUI.py
# Purpose       : self-contained class with all the appropriate elements to 
#                 interact with the GUI.
# Author        : QuBi (nitrogenium@hotmail.com)
# Creation date : Sunday, 07 October 2024
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================



# =============================================================================
# External libs 
# =============================================================================
import database
import os
from PIL import ImageGrab, ImageTk, Image
import ruler
import snapshot
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk




# =============================================================================
# Constants pool
# =============================================================================
# Some high resolution screens (typically 4k) use a scaling factor that messes 
# with the coordinates of 'Imagegrab'.
# Declare here the scaling that applies to you:
# Zoom factor 100%: SCREEN_SCALING = 1.0
# Zoom factor 250%: SCREEN_SCALING = 2.5
SCREEN_SCALING = 1.0

SCORE_DB_DIR = "./snaps"

BORDER_SIZE = 100



# =============================================================================
# Main code
# =============================================================================
class EditorGUI :

  """
  Defines the class for the main GUI of the scoreShot (capture) app.
  """  
  def __init__(self, root) :
    
    self.root = root
    
    # [MAIN WINDOW] Properties
    self.root.geometry("1500x500")
    self.root.title("scoreShot - Capture database v0.1 [ALPHA] (September 2024)")
    self.root.resizable(0, 0)

    # [MAIN WINDOW] Widgets
    self.availableLbl = ttk.Label(self.root, text = "Snapshots:")
    self.captureListBox = tk.Listbox(self.root, width = 30, font = ("Consolas", 10))
    # x = ImageTk.PhotoImage(Image.open(f"{SCORE_DB_DIR}/screenshot_0.png"))
    # imgbox = tk.Label(root, image = x)
    self.imgbox = tk.Label(self.root, text = "*** No signal ***")
    
    # [MAIN WINDOW] Layout
    self.root.grid_columnconfigure(0, minsize = 100)
    self.root.grid_columnconfigure(1, weight = 1)
    self.availableLbl.grid(column = 0, row = 0, columnspan = 1, rowspan = 1, sticky = "sw")
    self.captureListBox.grid(column = 0, row = 1, columnspan = 1, rowspan = 1)
    self.imgbox.grid(column = 1, row = 1, columnspan = 1, rowspan = 1)

    # [MAIN WINDOW] Keyboard bindings
    self.root.bind('<q>', self.CLBK_onQuit)
    self.root.protocol("WM_DELETE_WINDOW", self.CLBK_onQuit)



    # [CAPTURE WINDOW] Properties
    self.captureWin = tk.Toplevel(self.root)
    self.captureWin.geometry("1250x440")
    self.captureWin.title("scoreShot - Capture tool v0.1 [ALPHA] (October 2024)")
    self.captureWin.attributes("-topmost", True)  # Make it always on top

    # [CAPTURE WINDOW] Layout
    self.captureWin.grid_columnconfigure(0, minsize = BORDER_SIZE)
    self.captureWin.grid_columnconfigure(1, weight = 1)
    self.captureWin.grid_columnconfigure(2, minsize = BORDER_SIZE)

    self.captureWin.grid_rowconfigure(0, minsize = BORDER_SIZE)
    self.captureWin.grid_rowconfigure(1, weight = 1)
    self.captureWin.grid_rowconfigure(2, minsize = BORDER_SIZE)

    # [CAPTURE WINDOW] Widgets
    self.canvasArray = []
    for row in range(3) :
      for col in range(3) :
        i = (col + row*3)
        
        if (i == 4) :
          color = "red"
        elif ((i % 2) == 0) :
          color = "lightsteelblue"
        else :
          color = "lightblue"
        
        # The "border" canvases have a fixed size
        if ((row == 0) or (row == 2) or (col == 0) or (col == 2)) :
          c = tk.Canvas(self.captureWin, bg = color, highlightthickness = 0, width = BORDER_SIZE, height = BORDER_SIZE)
        
        # The middle canvas (capture aperture) has a variable size
        elif ((row == 1) and (col == 1)) :
          c = tk.Canvas(self.captureWin, bg = color, highlightthickness = 2, highlightbackground = "blue")
        else :
          c = tk.Canvas(self.captureWin, bg = color, highlightthickness = 0)
        
        c.grid(row = row, column = col, sticky = "nsew")
        self.canvasArray.append(c)

    # Bind the red color (unused in the palette) with the transparency property.
    self.captureWin.attributes("-transparentcolor", "red")

    # Ruler widget
    self.ruler = ruler.Ruler(self.canvasArray)


    
    # [CAPTURE WINDOW] Keyboard bindings
    self.captureWin.bind("<Up>", self.CLBK_onMoveWindow)
    self.captureWin.bind("<Down>", self.CLBK_onMoveWindow)
    self.captureWin.bind("<Left>", self.CLBK_onMoveWindow)
    self.captureWin.bind("<Right>", self.CLBK_onMoveWindow)
    self.captureWin.bind("<MouseWheel>", self.CLBK_onMouseWheel)
    self.captureWin.bind("<Configure>", self.CLBK_onResize)
    self.captureWin.bind('<KeyPress>', self.CLBK_onKeyPress)
    self.captureWin.bind('<KeyRelease>', self.CLBK_onKeyRelease)
    self.captureWin.bind("<s>", self.CLBK_onScreenshot)
    self.captureWin.bind("<q>", self.CLBK_onQuit)

    self.captureListBox.bind("<<ListboxSelect>>", self.CLBK_onSnapshotSel)

  

  # ---------------------------------------------------------------------------
  # METHOD EditorGUI.loadDatabase()
  # ---------------------------------------------------------------------------
  def loadDatabase(self, songFile) :
    """
    Loads the snapshot database of the song.
    """
    self.db = database.Database(songFile)

    if not(self.db.isEmpty) :
      
      
      # Fill in the listbox
      # captureList = []
      # for fileName in os.listdir(SCORE_DB_DIR) :
      #   if fileName.endswith(".png"):
      #     captureList.append(fileName)
      # captureListVar = tk.StringVar(value = captureList)
      # captureListBox = tk.Listbox(root, listvariable = captureListVar, width = 30, font = ("Consolas", 10))
      print("TODO")


      # Show the first image of the list
      # TODO
    
      # Define the recall image
      self._setRecallImage()



  # ---------------------------------------------------------------------------
  # METHOD EditorGUI._setRecallImage()
  # ---------------------------------------------------------------------------
  def _setRecallImage(self) :
    """
    TODO
    """
    x = ImageTk.PhotoImage(Image.open(f"{SCORE_DB_DIR}/screenshot_0.png"))
    self.recallImg = tk.Label(self.captureWin, image = x)
    self.recallImg.grid(row = 1, column = 1, sticky = "nsew")
    self.recallImg.lower()



  # ---------------------------------------------------------------------------
  # METHOD EditorGUI._exitChecks()
  # ---------------------------------------------------------------------------
  def _exitChecks(self) :
    """
    Define here all the actions to be done before leaving the app.
    Typically, look for unsaved changes.
    """
    if self.db.hasUnsavedChanges :
      save = messagebox.askyesno("Exit", "Save the unsaved changes?")

      # Save to JSON
      # ...
      
    self.root.withdraw()
    self.captureWin.withdraw()
      



  # ---------------------------------------------------------------------------
  # Callbacks methods
  # ---------------------------------------------------------------------------
  def CLBK_onQuit(self, event = None) : 
    self._exitChecks()
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
    
    # no(Shift key) + mousewheel
    else :
      if (event.delta > 0) :
        self.captureWin.geometry(f"+{x}+{y-1}")
      elif (event.delta < 0) :
        self.captureWin.geometry(f"+{x}+{y+1}")



  def CLBK_onScreenshot(self, event) :
    # Get the coordinates of the aperture 
    x1 = self.canvasArray[4].winfo_rootx()*SCREEN_SCALING
    y1 = self.canvasArray[4].winfo_rooty()*SCREEN_SCALING
    x2 = x1 + self.canvasArray[4].winfo_width()*SCREEN_SCALING
    y2 = y1 + self.canvasArray[4].winfo_height()*SCREEN_SCALING

    # Turn off the ruler display
    # (We don't want them in the screenshot)
    self.ruler.visible = False
    self.canvasArray[4].config(highlightthickness = 0)
    self.captureWin.update() # Force the update of the tkinter window

    # Capture!
    screenshotImg = ImageGrab.grab((x1,y1,x2,y2))
    self.db.insert(screenshotImg)

    
    # Turn on the ruler display
    self.ruler.visible = True
    self.canvasArray[4].config(highlightthickness = 2)

    



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



  def CLBK_onSnapshotSel(self, event) :
    index = self.captureListBox.curselection()
    if index :
      imgName = self.captureListBox.get(index)

      x = ImageTk.PhotoImage(Image.open(f"{SCORE_DB_DIR}/{imgName}"))

      # TODO: resize so that the picture occupies the same real estate no
      # matter what (even if there was some screen scaling)
      # ...


      self.imgbox.config(image = x)
      self.imgbox.image = x



  def CLBK_onKeyPress(self, event) :
    if (event.char == 'r') :
      self.recallImg.lift()



  def CLBK_onKeyRelease(self, event) :
    if (event.char == "r") :
      self.recallImg.lower()



  def CLBK_onResize(self, event) :
    self.ruler.update()







  # ---------------------------------------------------------------------------
  # METHOD Database._makeDatabaseFileName()
  # ---------------------------------------------------------------------------





# =============================================================================
# Unit tests
# =============================================================================
if (__name__ == "__main__") :
  print("[INFO] There are no unit tests available for 'editorGUI.py'")



