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
import mido
import tkinter as tk
from tkinter import ttk
import os



# =============================================================================
# Guards
# =============================================================================
if (__name__ == "__main__") :
  print("[WARNING] This lib is not intended to be called as a main.")



# =============================================================================
# Main code
# =============================================================================

def getFileList(folderPath, extension) :
  fileList = []
  for filename in os.listdir(folderPath) :
    if filename.endswith(extension):
      fileList.append(os.path.join(folderPath, filename))

  return fileList




def showSetupGUI() :

  global selectedDevice
  global selectedFile
  selectedDevice = ""
  selectedFile = ""



  def sendConf() :
    global selectedDevice
    global selectedFile
    fileList = getFileList("./midi/", fileExt.get())
    selectedDevice = comboMidi.get()
    selectedFile = fileList[comboFile.current()]
    print(f"Selected MIDI Device: {selectedDevice}")
    print(f"Selected file: {selectedFile}")
    root.destroy()



  def onRadioButtonChange():
    print(fileExt.get())
    fileList = getFileList("./midi/", fileExt.get())
    print(fileList)
    if not(fileList) :
      fileList = ["None"]
      comboFile["values"] = fileList
      comboFile.set(fileList[0])
      buttonOK["state"] = "disabled"
    else :      
      fileListName = [os.path.basename(file) for file in fileList]
      comboFile["values"] = fileListName
      comboFile.set(fileListName[0])
      buttonOK["state"] = "normal"



  def centerWindow(container):
    container.update_idletasks()  # Ensure widgets are updated before calculating size
    w = container.winfo_reqwidth()
    h = container.winfo_reqheight()

    screen_width = container.winfo_screenwidth()
    screen_height = container.winfo_screenheight()

    x = (screen_width - w) // 2
    y = (screen_height - h) // 2

    container.geometry(f"{w}x{h}+{x}+{y}")



  fileList = getFileList("./midi/", ".mid")
  if not(fileList) :
    fileList = ["None"]

  # Create the main window
  root = tk.Tk()
  root.title("New learning session")
  root.resizable(0, 0)

  # -----------------------------------------------------------------------------
  # MIDI interface selection
  # -----------------------------------------------------------------------------
  lfMidi = ttk.LabelFrame(root, text = 'MIDI input')
  lfMidi.grid(row=0, column=0, padx = 10, pady = 5, sticky = "w")

  # Create a label
  label = tk.Label(lfMidi, text = "Select a MIDI device:")
  label.grid(row=0, column=0, padx = 10, pady = 1, sticky="w")

  # Dropdown list for the MIDI selection
  midiDevices = mido.get_input_names()
  midiDevices.append("None")
  comboMidi = ttk.Combobox(lfMidi, values = midiDevices, state = 'readonly')
  comboMidi.grid(row=1, column=0, padx=10, pady = 5, sticky = "w")
  comboMidi.set("None")



  # -----------------------------------------------------------------------------
  # File selection
  # -----------------------------------------------------------------------------
  lfFileSel = ttk.LabelFrame(root, text = 'File input')
  lfFileSel.grid(row=0, column=1, padx = 10, pady = 5, sticky = "e")

  label2 = tk.Label(lfFileSel, text = "Filter by:")
  label2.grid(row = 0, column = 0, padx = 3, pady = 1, sticky="w")

  fileExt = tk.StringVar()
  r1 = ttk.Radiobutton(lfFileSel, text = ".mid file", value = ".mid", variable = fileExt, command = onRadioButtonChange)
  r1.grid(row = 0, column = 1, padx = 1, pady = 1, sticky = "w")
  r2 = ttk.Radiobutton(lfFileSel, text = ".pr file", value = ".pr", variable = fileExt, command = onRadioButtonChange)
  r2.grid(row = 0, column = 2, padx = 1, pady = 1, sticky = "e")
  fileExt.set(".mid")

  label3 = tk.Label(lfFileSel, text = "Select a File:")
  label3.grid(row = 2, column = 0, padx = 3, pady = 1, sticky = "w")

  # Dropdown list for the file selection
  comboFile = ttk.Combobox(lfFileSel, values = [os.path.basename(file) for file in fileList], state = 'readonly')
  comboFile["width"] = 50
  comboFile.set(comboFile["values"][0])
  comboFile.grid(row = 3, column = 0, columnspan = 3, padx = 3, pady = 5, sticky = "e")


  buttonOK = tk.Button(root, text = "OK", command = sendConf)
  buttonOK.grid(row=1, column = 1, padx = 10, pady = 20, sticky = "e")
  buttonOK["width"] = 20
  if (len(fileList) == 1 and fileList[0] == "None") :
    buttonOK.config(state = "disabled")
  else :
    buttonOK.config(state = "normal")


  buttonQuit = tk.Button(root, text = "Quit", command = lambda: exit(0))
  buttonQuit.grid(row=1, column = 0, padx = 10, pady = 20, sticky = "w")
  buttonQuit["width"] = 10
  buttonQuit.config(state = "normal")


  # Set the select button as the "default" button
  root.bind("<Return>", lambda event = None : buttonOK.invoke())

  centerWindow(root)

  root.mainloop()
  
  return (selectedDevice, selectedFile)
