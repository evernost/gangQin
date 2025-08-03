# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : fileSelectionGUI
# File name     : fileSelectionGUI.py
# Purpose       : shows the song and MIDI input selection GUI for gangQin
# Author        : QuBi (nitrogenium@hotmail.com)
# Creation date : Sunday, 24 Sept 2023
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# EXTERNALS
# =============================================================================
# Project libraries
from src.commons import *

# Standard libraries
import configparser     # For .ini files
import mido             # For read/write in MIDI files
import os               # For paths
import tkinter as tk    # For GUI
from tkinter import ttk



# =============================================================================
# CONSTANTS
# =============================================================================
# None.



# =============================================================================
# CLASS DEFINITION
# =============================================================================
class FileSelectionGUI :

  """
  FILE_SELECTION_GUI object

  Self-contained class containing all the necessary functions to show the 
  song and MIDI keyboard interface selector.

  Call the app, it will return a dictionary the information upon exiting.

  See the unit tests for a quick demo.
  """

  def __init__(self) :
    
    # Populated after calling 'FileSelectGUI._configLoad()'
    self.config = None
    self.configFile = "./conf/conf.ini"

    # Populated after calling 'FileSelectGUI._listMidiDevices()'
    self.midiDevices = []
    
    # Populated after calling 'FileSelectGUI._listSongFiles()'
    self.midiFiles  = []
    self.gqFiles    = []
    
    # Populated after clicking on 'Start'
    self.selectedDevice = ""
    self.selectedFile = ""

    self._configLoad()
    self._listMidiDevices()
    self._listSongFiles()

    # Initialise display
    self.root = None
    


  # ---------------------------------------------------------------------------
  # METHOD FileSelectGUI.run()
  # ---------------------------------------------------------------------------
  def run(self) :
    """
    Shows the GUI, loops until the user validates the configuration.

    The function returns the full name of the song (path included) and 
    the name of the MIDI keyboard interface upon exiting.
    """

    # Configure the main window
    self.root = tk.Tk()
    self.root.title("New learning session")
    self.root.resizable(0, 0)

    # GUI definition
    self.guiFrameMidiInput = ttk.LabelFrame(self.root, text = "MIDI input")
    self.guiFrameMidiInput.grid(row = 0, column = 0, padx = 10, pady = 5, sticky = "w")

    self.guiLabelSelectDevice = tk.Label(self.guiFrameMidiInput, text = "Select the input device:")
    self.guiLabelSelectDevice.grid(row = 0, column = 0, padx = 10, pady = 1, sticky = "w")

    self.guiComboMIDI = ttk.Combobox(self.guiFrameMidiInput, values = self.midiDevices, state = "readonly")
    self.guiComboMIDI.grid(row = 1, column = 0, padx = 10, pady = 5, sticky = "w")
    self._setToLastMidiInterface(self.guiComboMIDI)

    self.guiFrameFileSel = ttk.LabelFrame(self.root, text = "File input")
    self.guiFrameFileSel.grid(row = 0, column = 1, padx = 10, pady = 5, sticky = "e")

    self.guiLabelFilterBy = tk.Label(self.guiFrameFileSel, text = "Filter by:")
    self.guiLabelFilterBy.grid(row = 0, column = 0, padx = 3, pady = 1, sticky = "w")

    self.guiFileExtChoice = tk.StringVar()
    self.guiRadioButtonMIDI = ttk.Radiobutton(self.guiFrameFileSel, text = ".mid file", value = ".mid", variable = self.guiFileExtChoice, command = self.CLBK_onFileTypeChange)
    self.guiRadioButtonMIDI.grid(row = 0, column = 1, padx = 1, pady = 1, sticky = "w")
    self.guiRadioButtonGQ = ttk.Radiobutton(self.guiFrameFileSel, text = ".pr file [SOON: .gq3]" , value = ".pr" , variable = self.guiFileExtChoice, command = self.CLBK_onFileTypeChange)
    self.guiRadioButtonGQ.grid(row = 0, column = 2, padx = 1, pady = 1, sticky = "e")
    self._setToLastFileExt(self.guiFileExtChoice)

    self.guiLabelSelectFile = tk.Label(self.guiFrameFileSel, text = "Select a File:")
    self.guiLabelSelectFile.grid(row = 2, column = 0, padx = 3, pady = 1, sticky = "w")

    self.guiComboFile = ttk.Combobox(self.guiFrameFileSel, values = [], state = "readonly")
    self.guiComboFile["width"] = 80
    self.guiComboFile.grid(row = 3, column = 0, columnspan = 3, padx = 3, pady = 5, sticky = "e")
    self._populateSongs(self.guiComboFile)
    self._setToLastSong(self.guiComboFile)

    self.guiButtonStart = tk.Button(self.root, text = "Start", command = self.CLBK_onStart, default = tk.ACTIVE)
    self.guiButtonStart.grid(row = 1, column = 1, padx = 10, pady = 20, sticky = "e")
    self.guiButtonStart["width"] = 20
    self._setButtonStartStatus()

    buttonQuit = tk.Button(self.root, text = "Quit", command = lambda: exit(0))
    buttonQuit.grid(row = 1, column = 0, padx = 10, pady = 20, sticky = "w")
    buttonQuit["width"] = 10
    buttonQuit.config(state = "normal")

    # Make the 'start' button default
    self.root.bind("<Return>", lambda event = None : self.guiButtonStart.invoke())

    # Code executed upon exit
    self.root.protocol("WM_DELETE_WINDOW", self.CLBK_onQuit)
    
    # Main loop
    self._centerWindow()
    self.root.mainloop()
  
    # Export this configuration to a .ini file
    #self._readSelection()
    #self._configSave()

    # Return the selection (MIDI interface + file) to the main  
    return (self.selectedDevice, self.selectedFile)



  # ---------------------------------------------------------------------------
  # METHOD FileSelectGUI._readSelection()
  # ---------------------------------------------------------------------------
  def _readSelection(self) :
    """
    Returns a descriptor (dictionary) with the selected song and the selected
    input MIDI interface.
    """
  
    # Read the file
    comboIndex = self.guiComboFile.current()
    if (self.guiFileExtChoice.get() == ".mid") : 
      self.selectedFile = self.midiFiles[comboIndex]
    else :
      self.selectedFile = self.gqFiles[comboIndex]

    # Read the device
    self.selectedDevice = self.guiComboMIDI.get()



  # ---------------------------------------------------------------------------
  # METHOD FileSelectGUI._listMidiDevices()                           [PRIVATE]
  # ---------------------------------------------------------------------------
  def _listMidiDevices(self) :
    """
    Lists all the MIDI keyboards detected on the computer.
    Devices are listed with their string descriptor.

    The list always contains the element "None" for the 'navigation mode' 
    i.e. gangQin without external keyboard.
    """

    self.midiDevices = mido.get_input_names()
    self.midiDevices.append("None")



  # ---------------------------------------------------------------------------
  # METHOD FileSelectGUI._listSongFiles()                             [PRIVATE]
  # ---------------------------------------------------------------------------
  def _listSongFiles(self) :
    """
    Description is TODO.
    """

    self.midiFiles = self._listFilesWithExt(SONG_PATH, ".mid")
    if not(self.midiFiles) :
      self.midiFiles = ["None"]

    self.gqFiles = self._listFilesWithExt(SONG_PATH, ".pr")
    if not(self.gqFiles) :
      self.gqFiles = ["None"]



  # ---------------------------------------------------------------------------
  # METHOD FileSelectGUI._listFilesWithExt()                          [PRIVATE]
  # ---------------------------------------------------------------------------
  def _listFilesWithExt(self, folderPath, extension) :
    """
    Returns a sorted list of all files of a given extension in a specific
    directory.

    This is the place you might want to edit the sorting method in case you
    want a specific order in the list instead of alphabetical sort.
    """

    fileList = []
    for filename in os.listdir(folderPath) :
      if filename.endswith(extension) :
        fileList.append(folderPath + '/' + filename)

    fileList.sort()
    return fileList



  # ---------------------------------------------------------------------------
  # METHOD FileSelectGUI._configLoad()                                [PRIVATE]
  # ---------------------------------------------------------------------------
  def _configLoad(self) :
    """
    Tries to load a configuration file.
    """
    
    self.config = configparser.ConfigParser()
    if os.path.exists(self.configFile) :
      self.config.read(self.configFile)
    else :
      print("[INFO] No last configuration found: loading defaults.")



  # ---------------------------------------------------------------------------
  # METHOD FileSelectGUI._configSave()                                [PRIVATE]
  # ---------------------------------------------------------------------------
  def _configSave(self) :
    """
    Exports the current configuration to a .ini file.
    """

    print("exporting conf...")
    print(f"- midi_interface: {self.selectedDevice}")
    print(f"- song          : {self.selectedFile}")

    self.config["DEFAULT"] = {
      "midi_interface": self.selectedDevice,
      "song"          : self.selectedFile
    }

    # Create the './conf' dir if it does not exist
    if not os.path.exists("./conf"):
      os.makedirs("./conf")

    with open(self.configFile, "w") as configfile :
      self.config.write(configfile)



  # ---------------------------------------------------------------------------
  # METHOD FileSelectGUI._populateSongs()                             [PRIVATE]
  # ---------------------------------------------------------------------------
  def _populateSongs(self, comboBox) :
    """
    Populates the listed songs in the combo box.
    """

    if (self.guiFileExtChoice.get() == ".mid"): 
      comboBox["values"] = [os.path.basename(file) for file in self.midiFiles]
    elif (self.guiFileExtChoice.get() == ".pr") : 
      comboBox["values"] = [os.path.basename(file) for file in self.gqFiles]
    else :
      pass



  # ---------------------------------------------------------------------------
  # METHOD FileSelectGUI._setToLastMidiInterface()                    [PRIVATE]
  # ---------------------------------------------------------------------------
  def _setToLastMidiInterface(self, comboBox) :
    """
    Sets the MIDI interface combo box to the last known configuration.
    """

    if ("midi_interface" in self.config["DEFAULT"]) :
      if self.config["DEFAULT"]["midi_interface"] in self.midiDevices :
        comboBox.set(self.config["DEFAULT"]["midi_interface"])
      else :
        print(f"[INFO] The last used interface is not available ({self.config["DEFAULT"]["midi_interface"]})")
        comboBox.set("None")

    else :
      comboBox.set("None")



  # ---------------------------------------------------------------------------
  # METHOD FileSelectGUI._setToLastSong()                             [PRIVATE]
  # ---------------------------------------------------------------------------
  def _setToLastSong(self, comboBox) :
    """
    Sets the file selection combo box to the last song practiced.
    """

    if ("song" in self.config["DEFAULT"]) :
      if self.config["DEFAULT"]["song"] in (self.midiFiles + self.gqFiles) :
        comboBox.set(os.path.basename(self.config["DEFAULT"]["song"]))
      else :
        print(f"[INFO] The last practiced song is not available ({self.config["DEFAULT"]["song"]})")
        comboBox.set(comboBox["values"][0])
    else :
      comboBox.set(comboBox["values"][0])



  # ---------------------------------------------------------------------------
  # METHOD FileSelectGUI._setToLastFileExt()                          [PRIVATE]
  # ---------------------------------------------------------------------------
  def _setToLastFileExt(self, choice) -> None :
    """
    Sets the extension selector to the last type of song practiced.
    """
    
    # Read the last practiced song, set the .mid/.gq selection accordingly
    if ("song" in self.config["DEFAULT"]) :
      if self.config["DEFAULT"]["song"] in (self.midiFiles + self.gqFiles) :
        (_, lastFileExt) = os.path.splitext(self.config["DEFAULT"]["song"])
        choice.set(lastFileExt)
      else :
        choice.set(".mid")
    else :
      choice.set(".mid")



  # ---------------------------------------------------------------------------
  # METHOD FileSelectGUI._setButtonStartStatus()                      [PRIVATE]
  # ---------------------------------------------------------------------------
  def _setButtonStartStatus(self) -> None :
    """
    Description is TODO.
    """

    if (len(self.guiComboFile["values"]) == 1 and self.guiComboFile["values"][0] == "None") :
      self.guiButtonStart.config(state = "disabled")
    else :
      self.guiButtonStart.config(state = "normal")



  # ---------------------------------------------------------------------------
  # METHOD FileSelectGUI._centerWindow()                              [PRIVATE]
  # ---------------------------------------------------------------------------
  def _centerWindow(self) :
    """
    Centers the window on screen.
    """
    
    # Ensure widgets are updated before calculating size
    self.root.update_idletasks()
    
    w = self.root.winfo_reqwidth()
    h = self.root.winfo_reqheight()

    screenWidth = self.root.winfo_screenwidth()
    screenHeight = self.root.winfo_screenheight()

    x = (screenWidth - w) // 2
    y = (screenHeight - h) // 2

    self.root.geometry(f"{w}x{h}+{x}+{y}")



  # ---------------------------------------------------------------------------
  # METHOD FileSelectGUI.CLBK_onFileTypeChange()
  # ---------------------------------------------------------------------------
  def CLBK_onFileTypeChange(self, event = None) :
    """
    CALLBACK function
    This function is called every time the file type .gq/.mid selector is 
    changed.
    """
    
    if (self.guiFileExtChoice.get() == ".mid") : 
      fileList = [os.path.basename(file) for file in self.midiFiles]
    elif (self.guiFileExtChoice.get() == ".pr") : 
      fileList = [os.path.basename(file) for file in self.gqFiles]
    else :
      pass
    
    # No file found
    if not(fileList) :
      fileList = ["None"]
      self.guiComboFile["values"] = fileList
      self.guiComboFile.set(fileList[0])    
    else :      
      self.guiComboFile["values"] = fileList
      self.guiComboFile.set(fileList[0])
        
    # Update the OK button status to enabled/disabled based on 
    # the new selection
    self._setButtonStartStatus()



  # ---------------------------------------------------------------------------
  # METHOD FileSelectGUI.CLBK_onFileTypeChange()
  # ---------------------------------------------------------------------------
  def CLBK_onStart(self) :
    """
    CALLBACK function
    This function is called when the user selection is done and committed.
    """

    self._readSelection()
    self._configSave()
    self.root.destroy()



  # ---------------------------------------------------------------------------
  # METHOD FileSelectGUI.CLBK_onQuit()
  # ---------------------------------------------------------------------------
  def CLBK_onQuit(self) :
    """
    CALLBACK function
    This function is called when the user prematurely exits the app.
    """
    
    self._readSelection()
    self._configSave()
    print("[INFO] User exit...")
    exit()



# =============================================================================
# UTILITIES
# =============================================================================

# Factory function
def new() :
  return FileSelectionGUI()



# =============================================================================
# UNIT TESTS
# =============================================================================
if (__name__ == "__main__") :
  
  print("[INFO] Library 'FileSelectGUI' called as main: running unit tests...")
  
  gui = new()
  (midiDevice, songFile) = gui.run()

  print(f"- selected MIDI interface : {midiDevice}")
  print(f"- selected song           : {songFile}")
  