# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : errorReportGUI
# File name     : errorReportGUI.py
# Purpose       : shows the error reporting GUI
# Author        : QuBi (nitrogenium@outlook.fr)
# Creation date : Tuesday, 03 December 2024
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

# List of possible reports:
# 1 - Score: note with incorrect pitch
# 2 - Score: missing note
# 2 - Score: note in excess
# 3 - PlayGlow: not placed accurately
# 4 - PlayGlow: missing
# 5 - Fingersatz: value is dubious
# 6 - Other



# =============================================================================
# Main code
# =============================================================================


def show() :
  """
  Shows the error reporting GUI.
  """

  global errorCode
  errorCode = ""



  # ---------------------------------------------------------------------------
  # GUI exit point
  # ---------------------------------------------------------------------------
  def exitGUI() :
    global errorCode
    #errorCode = ...
    
    root.destroy()



  # ---------------------------------------------------------------------------
  # [CALLBACK] Radio button change handler
  # ---------------------------------------------------------------------------
  def CLBK_onRadioButtonChange() :

    # List files with this extension
    fileList = getFileListByExt(SONG_PATH, fileExt.get())
    
    # No file found
    if not(fileList) :
      fileList = ["None"]
      comboFile["values"] = fileList
      comboFile.set(fileList[0])
      
      buttonOK["state"] = "disabled"
    
    else :
      # Trim the path to the files
      fileListNoPath = [os.path.basename(file) for file in fileList]
      
      comboFile["values"] = fileListNoPath
      comboFile.set(fileListNoPath[0])
      
      buttonOK["state"] = "normal"



  # ---------------------------------------------------------------------------
  # [GUI MANAGEMENT] Window centering
  # ---------------------------------------------------------------------------
  def centerWindow(container) :
    
    # Ensure widgets are updated before calculating size
    container.update_idletasks()
    
    w = container.winfo_reqwidth()
    h = container.winfo_reqheight()

    screen_width = container.winfo_screenwidth()
    screen_height = container.winfo_screenheight()

    x = (screen_width - w) // 2
    y = (screen_height - h) // 2

    container.geometry(f"{w}x{h}+{x}+{y}")



  # ---------------------------------------------------------------------------
  # [GUI DEFINITION] Create the main window
  # ---------------------------------------------------------------------------
  root = tk.Tk()
  root.title("Report error")
  root.resizable(0, 0)



  # ---------------------------------------------------------------------------
  # [GUI DEFINITION] .mid/.pr file selection
  # ---------------------------------------------------------------------------
  fileList = getFileListByExt(SONG_PATH, ".mid")
  if not(fileList) :
    fileList = ["None"]

    
  fileSelFrame = ttk.LabelFrame(root, text = "File input")
  fileSelFrame.grid(row = 0, column = 1, padx = 10, pady = 5, sticky = "e")

  # filterByFrame = tk.Label(fileSelFrame, text = "Filter by:")
  # filterByFrame.grid(row = 0, column = 0, padx = 3, pady = 1, sticky = "w")

  # fileExt = tk.StringVar()
  # radioButton_mid = ttk.Radiobutton(fileSelFrame, text = ".mid file", value = ".mid", variable = fileExt, command = CLBK_onRadioButtonChange)
  # radioButton_pr  = ttk.Radiobutton(fileSelFrame, text = ".pr file" , value = ".pr" , variable = fileExt, command = CLBK_onRadioButtonChange)
  
  # radioButton_mid.grid(row = 0, column = 1, padx = 1, pady = 1, sticky = "w")
  # radioButton_pr.grid(row = 0, column = 2, padx = 1, pady = 1, sticky = "e")

  # # Read the last practiced song, set the .mid/.pr selection accordingly
  # if "song" in configData["DEFAULT"] :
  #   if configData["DEFAULT"]["song"] in getFileListByExt(SONG_PATH, ".mid") + getFileListByExt(SONG_PATH, ".pr") :
  #     (_, lastFileExt) = os.path.splitext(configData["DEFAULT"]["song"])

  #     fileExt.set(lastFileExt)

  #   else :
  #     fileExt.set(".mid")

  # else :
  #   fileExt.set(".mid")

  

  # ---------------------------------------------------------------------------
  # [GUI DEFINITION] Dropdown list for the error code selection
  # ---------------------------------------------------------------------------
  label3 = tk.Label(fileSelFrame, text = "Select a File:")
  label3.grid(row = 2, column = 0, padx = 3, pady = 1, sticky = "w")

  comboFile = ttk.Combobox(fileSelFrame, values = [], state = "readonly")
  comboFile["width"] = 80
  comboFile.grid(row = 3, column = 0, columnspan = 3, padx = 3, pady = 5, sticky = "e")

  fileList = getFileListByExt(SONG_PATH, ".pr")
  comboFile["values"] = [os.path.basename(file) for file in fileList]

  # By default, set to the last song
  if "song" in configData["DEFAULT"] :
    if configData["DEFAULT"]["song"] in getFileListByExt(SONG_PATH, ".mid") + getFileListByExt(SONG_PATH, ".pr") :
      comboFile.set(os.path.basename(configData["DEFAULT"]["song"]))
      
    else :
      print(f"[INFO] The last practiced song is not available ({configData['DEFAULT']['song']})")
      comboFile.set(comboFile["values"][0])

  else :
    comboFile.set(comboFile["values"][0])



  # -----------------------------------------------------------------------------
  # [GUI DEFINITION] OK button
  # -----------------------------------------------------------------------------
  buttonOK = tk.Button(root, text = "Start", command = exitGUI, default = tk.ACTIVE)
  buttonOK.grid(row = 1, column = 1, padx = 10, pady = 20, sticky = "e")
  buttonOK["width"] = 20
  if (len(fileList) == 1 and fileList[0] == "None") :
    buttonOK.config(state = "disabled")
  else :
    buttonOK.config(state = "normal")



  # -----------------------------------------------------------------------------
  # [GUI DEFINITION] Exit button
  # -----------------------------------------------------------------------------
  buttonQuit = tk.Button(root, text = "Quit", command = lambda: exit(0))
  buttonQuit.grid(row = 1, column = 0, padx = 10, pady = 20, sticky = "w")
  buttonQuit["width"] = 10
  buttonQuit.config(state = "normal")

  

  # ---------------
  # Main event loop
  # ---------------
  # Set the select button as the "default" button
  root.bind("<Return>", lambda event = None : buttonOK.invoke())

  centerWindow(root)

  root.mainloop()
  

  # ***** Code beyond this point is run after clicking "OK" *****

  # Save conf to the .ini file  
  configData["DEFAULT"] = {
    "midi_interface": selectedDevice,
    "song": selectedFile
    }

  # Create the ./conf dir if it does not exist
  if not os.path.exists("./conf"):
    os.makedirs("./conf")

  with open("./conf/conf.ini", "w") as configfile :
    configData.write(configfile)

  return (selectedDevice, selectedFile)



# =============================================================================
# Unit tests
# =============================================================================
if (__name__ == "__main__") :
  show()