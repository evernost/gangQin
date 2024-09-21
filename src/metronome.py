# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : metronome
# File name     : metronome.py
# Purpose       : metronome object
# Author        : QuBi (nitrogenium@hotmail.com)
# Creation date : Saturday, 31th August, 2024
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# External libs
# =============================================================================
# Project specific constants
from commons import *

import numpy as np
import pygame



# =============================================================================
# Constants pool
# =============================================================================
MSG_TEMPO_UPDATE = 1
MSG_TIMER_ON = 2
MSG_TIMER_OFF = 3



# =============================================================================
# Unit tests
# =============================================================================
if (__name__ == "__main__") :
  print("[INFO] There are no unit tests available for 'metronome.py'")



class Metronome :
  """
  todo!


  """
  def __init__(self, bpm = 120, num = 4, denom = 4) :
    self.enable = False
        
    self.bpm = bpm
    self.num = num      # Number of beats per measure
    self.denom = denom  # 1 = whole note, 2 = half note, 4 = quarter note, 8 = eighth note etc.

    self.counter = 1

    self._optionMode = False
    self._switched = False

    self.tickDuration = 0.2
    self.tickVolume = 0.3
    
    self.msgQueue = []

    # Prepare the samples array that make the 'tic' sound of the metronome
    t = np.linspace(0, self.tickDuration, int(44100 * self.tickDuration), endpoint = False)
    tickHigh = np.int16(32767 * self.tickVolume * np.sin(2 * np.pi * 880.0 * t) * np.exp(-t/(self.tickDuration/3)))
    tickLow = np.int16(32767 * self.tickVolume * np.sin(2 * np.pi * 440.0 * t) * np.exp(-t/(self.tickDuration/3)))
    tickHigh = tickHigh.tobytes()
    tickLow = tickLow.tobytes()
    self.tickHighSound = pygame.mixer.Sound(buffer = tickHigh)
    self.tickLowSound = pygame.mixer.Sound(buffer = tickLow)



  # ---------------------------------------------------------------------------
  # METHOD Metronome.getInterval_ms()
  # ---------------------------------------------------------------------------
  def getInterval_ms(self) :
    """
    Returns the value the interval (in ms) between 2 clicks of the metronome.
    """
    
    return (1000*60//self.bpm)
  


  # ---------------------------------------------------------------------------
  # METHOD Metronome.keyPress(pygameKeys)
  # ---------------------------------------------------------------------------
  def keyPress(self, pygameKeys) :
    """
    Updates the metronome object status (ON, OFF, increase tempo, etc.) 
    based on the keys that have been pressed.

    TODO: 'm' and '↑' increase the number of beats per bar.
    """

    if pygameKeys[pygame.K_m] :

      if not(self.enable) :
        self.enable = True
        self._switched = True
        self.msgQueue.append(MSG_TIMER_ON)

      if pygameKeys[pygame.K_KP_PLUS] :
        self._optionMode = True
        self.bpm += 1
        if not(MSG_TEMPO_UPDATE in self.msgQueue) :
          self.msgQueue.append(MSG_TEMPO_UPDATE)
      
      elif pygameKeys[pygame.K_KP_MINUS] :
        self._optionMode = True
        self.bpm -= 1
        if not(MSG_TEMPO_UPDATE in self.msgQueue) :
          self.msgQueue.append(MSG_TEMPO_UPDATE)

    else :
      self.switched = False
      self._optionMode = False


      
  # ---------------------------------------------------------------------------
  # METHOD Metronome.keyRelease(pygameKeys)
  # ---------------------------------------------------------------------------
  def keyRelease(self, key) :
    """
    Updates the metronome object status (ON, OFF, increase tempo, etc.) 
    based on the keys that have been released.
    """

    if (key == pygame.K_m) :

      if self._switched :
        self._switched = False

      else : 
        if self._optionMode :
          self._optionMode = False
        else :
          self.enable = False
          self.counter = 1
          self.msgQueue.append(MSG_TIMER_OFF)
        


  # ---------------------------------------------------------------------------
  # METHOD Metronome.playTick()
  # ---------------------------------------------------------------------------
  def playTick(self) :
    """
    Plays the metronome 'tic' sound.
    """

    if self.enable :

      if (self.counter == self.num) :
        self.tickHighSound.play()
        self.counter = 1

      else :
        self.tickLowSound.play()
        self.counter += 1



  # ---------------------------------------------------------------------------
  # METHOD Metronome.getMsg()
  # ---------------------------------------------------------------------------
  def clearQueue(self) :
    self.msgQueue = []


