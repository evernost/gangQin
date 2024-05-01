# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : notify
# File name     : notify.py
# Purpose       : provides audio notification utilities
# Author        : QuBi (nitrogenium@hotmail.com)
# Creation date : Sunday, 7 Apr 2024
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# External libs
# =============================================================================
# Project specific constants
from commons import *

# For wavefile play
import playsound

import random



# =============================================================================
# Constants pool
# =============================================================================
SOUND_DIR = "./resources/sounds"

WRONG_SOUND_FILES = ["Science_critical_stop.wav",
                     "Travel_program_error.wav",
                     "Travel_default_sound.wav",
                     "Travel_exclamation.wav",
                     "chord.wav",
                     "The_Golden_Era_program_error.wav"]

SUCCESS_SOUND_FILES = ["Travel_question.wav",
                       "Utopia_Asterisk.wav",
                       "Utopia_Exclamation.wav"]



# =============================================================================
# Guards
# =============================================================================
if (__name__ == "__main__") :
  print("[WARNING] This library is not intended to be called as a main.")



# =============================================================================
# Main code
# =============================================================================

class Notify :

  def __init__(self) :
    self.wrongNoteFlag = False
    self.loopPassedFlag = False

    



  # ---------------------------------------------------------------------------
  # Wrong note notification sound
  # ---------------------------------------------------------------------------
  def wrongNote(self) :

    if not(self.wrongNoteFlag) :
      
      file = random.choice(WRONG_SOUND_FILES)
      
      playsound.playsound(SOUND_DIR + "/" + file, False)
    
      # Prevent from repeated plays
      self.wrongNoteFlag = True



  # ---------------------------------------------------------------------------
  # Loop passed notification sound
  # ---------------------------------------------------------------------------
  def loopPassed(self) :

    if not(self.loopPassedFlag) :
      
      file = random.choice(SUCCESS_SOUND_FILES)
      
      playsound.playsound(SOUND_DIR + "/" + file, False)
    
      # Prevent from repeated plays
      self.loopPassedFlag = True


  # ---------------------------------------------------------------------------
  # Flag reset
  # ---------------------------------------------------------------------------
  def wrongNoteReset(self) :

    self.wrongNoteFlag = False

  def loopPassedReset(self) :
    self.loopPassedFlag = False