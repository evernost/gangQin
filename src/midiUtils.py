# -*- coding: utf-8 -*-
# =============================================================================
# Module name   : midiUtils
# File name     : midiUtils.py
# Purpose       : 
# Author        : Quentin Biache
# Creation date : Sunday, September 24th
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# External libs
# =============================================================================
import mido
import tkinter as tk
from tkinter import ttk



def midiInterfaceGUI() :

  global selectedDevice
  selectedDevice = ""

  def selectMidiDevice() :
    global selectedDevice
    selectedDevice = deviceCombo.get()
    print(f"Selected MIDI Device: {selectedDevice}")
    root.destroy()
  
  # Create the main window
  root = tk.Tk()
  root.title("MIDI Device Selector")

  # Get the screen width and height
  screen_width = root.winfo_screenwidth()
  screen_height = root.winfo_screenheight()

  # Calculate the window's position to center it on the screen
  window_width = 300
  window_height = 150
  x = (screen_width - window_width) // 2
  y = (screen_height - window_height) // 2
  root.geometry(f"{window_width}x{window_height}+{x}+{y}")

  # Get the list of MIDI devices
  midiDevices = mido.get_input_names()

  # Create a label
  label = tk.Label(root, text = "Select a MIDI device:")
  label.pack(pady = 10)

  # Create a dropdown list
  deviceCombo = ttk.Combobox(root, values = midiDevices)
  deviceCombo.pack(pady = 5)

  # Create a button to select the device
  select_button = tk.Button(root, text = "Select", command = selectMidiDevice)
  select_button.pack(pady=10)

  root.mainloop()
  
  return selectedDevice
  