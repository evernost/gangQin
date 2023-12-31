# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : commons
# File name     : commons.py
# Purpose       : constants used throughout the project
# Author        : QuBi (nitrogenium@hotmail.com)
# Creation date : Sunday, 8 Oct 2023
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

VOICE_DEFAULT = 0
VOICE_1 = 1
VOICE_2 = 2
VOICE_3 = 3
VOICE_4 = 4

ACTIVE_HANDS_BOTH  = "LR"
ACTIVE_HANDS_LEFT  = "L "
ACTIVE_HANDS_RIGHT = " R"

REV_MAJOR = 0
REV_MINOR = 9
REV_YEAR = 2023
REV_MONTH = "Nov"

# Size of the keys (in pixels)
WHITE_NOTE_HEIGHT = 150
WHITE_NOTE_WIDTH = 25
BLACK_NOTE_HEIGHT = 100
BLACK_NOTE_WIDTH = 12
NOTE_CHANFER = 2
NOTE_SPACING = 1

# Piano roll settings
PIANOROLL_VIEW_SPAN = 5

# Pygame click codes
MOUSE_LEFT_CLICK = 1
MOUSE_SCROLL_UP = 4
MOUSE_SCROLL_DOWN = 5

# Theme 
BACKGROUND_COLOR = (50, 50, 80)
UI_TEXT_COLOR = (200, 200, 250)

#               Unused       Voice 1        Voice 2        Voice 3        Voice 4
VOICE_COLOR = [(0, 0, 0), (0, 150, 200), (0, 200, 200), (200, 100, 0), (200, 200, 0)]

# =============================================================================
# Guards
# =============================================================================
if (__name__ == "__main__") :
  print("[WARNING] This library is not intended to be called as a main.")


