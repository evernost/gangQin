# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : fileSelectionGUI
# File name     : fileSelectionGUI.py
# Purpose       : shows the song selection GUI for scoreShot_capture/fusion
# Author        : QuBi (nitrogenium@outlook.fr)
# Creation date : Sunday, 01 December 2024
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# External libs
# =============================================================================
# Project specific constants
from src.commons import *

import os
import tkinter as tk
from tkinter import ttk



# =============================================================================
# Main code
# =============================================================================

def getFileListByExt(folderPath, extension) :
  """
  Returns a sorted list of all files of a given extension in a specific
  directory.
  """
  
  fileList = ["None"]
  for filename in os.listdir(folderPath) :
    if filename.endswith(extension):
      fileList.append(os.path.join(folderPath, filename))

  fileList.sort()
  return fileList


def new() :
  return FileSelectionGUI()





class FileSelectionGUI :

  """
  TODO
  """

  def __init__(self) :
    self.songFile = ""
    self.title = "Song selection"
    self.root = None
    
    self.songList = getFileListByExt(SONG_PATH, ".pr")



  # ---------------------------------------------------------------------------
  # METHOD FileSelectionGUI.setTitle()
  # ---------------------------------------------------------------------------
  def setTitle(self, title) :
    """
    Sets the title of the GUI.
    """
    
    self.title = title



  # ---------------------------------------------------------------------------
  # METHOD FileSelectionGUI.show()
  # ---------------------------------------------------------------------------
  def show(self) :
    """
    Shows the song file selection GUI.
    Returns a string with the full name of the file (path included) upon exiting.
    """
    
    self.root = tk.Tk()
    self.root.title(self.title)
    self.root.resizable(0, 0)

    fileSelFrame = ttk.LabelFrame(self.root, text = "File input")
    fileSelFrame.grid(row = 0, column = 0, columnspan = 3, padx = 10, pady = 5, sticky = "e")
    
    label1 = tk.Label(fileSelFrame, text = "Select a song:")
    label1.grid(row = 2, column = 0, padx = 3, pady = 1, sticky = "w")

    self.comboFile = ttk.Combobox(fileSelFrame, values = [], state = "readonly")    
    self.comboFile["values"] = [os.path.basename(file) for file in self.songList]
    self.comboFile.set(self.comboFile["values"][0])
    self.comboFile["width"] = 80
    self.comboFile.grid(row = 3, column = 0, columnspan = 3, padx = 3, pady = 5, sticky = "e")
    
    buttonStart = tk.Button(self.root, text = "Start", command = self.CLBK_onStart, default = tk.ACTIVE)
    buttonStart.grid(row = 1, column = 2, padx = 10, pady = 20, sticky = "e")
    buttonStart["width"] = 20
    if (len(self.songList) == 1 and self.songList[0] == "None") :
      buttonStart.config(state = "disabled")
    else :
      buttonStart.config(state = "normal")

    buttonQuit = tk.Button(self.root, text = "Quit", command = self.CLBK_onQuit)
    buttonQuit.grid(row = 1, column = 0, padx = 10, pady = 20, sticky = "w")
    buttonQuit["width"] = 10
    buttonQuit.config(state = "normal")

    # Bindings
    self.root.bind("<Escape>",  self.CLBK_onQuit)
    self.root.bind("<q>",       self.CLBK_onQuit)
    self.root.bind("<Return>",  self.CLBK_onStart)

    self.centerWindow()
    self.root.mainloop()
    
    self.saveDefault()

    return self.songFile



  # ---------------------------------------------------------------------------
  # METHOD FileSelectionGUI.centerWindow()
  # ---------------------------------------------------------------------------
  def centerWindow(self) :
    """
    Centers the GUI on screen.
    """
    
    self.root.update_idletasks()
    
    w = self.root.winfo_reqwidth()
    h = self.root.winfo_reqheight()

    screen_width = self.root.winfo_screenwidth()
    screen_height = self.root.winfo_screenheight()

    x = (screen_width - w) // 2
    y = (screen_height - h) // 2

    self.root.geometry(f"{w}x{h}+{x}+{y}")



  # ---------------------------------------------------------------------------
  # METHOD FileSelectionGUI.CLBK_onQuit()
  # ---------------------------------------------------------------------------
  def CLBK_onQuit(self, event = None) :
    exit()



  # ---------------------------------------------------------------------------
  # METHOD FileSelectionGUI.CLBK_onStart()
  # ---------------------------------------------------------------------------
  def CLBK_onStart(self, event = None) :
    self.songFile = self.songList[self.comboFile.current()]
    self.root.destroy()



  # ---------------------------------------------------------------------------
  # METHOD FileSelectionGUI.loadDefault()
  # ---------------------------------------------------------------------------
  def loadDefault(self) :
    """
    Loads the file that has been selected last time the app was called, so 
    that the selection menu can propose this one first.
    """
    print("[DEBUG] FileSelectionGUI.loadDefault(): todo!")



  # ---------------------------------------------------------------------------
  # METHOD FileSelectionGUI.saveDefault()
  # ---------------------------------------------------------------------------
  def saveDefault(self) :
    """
    Saves the selected file to a .ini file so that the app defaults to the 
    last file upon next start.
    """
    print("[DEBUG] FileSelectionGUI.saveDefault(): todo!")



# =============================================================================
# Unit tests
# =============================================================================
if (__name__ == "__main__") :
  gui = new()
  songFile = gui.show()
  print(f"Selected song: '{songFile}'")

