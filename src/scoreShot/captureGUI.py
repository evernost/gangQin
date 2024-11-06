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
import configparser
import database
import os
from PIL import ImageGrab, ImageTk, Image
import ruler
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

BORDER_SIZE = 100



# =============================================================================
# Main code
# =============================================================================
class CaptureGUI :

  """
  Defines the class for the main GUI of the scoreShot (capture) app.
  """  
  def __init__(self, root) :
    
    self.root = root

    # [MAIN WINDOW] Properties
    self.root.geometry("1500x500")
    self.root.title("scoreShot - Capture database v0.1 [ALPHA] (October 2024)")
    self.root.resizable(0, 0)

    # [MAIN WINDOW] Widgets
    self.availableLbl = ttk.Label(self.root, text = "Snapshots:")
    self.snapshotListbox = tk.Listbox(self.root, width = 30, font = ("Consolas", 10))
    self.imgbox = tk.Label(self.root, text = "*** No signal ***")
    
    # [MAIN WINDOW] Layout
    self.root.grid_columnconfigure(0, minsize = 100)
    self.root.grid_columnconfigure(1, weight = 1)
    self.availableLbl.grid(column = 0, row = 0, columnspan = 1, rowspan = 1, sticky = "sw")
    self.snapshotListbox.grid(column = 0, row = 1, columnspan = 1, rowspan = 1)
    self.imgbox.grid(column = 1, row = 1, columnspan = 1, rowspan = 1)

    # [MAIN WINDOW] Keyboard bindings
    self.root.bind("<q>"      , self.CLBK_onQuit)
    self.root.bind("<Escape>" , self.CLBK_onEsc)
    self.root.bind("<Delete>" , self.CLBK_onDel)
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
    self.recallImg = tk.Label(self.captureWin)
    self.recallImg.grid(row = 1, column = 1, sticky = "nsew")
    self.recallImg.lower()

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
    self.captureWin.bind("<Up>"         , self.CLBK_onMoveWindow)
    self.captureWin.bind("<Down>"       , self.CLBK_onMoveWindow)
    self.captureWin.bind("<Left>"       , self.CLBK_onMoveWindow)
    self.captureWin.bind("<Right>"      , self.CLBK_onMoveWindow)
    self.captureWin.bind("<MouseWheel>" , self.CLBK_onMouseWheel)
    self.captureWin.bind("<Configure>"  , self.CLBK_onResize)
    self.captureWin.bind('<KeyPress>'   , self.CLBK_onKeyPress)
    self.captureWin.bind('<KeyRelease>' , self.CLBK_onKeyRelease)
    self.captureWin.bind("<Escape>"     , self.CLBK_onEsc)
    self.captureWin.bind("<l>"          , self.CLKB_onToggleLock)
    self.captureWin.bind("<s>"          , self.CLBK_onScreenshot)
    self.captureWin.bind("<q>"          , self.CLBK_onQuit)
    
    
    self.snapshotListbox.bind("<<ListboxSelect>>", self.CLBK_snapshotListboxClick)

    self.GUIConfigFile = ""

    self.GUIResizeLocked = False



  # ---------------------------------------------------------------------------
  # METHOD EditorGUI.loadDatabase()
  # ---------------------------------------------------------------------------
  def loadDatabase(self, songFile) :
    """
    Loads the snapshot database of the song and restore the application
    settings.
    """
    
    # Try to load the database, creates one if it does not exist
    self.db = database.Database(songFile)

    # Update the GUI listbox
    if not(self.db.isEmpty) :
      self._updateListBox()

    
    
  # ---------------------------------------------------------------------------
  # METHOD EditorGUI.loadGUIConfig()
  # ---------------------------------------------------------------------------
  def loadGUIConfig(self) :
    """
    Loads the GUI configuration file (window geometry, ruler position etc.)
    in a .conf file that can be restored later.
    """
      
    self.GUIConfigFile = f"{self.db.depotFolder}/GUIConfig.ini"
    songName = self.db.songName

    # Try to load a configuration file
    GUIConfigData = configparser.ConfigParser()
    if os.path.exists(self.GUIConfigFile) :
      GUIConfigData.read(self.GUIConfigFile)

      # Adjust the window
      if songName in GUIConfigData :
        windowWidth   = int(GUIConfigData[songName]["window_width"])
        windowHeight  = int(GUIConfigData[songName]["window_height"])
        handleLeft    = int(GUIConfigData[songName]["handle_left"])
        handleRight   = int(GUIConfigData[songName]["handle_right"])
        handleUp      = int(GUIConfigData[songName]["handle_up"])
        handleDown    = int(GUIConfigData[songName]["handle_down"])
        
        self.captureWin.geometry(f"{windowWidth}x{windowHeight}")
        self.captureWin.update()
        self.ruler.setHandles(handleLeft, handleRight, handleUp, handleDown)

        print("[INFO] Capture window settings restored from last session. Press the ESC key to load defaults.")



  # ---------------------------------------------------------------------------
  # METHOD EditorGUI.saveGUIConfig()
  # ---------------------------------------------------------------------------
  def saveGUIConfig(self) :
    """
    Saves the GUI settings (window geometry, ruler position etc.) to a configuration
    file that can be restored upon next session.
    """
    
    geometry = self.captureWin.geometry()
    (windowWidth, windowHeight, x, y) = map(int, geometry.replace("x", "+").split("+"))
    (handleLeft, handleRight, handleUp, handleDown) = self.ruler.getHandles()

    GUIConfigData = configparser.ConfigParser()
    GUIConfigData[self.db.songName] = {
      "window_width"  : windowWidth,
      "window_height" : windowHeight,
      "handle_left"   : handleLeft,
      "handle_right"  : handleRight,
      "handle_up"     : handleUp,
      "handle_down"   : handleDown
    }
    with open(self.GUIConfigFile, "w") as configfile :
      GUIConfigData.write(configfile)
  


  # ---------------------------------------------------------------------------
  # METHOD EditorGUI._updateListBox()
  # ---------------------------------------------------------------------------
  def _updateListBox(self) :
    """
    Updates the content of the snapshot selection listbox with the current 
    state of the database.
    """

    L = self.db.getListBoxDescriptor()

    self.snapshotListbox.delete(0, tk.END)
    for item in L :
      self.snapshotListbox.insert(tk.END, item)
    


  # ---------------------------------------------------------------------------
  # METHOD EditorGUI._setRecallImage()
  # ---------------------------------------------------------------------------
  def _setRecallImage(self) :
    """
    Loads the "recall image" with the appropriate image file.
    """
    
    if not(self.db.isEmpty) :
      s = self.db.snapshots[self.db.indexLastInsertion]
      
      print("[DEBUG] EditorGUI._setRecallImage: section is TODO!")
      #x = ImageTk.PhotoImage(Image.open(f"{SCORE_DB_DIR}/screenshot_0.png"))

    else :
      print("[DEBUG] EditorGUI._setRecallImage: database is empty, no image to recall!")



  # ---------------------------------------------------------------------------
  # METHOD EditorGUI._exitChecks()
  # ---------------------------------------------------------------------------
  def _exitChecks(self) :
    """
    Define here all the actions to be done before leaving the app.
    Typically, look for unsaved changes.
    """
    
    if self.db.hasUnsavedChanges :

      # Remove the app windows      
      self.root.withdraw()
      self.captureWin.withdraw()
      
      if (len(self.db.changeLog) > 1) :
        msg = "Save the following change?" + "\n" + self.db.changeLog[0]
      
      else :
        msg = "Save the following changes?" + "\n"
        for (index, change) in enumerate(self.db.changeLog) :
          if (index >= 5) :
            msg += "..."
            break
          else :
            msg += change

      saveReq = messagebox.askyesno("Exit", msg)
      if saveReq :
        self.db.save()
        self.saveGUIConfig()
        
        

  # ---------------------------------------------------------------------------
  # Callbacks methods
  # ---------------------------------------------------------------------------
  
  
  # -----------
  # Mouse wheel 
  # -----------
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



  # --------------
  # 'ESC' keypress
  # --------------
  def CLBK_onEsc(self, event) :
    """
    CALLBACK: on "Esc" key press
    """
    
    self.captureWin.geometry("1250x440")
    self.captureWin.update()
    self.ruler.setHandlesDefault()
    print("[INFO] Capture window reset to default size.")



  # ------------
  # 's' keypress
  # ------------
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

    # Update the content of the snapshot listbox
    self._updateListBox()



  # ------------------------------
  # Click event (snapshot Listbox)
  # ------------------------------
  def CLBK_snapshotListboxClick(self, event) :
    index = self.snapshotListbox.curselection()

    if index :
      #print(f"[DEBUG] Now selecting snapshot index: {index[0]}")

      imgName = self.db.getSnapshotFileByIndex(index[0])

      x = ImageTk.PhotoImage(Image.open(imgName))

      # TODO: resize so that the picture occupies the same real estate no
      # matter what (even if there was some screen scaling)
      # ...


      self.imgbox.config(image = x)
      self.imgbox.image = x



  # ---------------
  # 'Del' key press
  # ---------------
  def CLBK_onDel(self, event) :
    print("[DEBUG] 'Del' key is not handled yet.")

  # ---------------
  # Key press (any)
  # ---------------
  def CLBK_onKeyPress(self, event) :
    if (event.char == "r") :
      self.recallImg.lift()

  # -----------------
  # Key release (any)
  # -----------------
  def CLBK_onKeyRelease(self, event) :
    if (event.char == "r") :
      self.recallImg.lower()


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


  def CLBK_onResize(self, event) :
    self.ruler.updateOnResize()


  def CLKB_onToggleLock(self, event) :
    if not(self.GUIResizeLocked) :
      self.captureWin.resizable(False, False)
      print("[DEBUG] Locked!")
    else :
      self.captureWin.resizable(True, True)

    self.GUIResizeLocked = not(self.GUIResizeLocked)


  # --------
  # App exit
  # --------
  def CLBK_onQuit(self, event = None) : 
    self._exitChecks()
    print("Exiting app...")
    self.root.destroy()




# =============================================================================
# Unit tests
# =============================================================================
if (__name__ == "__main__") :
  print("[INFO] There are no unit tests available for 'editorGUI.py'")



