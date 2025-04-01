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
REV_MAJOR = 2
REV_MINOR = 1
REV_TYPE = "STABLE" # "ALPHA", "BETA", "STABLE"
REV_YEAR = 2025
REV_MONTH = "April"

# GUI SETTINGS (do not modify)
GUI_SCREEN_WIDTH = 1320
GUI_SCREEN_HEIGHT = 500
GUI_FPS = 60

# GUI THEME
GUI_BACKGROUND_COLOR  = (18, 67, 60)
GUI_TEXT_COLOR        = (40, 147, 131)


# Piano roll settings
# Defines (roughly) the number of notes to be displayed ahead from the current cursor 
# in the piano roll
PIANOROLL_VIEW_SPAN = 10



#               Unused       Voice 1        Voice 2        Voice 3        Voice 4
VOICE_COLOR = [(0, 0, 0), (0, 150, 200), (0, 200, 200), (200, 100, 0), (200, 200, 0)]

# GENERAL CONSTANTS
LOW_KEY_MIDI_CODE = 21
HIGH_KEY_MIDI_CODE = 108
GRAND_PIANO_MIDI_RANGE = range(LOW_KEY_MIDI_CODE, HIGH_KEY_MIDI_CODE + 1)
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

# Size of the keys (in pixels)
WHITE_NOTE_HEIGHT = 150
WHITE_NOTE_WIDTH = 25
BLACK_NOTE_HEIGHT = 100
BLACK_NOTE_WIDTH = 12
NOTE_CHANFER = 2
NOTE_SPACING = 1

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



# =============================================================================
# Unit tests
# =============================================================================
if (__name__ == "__main__") :
  print("[INFO] There are no unit tests available for 'commons.py'")


