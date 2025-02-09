# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : scoreShot_capture
# File name     : scoreShot_capture.py
# Purpose       : application entry point for the scoreShot capturing tool
# Author        : QuBi (nitrogenium@outlook.fr)
# Creation date : Monday, 24 September 2024
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================



# =============================================================================
# External libs 
# =============================================================================
import src.scoreShot.fileSelectionGUI as fileSelectionGUI

import captureGUI
import tkinter as tk



# =============================================================================
# Constants pool
# =============================================================================
# Some high resolution screens use a scaling factor that messes with the 
# coordinates of 'Imagegrab'.
# Zoom factor 100%: SCREEN_SCALING = 1.0
# Zoom factor 250%: SCREEN_SCALING = 2.5
SCREEN_SCALING = 1.0



# =============================================================================
# Main code
# =============================================================================



print(f"================================================================================")
print(f"SCORESHOT CAPTURE - v0.1 (September 2024)")
print(f"================================================================================")
print("Shortcuts:")
print("- Left/Right/Up/Down     : move the capture window pixel by pixel")
print("- Mouse wheel up         : move the capture window position up by 1 pixel")
print("- Mouse wheel down       : move the capture window position down by 1 pixel")
print("- Alt + Mouse wheel up   : move the capture window position left by 1 pixel")
print("- Alt + Mouse wheel down : move the capture window position right by 1 pixel")
print("- 'Esc'                  : restore the default size of the capture window")
print("- 'l'                    : toggle the lock on the capture window resize")
print("- 'r'                    : temporarily recall the last snaphost")
print("- 's'                    : take snapshot")
print("- 'q'                    : exit app")



# Show the song file selection GUI
fileSel = fileSelectionGUI.new()
fileSel.setTitle("ScoreShot (Capture) - New session")
songFile = fileSel.show()

# Show the capture GUI
root = tk.Tk()
app = captureGUI.CaptureGUI(root)
app.loadDatabase(songFile)
app.loadGUIConfig()

root.mainloop()
