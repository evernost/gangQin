# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : commons
# File name     : commons.py
# File type     : Python script (Python 3)
# Purpose       : constants used throughout the project
# Author        : QuBi (nitrogenium@outlook.fr)
# Creation date : Sunday, 8 October 2023
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# External libs
# =============================================================================
# None.



# =============================================================================
# Constants pool
# =============================================================================
# NOTE: be cautious when adding variables here, as they will be exposed 
#       everywhere else in the code without prefix ("from commons import *")

# VERSION
REV_MAJOR = 3
REV_MINOR = 0
REV_TYPE = "ALPHA" # "ALPHA", "BETA", "STABLE"
REV_YEAR = 2025
REV_MONTH = "April"

# GUI SETTINGS (do not edit)
GUI_SCREEN_WIDTH = 1320
GUI_SCREEN_HEIGHT = 500
GUI_FPS = 60

# GUI COLOR THEME
GUI_BACKGROUND_COLOR  = (18, 67, 60)
GUI_TEXT_COLOR        = (40, 147, 131)

# KEYBOARD SETTINGS (do not edit)
KEYBOARD_WHITE_NOTE_HEIGHT = 150
KEYBOARD_WHITE_NOTE_WIDTH = 25
KEYBOARD_BLACK_NOTE_HEIGHT = 100
KEYBOARD_BLACK_NOTE_WIDTH = 12    # A multiple of 6 is preferable to avoid 'un-eveness' in the display (rounding effect) 
KEYBOARD_NOTE_CHANFER = 2
KEYBOARD_NOTE_SPACING = 1

# KEYBOARD COLOR THEME
KEYBOARD_WHITE_NOTE_COLOR = (255, 255, 255)
KEYBOARD_BLACK_NOTE_COLOR = (0, 0, 0)
KEYBOARD_FINGERSATZ_FONT_COLOR_WHITE_NOTE = (240, 240, 240)
KEYBOARD_FINGERSATZ_FONT_COLOR_BLACK_NOTE = (240, 240, 240)
KEYBOARD_PLAY_RECT_COLOR_LEFT_HAND_WHITE_NOTE = (200, 10, 0)
KEYBOARD_PLAY_RECT_COLOR_LEFT_HAND_BLACK_NOTE = (200, 10, 0)
KEYBOARD_PLAY_RECT_COLOR_RIGHT_HAND_WHITE_NOTE = (0, 200, 10)
KEYBOARD_PLAY_RECT_COLOR_RIGHT_HAND_BLACK_NOTE = (0, 200, 10)

# PIANO ROLL SETTINGS (do not edit)
# Defines (roughly) the number of notes to be displayed ahead from the current cursor 
# in the piano roll
PIANOROLL_VIEW_SPAN = 10

# PIANO ROLL COLOR THEME
PIANOROLL_BACKGROUND_COLOR = (80, 80, 80)
PIANOROLL_NOTE_LINE_COLOR = (50, 50, 50)

PIANOROLL_NOTE_COLOR_LEFT_HAND = (250, 165, 165)
PIANOROLL_NOTE_COLOR_RIGHT_HAND = (165, 250, 200)




# GENERAL CONSTANTS
MIDI_CODE_LOWEST_KEY = 21
MIDI_CODE_HIGHEST_KEY = 108
GRAND_PIANO_MIDI_RANGE = range(MIDI_CODE_LOWEST_KEY, MIDI_CODE_HIGHEST_KEY + 1)
WHITE_NOTES_CODE_MOD12 = [0, 2, 4, 5, 7, 9, 11]
BLACK_NOTES_CODE_MOD12 = [1, 3, 6, 8, 10]

# NOTES PROPERTIES
WHITE_KEY = 0
BLACK_KEY = 1
UNDEFINED_HAND = -1
RIGHT_HAND = 0
LEFT_HAND = 1
UNDEFINED_FINGER = 0
NOTE_END_UNKNOWN = -1

VOICE_DEFAULT = 0
VOICE_1 = 1
VOICE_2 = 2
VOICE_3 = 3
VOICE_4 = 4

SCALE_DISABLED = 0

ACTIVE_HANDS_BOTH  = "LR"
ACTIVE_HANDS_LEFT  = "L "
ACTIVE_HANDS_RIGHT = " R"

WIDGET_LOC_UNDEFINED = (-1, -1)

# Pygame click codes
MOUSE_LEFT_CLICK = 1
MOUSE_RIGHT_CLICK = 3
MOUSE_SCROLL_UP = 4
MOUSE_SCROLL_DOWN = 5



# Path of the songs (.pr and .mid)
SONG_PATH = "./songs"

# Backup feature (autosave)
AUTOSAVE_INTERVAL_SEC = 90
AUTOSAVE_BACKUP_PATH = "./backup"

# Define if the staffscope is displayed by default at startup
STAFFSCOPE_DEFAULT_VISIBILITY = True


# *** BELOW IS DEPRECATED OR WILL BE IN A FUTURE RELEASE ***
#               Unused       Voice 1        Voice 2        Voice 3        Voice 4
VOICE_COLOR = [(0, 0, 0), (0, 150, 200), (0, 200, 200), (200, 100, 0), (200, 200, 0)]



# =============================================================================
# Unit tests
# =============================================================================
if (__name__ == "__main__") :
  print("[INFO] There are no unit tests available for 'commons.py'")


