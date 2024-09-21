# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : conf
# File name     : conf.py
# Purpose       : provides GUI to configure the main gangQin app
# Author        : QuBi (nitrogenium@hotmail.com)
# Creation date : Sunday, 24 Sept 2023
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# External libs
# =============================================================================
# Project specific constants
from commons import *

import configparser
import mido
import os
import tkinter as tk
from tkinter import ttk



# =============================================================================
# Main code
# =============================================================================
def getFileList(folderPath, extension) :
  """
  todo
  """
  fileList = []
  for filename in os.listdir(folderPath) :
    if filename.endswith(extension):
      fileList.append(os.path.join(folderPath, filename))

  fileList.sort()
  return fileList



# -----------------------------------------------------------------------------
# File selection GUI
# -----------------------------------------------------------------------------
def show() :

  global selectedDevice
  global selectedFile
  selectedDevice = ""
  selectedFile   = ""

  # Try to load a configuration file
  configData = configparser.ConfigParser()
  if os.path.exists("./conf/conf.ini") :
    configData.read("./conf/conf.ini")



  # ---------------------------------------------------------------------------
  # GUI exit point
  # ---------------------------------------------------------------------------
  # Commit the configuration 
  def sendConf() :
    global selectedDevice
    global selectedFile
    
    # Read the file
    fileList = getFileList(SONG_PATH, fileExt.get())
    selectedFile = fileList[comboFile.current()]

    # Read the device
    selectedDevice = comboMidi.get()

    root.destroy()



  # ---------------------------------------------------------------------------
  # [GUI MANAGEMENT] React to a radio button change
  # ---------------------------------------------------------------------------
  def onRadioButtonChange():

    # List files with this extension
    fileList = getFileList(SONG_PATH, fileExt.get())
    
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
  def centerWindow(container):
    
    # Ensure widgets are updated before calculating size
    container.update_idletasks()
    
    w = container.winfo_reqwidth()
    h = container.winfo_reqheight()

    screen_width = container.winfo_screenwidth()
    screen_height = container.winfo_screenheight()

    x = (screen_width - w) // 2
    y = (screen_height - h) // 2

    container.geometry(f"{w}x{h}+{x}+{y}")



  # -----------------------------------------------------------------------------
  # [GUI DEFINITION] Create the main window
  # -----------------------------------------------------------------------------
  root = tk.Tk()
  root.title("New learning session")
  root.resizable(0, 0)



  # -----------------------------------------------------------------------------
  # [GUI DEFINITION] MIDI interface selection
  # -----------------------------------------------------------------------------
  midiInputFrame = ttk.LabelFrame(root, text = "MIDI input")
  midiInputFrame.grid(row = 0, column = 0, padx = 10, pady = 5, sticky = "w")

  # Input device label
  label = tk.Label(midiInputFrame, text = "Select the input device:")
  label.grid(row = 0, column = 0, padx = 10, pady = 1, sticky = "w")

  # Dropdown list for the MIDI selection
  midiDevices = mido.get_input_names()
  midiDevices.append("None")
  comboMidi = ttk.Combobox(midiInputFrame, values = midiDevices, state = "readonly")
  comboMidi.grid(row = 1, column = 0, padx = 10, pady = 5, sticky = "w")
  
  # By default, set to the last used MIDI interface
  if ("midi_interface" in configData["DEFAULT"]) :
    if configData["DEFAULT"]["midi_interface"] in midiDevices :
      comboMidi.set(configData["DEFAULT"]["midi_interface"])
    else :
      print(f"[INFO] The last used interface is not available ({configData['DEFAULT']['midi_interface']})")
      comboMidi.set("None")

  else :
    comboMidi.set("None")



  # -----------------------------------------------------------------------------
  # [GUI DEFINITION] .mid/.pr file selection
  # -----------------------------------------------------------------------------
  fileList = getFileList(SONG_PATH, ".mid")
  if not(fileList) :
    fileList = ["None"]

  
  
  fileSelFrame = ttk.LabelFrame(root, text = "File input")
  fileSelFrame.grid(row=0, column = 1, padx = 10, pady = 5, sticky = "e")

  filterByFrame = tk.Label(fileSelFrame, text = "Filter by:")
  filterByFrame.grid(row = 0, column = 0, padx = 3, pady = 1, sticky = "w")

  fileExt = tk.StringVar()
  radioButton_mid = ttk.Radiobutton(fileSelFrame, text = ".mid file", value = ".mid", variable = fileExt, command = onRadioButtonChange)
  radioButton_pr  = ttk.Radiobutton(fileSelFrame, text = ".pr file" , value = ".pr" , variable = fileExt, command = onRadioButtonChange)
  
  radioButton_mid.grid(row = 0, column = 1, padx = 1, pady = 1, sticky = "w")
  radioButton_pr.grid(row = 0, column = 2, padx = 1, pady = 1, sticky = "e")

  # Read the last practiced song, set the .mid/.pr selection accordingly
  if "song" in configData["DEFAULT"] :
    if configData["DEFAULT"]["song"] in getFileList(SONG_PATH, ".mid") + getFileList(SONG_PATH, ".pr") :
      (_, lastFileExt) = os.path.splitext(configData["DEFAULT"]["song"])

      fileExt.set(lastFileExt)

    else :
      fileExt.set(".mid")

  else :
    fileExt.set(".mid")

  

  # -----------------------------------------------------------------------------
  # [GUI DEFINITION] Dropdown list for the file selection
  # -----------------------------------------------------------------------------
  label3 = tk.Label(fileSelFrame, text = "Select a File:")
  label3.grid(row = 2, column = 0, padx = 3, pady = 1, sticky = "w")

  comboFile = ttk.Combobox(fileSelFrame, values = [], state = "readonly")
  comboFile["width"] = 80
  comboFile.grid(row = 3, column = 0, columnspan = 3, padx = 3, pady = 5, sticky = "e")

  fileList = getFileList(SONG_PATH, fileExt.get())
  comboFile["values"] = [os.path.basename(file) for file in fileList]

  # By default, set to the last song
  if "song" in configData["DEFAULT"] :
    if configData["DEFAULT"]["song"] in getFileList(SONG_PATH, ".mid") + getFileList(SONG_PATH, ".pr") :
      comboFile.set(os.path.basename(configData["DEFAULT"]["song"]))
      
    else :
      print(f"[INFO] The last practiced song is not available ({configData['DEFAULT']['song']})")
      comboFile.set(comboFile["values"][0])

  else :
    comboFile.set(comboFile["values"][0])



  # -----------------------------------------------------------------------------
  # [GUI DEFINITION] OK button
  # -----------------------------------------------------------------------------
  buttonOK = tk.Button(root, text = "Start", command = sendConf, default = tk.ACTIVE)
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