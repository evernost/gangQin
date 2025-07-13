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
REV_MONTH = "June"

# GUI SETTINGS (do not edit)
GUI_SCREEN_WIDTH = 1320
GUI_SCREEN_HEIGHT = 500
GUI_FPS = 60

# GUI COLOR THEME
GUI_BACKGROUND_COLOR  = (18, 67, 60)
GUI_TEXT_COLOR        = (40, 147, 131)

# Widgets ID (do not edit)
WIDGET_ID_SCORE = 0
WIDGET_ID_KEYBOARD = 1
WIDGET_ID_PIANOROLL = 2
WIDGET_ID_STAFFSCOPE = 3
WIDGET_ID_FINGERSELECTOR = 4
WIDGET_ID_ARBITER = 5
WIDGET_ID_SEQUENCER = 6
WIDGET_ID_STATS = 7
WIDGET_ID_ERROR_REPORT_GUI = 8

# KEYBOARD GEOMETRY (do not edit)
KEYBOARD_WHITE_NOTE_HEIGHT = 150
KEYBOARD_WHITE_NOTE_WIDTH = 25
KEYBOARD_BLACK_NOTE_HEIGHT = 100
KEYBOARD_BLACK_NOTE_WIDTH = 12    # Use a multiple of 6 to avoid 'un-eveness' in the display (rounding effect) 
KEYBOARD_NOTE_CHANFER = 2
KEYBOARD_NOTE_SPACING = 1

# KEYBOARD COLOR THEME
KEYBOARD_WHITE_NOTE_COLOR = (255, 255, 255)
KEYBOARD_BLACK_NOTE_COLOR = (0, 0, 0)
KEYBOARD_FINGERSATZ_FONT_COLOR_WHITE_NOTE = (240, 240, 240)
KEYBOARD_FINGERSATZ_FONT_COLOR_BLACK_NOTE = (240, 240, 240)
KEYBOARD_NOTE_COLOR_LEFT_HAND   = (255, 0, 0)
KEYBOARD_NOTE_COLOR_RIGHT_HAND  = (0, 255, 0)
KEYBOARD_PLAY_RECT_COLOR_LEFT_HAND_WHITE_NOTE = (200, 10, 0)
KEYBOARD_PLAY_RECT_COLOR_LEFT_HAND_BLACK_NOTE = (200, 10, 0)
KEYBOARD_PLAY_RECT_COLOR_RIGHT_HAND_WHITE_NOTE = (0, 200, 10)
KEYBOARD_PLAY_RECT_COLOR_RIGHT_HAND_BLACK_NOTE = (0, 200, 10)

# SCORE SETTINGS
# gangQin always deals with 2 staves max (left and right hand)
SCORE_N_STAFF = 2
SCORE_RIGHT_HAND_TRACK_ID = 0
SCORE_LEFT_HAND_TRACK_ID = 1
SCORE_ACTIVE_HANDS_LEFT  = "L "
SCORE_ACTIVE_HANDS_RIGHT = " R"
SCORE_ACTIVE_HANDS_BOTH  = "LR"

# PIANO ROLL SETTINGS (do not edit)
# Defines (roughly) the number of notes to be displayed ahead from the current cursor 
# in the piano roll
PIANOROLL_VIEW_SPAN = 10

# PIANO ROLL COLOR THEME
PIANOROLL_BACKGROUND_COLOR        = (80, 80, 80)
PIANOROLL_NOTE_LINE_SEP_COLOR     = (50, 50, 50)
PIANOROLL_NOTE_COLOR_LEFT_HAND    = (250, 165, 165)
PIANOROLL_NOTE_COLOR_RIGHT_HAND   = (165, 250, 200)
PIANOROLL_NOTE_BORDER_COLOR_LEFT  = (243, 35, 35)
PIANOROLL_NOTE_BORDER_COLOR_RIGHT = (35, 243, 118)

# MIDI CONSTANTS
MIDI_CODE_LOWEST_KEY = 21
MIDI_CODE_HIGHEST_KEY = 108
MIDI_CODE_GRAND_PIANO_RANGE = range(MIDI_CODE_LOWEST_KEY, MIDI_CODE_HIGHEST_KEY + 1)
MIDI_CODE_WHITE_NOTES_MOD12 = [0, 2, 4, 5, 7, 9, 11]
MIDI_CODE_BLACK_NOTES_MOD12 = [1, 3, 6, 8, 10]

# NOTES PROPERTIES
NOTE_WHITE_KEY = 0
NOTE_BLACK_KEY = 1
NOTE_UNDEFINED_HAND = -1
NOTE_RIGHT_HAND = SCORE_RIGHT_HAND_TRACK_ID
NOTE_LEFT_HAND = SCORE_LEFT_HAND_TRACK_ID
NOTE_UNDEFINED_FINGER = 0
NOTE_END_UNKNOWN = -1
NOTE_VOICE_DEFAULT = 0
NOTE_VOICE_1 = 1
NOTE_VOICE_2 = 2
NOTE_VOICE_3 = 3
NOTE_VOICE_4 = 4

# FINGER SELECTOR CONSTANTS
FINGERSEL_NONE_SELECTED = -1
FINGERSEL_UNCHANGED     = 0
FINGERSEL_CHANGED       = 1
FINGERSEL_HAND_CHANGE   = 3





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
SCALE_DISABLED = 0


# =============================================================================
# Unit tests
# =============================================================================
if (__name__ == "__main__") :
  print("[INFO] There are no unit tests available for 'commons.py'")


