# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : keyboard
# File name     : keyboard.py
# Purpose       : provides a grand piano widget for main app GUI
# Author        : QuBi (nitrogenium@hotmail.com)
# Creation date : Sunday, 8 Oct 2023
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# External libs
# =============================================================================
# Project specific constants
from commons import *

import pygame
import fontUtils as fu

import utils



# =============================================================================
# Constants pool
# =============================================================================




# =============================================================================
# Guards
# =============================================================================
if (__name__ == "__main__") :
  print("[WARNING] This library is not intended to be called as a main.")



# =============================================================================
# Main code
# =============================================================================

class Keyboard :

  # ---------------------------------------------------------------------------
  # Constructor
  # ---------------------------------------------------------------------------
  def __init__(self, loc) :
    (self.x, self.y) = loc
    self.activeNotes = []
    
    # -------------
    # Color palette
    # -------------
    
    # Black and white notes of the keyboard
    self.whiteNoteRGB = (255, 255, 255)
    self.blackNoteRGB = (0, 0, 0)
    
    # Rectangle indicating a note to play by left hand
    self.sqWhiteNoteLeftRGB = (0, 200, 10)
    self.sqBlackNoteLeftRGB = (0, 200, 10)

    # Rectangle indicating a note to play by right hand
    self.sqWhiteNoteRightRGB = (200, 10, 0)
    self.sqBlackNoteRightRGB = (200, 10, 0)

    # Rectangle indicating a note currently played by the MIDI input
    self.sqWhiteNoteNeutralRGB = (195, 195, 195)
    self.sqBlackNoteNeutralRGB = (155, 155, 155)

    # Rectangle of a note being played by both 
    # - a note to play by left hand
    # - the current MIDI input
    self.sqWhiteNoteOverlapLeftRGB = (140, 255, 146)
    self.sqBlackNoteOverlapLeftRGB = (140, 255, 146)

    # Rectangle of a note being played by both 
    # - a note to play by right hand
    # - the current MIDI input
    self.sqWhiteNoteOverlapRightRGB = (255, 138, 132)
    self.sqBlackNoteOverlapRightRGB = (255, 138, 132)

    # Color of the font indicating the finger
    #self.fingeringFontRGB = (240, 240, 240)
    self.fingerFontBlackNoteRGB = (240, 240, 240)

    self.litKeysPolygons = []

    # Define the size of the keys
    self.a = WHITE_NOTE_HEIGHT; self.b = WHITE_NOTE_WIDTH
    self.c = BLACK_NOTE_HEIGHT; self.d = BLACK_NOTE_WIDTH
    self.s = NOTE_CHANFER
    self.e = NOTE_SPACING
    
    # Generate polygons for all notes and store them in <keyboardPolygons>
    self.keyboardPolygons = []
    self.makeKeyboardPolygons()



  # ---------------------------------------------------------------------------
  # Method <makeKeyboardPolygons>
  # Generates the polygons depicting all the notes of a MIDI keyboard (128 notes)
  # For a grand piano, you'd use only polygons indexed from 21 (A0) to 108 (C8)
  # ---------------------------------------------------------------------------
  def makeKeyboardPolygons(self, grandPianoMode = True) :

    # Some shortcuts
    a = self.a; b = self.b
    c = self.c; d = self.d
    s = self.s
    e = self.e
    x0 = self.x - (12*b); y0 = self.y

    # Initialise output
    self.keyboardPolygons = [[] for _ in range(128)]

    # Generate polygons for each note
    for i in range(0, 128, 12) :
      
      # Note C
      if (grandPianoMode and (i == 108)) :
        self.keyboardPolygons[i] = [(x0+e, y0)]
        self.keyboardPolygons[i] += utils.Vector2D(0,a-s)
        self.keyboardPolygons[i] += utils.Vector2D(s,s)
        self.keyboardPolygons[i] += utils.Vector2D(b-(2*s)-(2*e),0)
        self.keyboardPolygons[i] += utils.Vector2D(s,-s)
        self.keyboardPolygons[i] += utils.Vector2D(0,-(a-s))
      else :
        self.keyboardPolygons[i] = [(x0+e, y0)]
        self.keyboardPolygons[i] += utils.Vector2D(0,a-s)
        self.keyboardPolygons[i] += utils.Vector2D(s,s)
        self.keyboardPolygons[i] += utils.Vector2D(b-(2*s)-(2*e),0)
        self.keyboardPolygons[i] += utils.Vector2D(s,-s)
        self.keyboardPolygons[i] += utils.Vector2D(0,-(a-c-e-s))
        self.keyboardPolygons[i] += utils.Vector2D(-2*d//3,0)
        self.keyboardPolygons[i] += utils.Vector2D(0,-(c+e))

      # Note Db
      self.keyboardPolygons[i+1] = [(x0+b-(2*d//3)+e, y0)]
      self.keyboardPolygons[i+1] += utils.Vector2D(0,c-e)
      self.keyboardPolygons[i+1] += utils.Vector2D(d-(2*e),0)
      self.keyboardPolygons[i+1] += utils.Vector2D(0,-(c-e))

      # Note D
      self.keyboardPolygons[i+2] = [(x0+b+(d//3)+e, y0)]
      self.keyboardPolygons[i+2] += utils.Vector2D(0,c+e)
      self.keyboardPolygons[i+2] += utils.Vector2D(-d//3,0)
      self.keyboardPolygons[i+2] += utils.Vector2D(0,a-c-e-s)
      self.keyboardPolygons[i+2] += utils.Vector2D(s,s)
      self.keyboardPolygons[i+2] += utils.Vector2D(b-(2*s)-(2*e),0)
      self.keyboardPolygons[i+2] += utils.Vector2D(s,-s)
      self.keyboardPolygons[i+2] += utils.Vector2D(0,-(a-c-e-s))
      self.keyboardPolygons[i+2] += utils.Vector2D(-d//3,0)
      self.keyboardPolygons[i+2] += utils.Vector2D(0,-(c+e))

      # Note Eb
      self.keyboardPolygons[i+3] = [(x0+(2*b)-(d//3)+e, y0)]
      self.keyboardPolygons[i+3] += utils.Vector2D(0,c-e)
      self.keyboardPolygons[i+3] += utils.Vector2D(d-(2*e),0)
      self.keyboardPolygons[i+3] += utils.Vector2D(0,-(c-e))

      # Note Eb
      self.keyboardPolygons[i+4] = [(x0+(2*b)+(2*d//3)+e, y0)]
      self.keyboardPolygons[i+4] += utils.Vector2D(0,c+e)
      self.keyboardPolygons[i+4] += utils.Vector2D(-2*d//3,0)
      self.keyboardPolygons[i+4] += utils.Vector2D(0,a-c-e-s)
      self.keyboardPolygons[i+4] += utils.Vector2D(s,s)
      self.keyboardPolygons[i+4] += utils.Vector2D(b-(2*s)-(2*e),0)
      self.keyboardPolygons[i+4] += utils.Vector2D(s,-s)
      self.keyboardPolygons[i+4] += utils.Vector2D(0,-(a-s))

      # Note F
      self.keyboardPolygons[i+5] = [(x0+(3*b)+e, y0)]
      self.keyboardPolygons[i+5] += utils.Vector2D(0,a-s)
      self.keyboardPolygons[i+5] += utils.Vector2D(s,s)
      self.keyboardPolygons[i+5] += utils.Vector2D(b-(2*s)-(2*e),0)
      self.keyboardPolygons[i+5] += utils.Vector2D(s,-s)
      self.keyboardPolygons[i+5] += utils.Vector2D(0,-(a-c-e-s))
      self.keyboardPolygons[i+5] += utils.Vector2D(-2*d//3,0)
      self.keyboardPolygons[i+5] += utils.Vector2D(0,-(c+e))

      # Note Gb
      self.keyboardPolygons[i+6] = [(x0+(4*b)-(2*d//3)+e, y0)]
      self.keyboardPolygons[i+6] += utils.Vector2D(0,c-e)
      self.keyboardPolygons[i+6] += utils.Vector2D(d-(2*e),0)
      self.keyboardPolygons[i+6] += utils.Vector2D(0,-(c-e))

      # Note G
      self.keyboardPolygons[i+7] = [(x0+(4*b)+(d//3)+e, y0)]
      self.keyboardPolygons[i+7] += utils.Vector2D(0,c+e)
      self.keyboardPolygons[i+7] += utils.Vector2D(-d//3,0)
      self.keyboardPolygons[i+7] += utils.Vector2D(0,a-c-e-s)
      self.keyboardPolygons[i+7] += utils.Vector2D(s,s)
      self.keyboardPolygons[i+7] += utils.Vector2D(b-(2*s)-(2*e),0)
      self.keyboardPolygons[i+7] += utils.Vector2D(s,-s)
      self.keyboardPolygons[i+7] += utils.Vector2D(0,-(a-c-e-s))
      self.keyboardPolygons[i+7] += utils.Vector2D(-d//2,0)
      self.keyboardPolygons[i+7] += utils.Vector2D(0,-(c+e))

      if ((i+8) < 127) :

        # Note Ab
        self.keyboardPolygons[i+8] = [(x0+(5*b)-(d//2)+e, y0)]
        self.keyboardPolygons[i+8] += utils.Vector2D(0,c-e)
        self.keyboardPolygons[i+8] += utils.Vector2D(d-(2*e),0)
        self.keyboardPolygons[i+8] += utils.Vector2D(0,-(c-e))

        # Note A
        if (grandPianoMode and ((i+9) == 21)) :
          self.keyboardPolygons[i+9] = [(x0+(5*b)+e, y0)]
          self.keyboardPolygons[i+9] += utils.Vector2D(0,a-s)
          self.keyboardPolygons[i+9] += utils.Vector2D(s,s)
          self.keyboardPolygons[i+9] += utils.Vector2D(b-(2*s)-(2*e),0)
          self.keyboardPolygons[i+9] += utils.Vector2D(s,-s)
          self.keyboardPolygons[i+9] += utils.Vector2D(0,-(a-c-e-s))
          self.keyboardPolygons[i+9] += utils.Vector2D(-d//3,0)
          self.keyboardPolygons[i+9] += utils.Vector2D(0,-(c+e))
        else :
          self.keyboardPolygons[i+9] = [(x0+(5*b)+(d//2)+e, y0)]
          self.keyboardPolygons[i+9] += utils.Vector2D(0,c+e)
          self.keyboardPolygons[i+9] += utils.Vector2D(-d//2,0)
          self.keyboardPolygons[i+9] += utils.Vector2D(0,a-c-e-s)
          self.keyboardPolygons[i+9] += utils.Vector2D(s,s)
          self.keyboardPolygons[i+9] += utils.Vector2D(b-(2*s)-(2*e),0)
          self.keyboardPolygons[i+9] += utils.Vector2D(s,-s)
          self.keyboardPolygons[i+9] += utils.Vector2D(0,-(a-c-e-s))
          self.keyboardPolygons[i+9] += utils.Vector2D(-d//3,0)
          self.keyboardPolygons[i+9] += utils.Vector2D(0,-(c+e))

        # Note Bb
        self.keyboardPolygons[i+10] = [(x0+(6*b)-(d//3)+e, y0)]
        self.keyboardPolygons[i+10] += utils.Vector2D(0,c-e)
        self.keyboardPolygons[i+10] += utils.Vector2D(d-(2*e),0)
        self.keyboardPolygons[i+10] += utils.Vector2D(0,-(c-e))

        # Note B
        self.keyboardPolygons[i+11] = [(x0+(6*b)+(2*d//3)+e, y0)]
        self.keyboardPolygons[i+11] += utils.Vector2D(0,c+e)
        self.keyboardPolygons[i+11] += utils.Vector2D(-2*d//3,0)
        self.keyboardPolygons[i+11] += utils.Vector2D(0,a-c-e-s)
        self.keyboardPolygons[i+11] += utils.Vector2D(s,s)
        self.keyboardPolygons[i+11] += utils.Vector2D(b-(2*s)-(2*e),0)
        self.keyboardPolygons[i+11] += utils.Vector2D(s,-s)
        self.keyboardPolygons[i+11] += utils.Vector2D(0,-(a-s))

      x0 += 7*b



  # ---------------------------------------------------------------------------
  # Method <drawKeys>
  # Draw the keyboard using the polygons generated for each note.
  # ---------------------------------------------------------------------------
  def drawKeys(self, screenInst) :

    # Draw keys from MIDI code 21 (A0) to MIDI code 108 (C8) ie notes of a grand piano.
    for i in range(LOW_KEY_MIDI_CODE, HIGH_KEY_MIDI_CODE+1) :
      if ((i % 12) in [1,3,6,8,10]) :
        pygame.draw.polygon(screenInst, self.blackNoteRGB, self.keyboardPolygons[i])
      else :
        pygame.draw.polygon(screenInst, self.whiteNoteRGB, self.keyboardPolygons[i])



  # ---------------------------------------------------------------------------
  # Method <keyPress>
  #
  # Highlight the given list of notes on the the keyboard
  # Indicate the hand to be used and the required finger if the information is 
  # available.
  # ---------------------------------------------------------------------------
  def keyPress(self, screenInst, noteList) :
    
    for noteObj in noteList :

      # -----------------------
      # White note highlighting
      # -----------------------
      if ((noteObj.pitch % 12) in [0, 2, 4, 5, 7, 9, 11]) :
        
        # Build the rectangle that will be drawn on top of the note
        eps = 3
        u = [x[0] for x in self.keyboardPolygons[noteObj.pitch]]
        x0 = min(u); y0 = self.y + self.c + self.e
        h = self.a - (self.c + self.e) - (2*eps)
        w = self.b - (2*self.e) - (2*eps)
        sq = [(x0 + eps, y0 + eps)]
        sq += utils.Vector2D(0, h)
        sq += utils.Vector2D(w,0)
        sq += utils.Vector2D(0,-h)
        
        if (noteObj.hand == LEFT_HAND) :
          if (noteObj.pitch in self.activeNotes) :
            pygame.draw.polygon(screenInst, self.sqWhiteNoteOverlapLeftRGB, sq)
          else :
            pygame.draw.polygon(screenInst, self.sqWhiteNoteLeftRGB, sq)
        
        if (noteObj.hand == RIGHT_HAND) :
          if (noteObj.pitch in self.activeNotes) :
            pygame.draw.polygon(screenInst, self.sqWhiteNoteOverlapRightRGB, sq)
          else :
            pygame.draw.polygon(screenInst, self.sqWhiteNoteRightRGB, sq)

        if (noteObj.hand == UNDEFINED_HAND) :
          pygame.draw.polygon(screenInst, self.sqWhiteNoteNeutralRGB, sq)

        # Show finger number
        if (noteObj.finger in [1,2,3,4,5]) :
          # Font size 1
          #fu.renderText(screenInst, str(finger), (x0+10,y0+23), 1, self.fingerFontWhiteNoteRGB)
          
          # Font size 2
          fu.renderText(screenInst, str(noteObj.finger), (x0+7, y0+19), 2, self.fingerFontWhiteNoteRGB)

      # Register this keypress for note overlap management
      self.activeNotes.append(noteObj.pitch)
      
      # Store the polygons that are lit
      if ((noteObj.hand == LEFT_HAND) or (noteObj.hand == RIGHT_HAND)) :
        # This makes the hitbox for click on the lit part of the key only
        #self.litKeysPolygons.append((sq, pitch))

        # This makes the hitbox for click on the entire key
        self.litKeysPolygons.append((self.keyboardPolygons[noteObj.pitch], noteObj.pitch))


      # ------------------
      # Black note drawing
      # ------------------
      if ((noteObj.pitch % 12) in [1, 3, 6, 8, 10]) :
        
        # Build the rectangle that will be drawn on top of the note
        eps = 3
        u = [x[0] for x in self.keyboardPolygons[noteObj.pitch]]
        x0 = min(u); y0 = self.y + 50
        h = self.c - self.e - (2*eps) - 50
        w = self.d - (2*self.e) - (2*eps)
        sq = [(x0 + eps, y0 + eps)]
        sq += utils.Vector2D(0, h)
        sq += utils.Vector2D(w,0)
        sq += utils.Vector2D(0,-h)

        # Note: function is called to plot the keypress from keyboard first. 
        # Then for the notes in MIDI file.
        # This has an impact on overlap handling
        if (noteObj.hand == LEFT_HAND) :
          if (noteObj.pitch in self.activeNotes) :
            pygame.draw.polygon(screenInst, self.sqBlackNoteOverlapLeftRGB, sq)
          else :
            pygame.draw.polygon(screenInst, self.sqBlackNoteLeftRGB, sq)

        if (noteObj.hand == RIGHT_HAND) :
          if (noteObj.pitch in self.activeNotes) :
            pygame.draw.polygon(screenInst, self.sqBlackNoteOverlapRightRGB, sq)
          else :
            pygame.draw.polygon(screenInst, self.sqBlackNoteRightRGB, sq)

        if (noteObj.hand == UNDEFINED_HAND) :
          pygame.draw.polygon(screenInst, self.sqBlackNoteNeutralRGB, sq)

        # Show finger number
        if (noteObj.finger in [1,2,3,4,5]) :
          # Font size 1
          fu.renderText(screenInst, str(noteObj.finger), (x0+10, y0+23), 1, self.fingerFontBlackNoteRGB)
          
          # Font size 2
          #fu.renderText(screenInst, str(finger), (x0+7, y0+19), 2, self.fingerFontBlackNoteRGB)

      



  # ---------------------------------------------------------------------------
  # Method <showScale>
  # 
  # Toggles the display of the scale
  # ---------------------------------------------------------------------------
  def showScale(self) :
    print("[NOTE] Showing the scale will be available in a future release.")








  # ---------------------------------------------------------------------------
  # Method <reset>
  #
  # The object keeps track of all calls to <keyPress>.
  # This function resets all notes stored.
  # Useful for the note overlapping detection.
  # ---------------------------------------------------------------------------
  def reset(self) :
    self.activeNotes = []
    self.litKeysPolygons = []


