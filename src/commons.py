# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : commons
# File name     : commons.py
# Purpose       : constants used throughout the project
# Author        : QuBi (nitrogenium@hotmail.com)
# Creation date : Sunday, 8 October 2023
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# External libs
# =============================================================================




# =============================================================================
# Constants pool
# =============================================================================
# Note: be cautious when adding variables here, as they will be exposed 
#       everywhere else in the code without prefix ("from commons import *")



# ----------------------
# Customizable variables
# ----------------------
REV_MAJOR = 2
REV_MINOR = 0
REV_TYPE = "BETA" # "ALPHA", "BETA", "STABLE"
REV_YEAR = 2025
REV_MONTH = "February"

# Piano roll settings
# Defines (roughly) the number of notes to be displayed ahead from the current cursor 
# in the piano roll
PIANOROLL_VIEW_SPAN = 10

# Theme 
BACKGROUND_COLOR = (30, 70, 130)
UI_TEXT_COLOR    = (129, 172, 226)

#               Unused       Voice 1        Voice 2        Voice 3        Voice 4
VOICE_COLOR = [(0, 0, 0), (0, 150, 200), (0, 200, 200), (200, 100, 0), (200, 200, 0)]

# ---------------
# Deeper settings
# ---------------
# These variables are linked to the app core. 
# They should NOT be modified, unless you know what you are doing.
LOW_KEY_MIDI_CODE = 21
HIGH_KEY_MIDI_CODE = 108
GRAND_PIANO_MIDI_RANGE = range(LOW_KEY_MIDI_CODE, HIGH_KEY_MIDI_CODE + 1)

WHITE_NOTES_CODE_MOD12 = [0, 2, 4, 5, 7, 9, 11]
BLACK_NOTES_CODE_MOD12 = [1, 3, 6, 8, 10]
WHITE_KEY = 0
BLACK_KEY = 1

UNDEFINED_HAND = -1
RIGHT_HAND = 0
LEFT_HAND = 1

UNDEFINED_FINGER = 0

NOTE_END_UNKNOWN = -1

SCALE_DISABLED = 0

VOICE_DEFAULT = 0
VOICE_1 = 1
VOICE_2 = 2
VOICE_3 = 3
VOICE_4 = 4

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

FPS = 60

# Path of the songs (.pr and .mid)
SONG_PATH = "./songs"

# Backup feature (autosave)
AUTOSAVE_INTERVAL_SEC = 90
AUTOSAVE_BACKUP_PATH = "./backup"





# =============================================================================
# Guards
# =============================================================================
if (__name__ == "__main__") :
  print("[WARNING] This library is not intended to be called as a main.")


