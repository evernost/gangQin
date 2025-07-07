# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : scoreShot_capture
# File name     : scoreShot_capture.py
# File type     : Python script (Python 3)
# Purpose       : application entry point for the scoreShot capturing tool
# Author        : QuBi (nitrogenium@outlook.fr)
# Creation date : Monday, 24 September 2024
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# EXTERNALS
# =============================================================================
import src.scoreShot.fileSelectionGUI as fileSelectionGUI

import captureGUI
import tkinter as tk



# =============================================================================
# CONSTANTS
# =============================================================================
# None.



# =============================================================================
# DISPLAY SHORTCUTS
# =============================================================================
print(f"================================================================================")
print(f"SCORESHOT CAPTURE - {captureGUI.CREDITS}")
print(f"================================================================================")
print("Capture window shortcuts:")
print("- Left/Right/Up/Down     : move the capture window pixel by pixel")
print("- Mouse wheel up         : move the capture window position up by 1 pixel")
print("- Mouse wheel down       : move the capture window position down by 1 pixel")
print("- Alt + Mouse wheel up   : move the capture window position left by 1 pixel")
print("- Alt + Mouse wheel down : move the capture window position right by 1 pixel")
print("- Esc                    : restore the default size of the capture window, ignore value stored in configuration file")
print("- 'c'                    : take snapshot")
print("- 'l'                    : enable/disable resizing the capture window")
print("- 'q'                    : exit app")
print("- 'r'                    : temporarily recall the last snapshot")
print("- 's'                    : save database")
print("- 't'                    : takes a test snapshot for a setup check")
print("")
print("Main window shortcuts:")
print("- Del                    : delete the selected snapshot [NOT IMPLEMENTED YET]")
print("- 'q'                    : exit app")
print("- 's'                    : save database")



# =============================================================================
# CAPTURE GUI
# =============================================================================
# Open the song file selection GUI
fileSel = fileSelectionGUI.new()
fileSel.setTitle("ScoreShot (Capture) - New session")
songFile = fileSel.show()

# Show the capture GUI
root = tk.Tk()
app = captureGUI.CaptureGUI(root)
app.loadDatabase(songFile)
app.loadGUIConfig()

root.mainloop()
