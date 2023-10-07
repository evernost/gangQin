# -*- coding: utf-8 -*-
# =============================================================================
# Module name   : keyboardUtils
# File name     : keyboardUtils.py
# Purpose       : keyboard drawing library
# Author        : QuBi (nitrogenium@hotmail.com)
# Creation date : Friday, 15 Sept 2023
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# External libs
# =============================================================================
import pygame
import mido
import fontUtils as fu
import json

# For point in polygon test
from shapely.geometry import Point, Polygon



# =============================================================================
# Constants pool
# =============================================================================
LOW_KEY_MIDI_CODE = 21
HIGH_KEY_MIDI_CODE = 108

LEFT_HAND = 0
RIGHT_HAND = 1
UNDEFINED_HAND = 2



# =============================================================================
# Guards
# =============================================================================
if (__name__ == "__main__") :
  print("[WARNING] This library is not intended to be called as a main.")



# =============================================================================
# Utilities
# =============================================================================
def noteName(midiCode) :
    
    if ((midiCode > 0) and (midiCode < 128)) :
      # List of note names
      note_names = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]

      # Calculate the octave and note index
      octave = (midiCode // 12) - 1
      note_index = midiCode % 12

      # Create the note name
      return f"{note_names[note_index]}{octave}"

    else :
      return ""



# =============================================================================
# Class: Vector2D 
# =============================================================================
class Vector2D :

  # ---------------------------------------------------------------------------
  # Constructor
  # ---------------------------------------------------------------------------
  def __init__(self, x, y) :
    self.x = x
    self.y = y



  # ---------------------------------------------------------------------------
  # Right addition: vector + listOfPoints
  # ---------------------------------------------------------------------------
  def __add__(self, other):
    self._checkOperand(other)

    # Adding a vector to a list
    if isinstance(other, list) :
      tmp = other.copy()
      if ((other[-1][0] == 0) and (other[-1][0] == 0)) :
        pass
      else :
        tmp.append((self.x + other[-1][0], self.y + other[-1][1]))
      return tmp
    
    # Adding a vector to another vector
    elif isinstance(other, Vector2D) :
      self.x += other.x
      self.y += other.y



  # ---------------------------------------------------------------------------
  # Left addition: listOfPoints + vector
  # ---------------------------------------------------------------------------
  def __radd__(self, other):
    return self.__add__(other)



  # ---------------------------------------------------------------------------
  # Define print
  # ---------------------------------------------------------------------------
  def __str__(self):
    return f"({self.x},{self.y})"



  # ---------------------------------------------------------------------------
  # Check the validity of the other operand
  # ---------------------------------------------------------------------------
  def _checkOperand(self, other) :
    
    if isinstance(other, list) :
      for i in other :
        if isinstance(i, tuple) :
          if (len(i) == 2) : 
            if all(isinstance(j, int) for j in i) :
              pass
            else :
              raise TypeError("[ERROR] Adding a vector to a list: the tuple must contain integers only.")
          else :
            raise TypeError("[ERROR] Adding a vector to a list: tuples in the list must be of length 2.")
        else :
          raise TypeError("[ERROR] Adding a vector to a list: the list must contain tuples only.")
      
    elif isinstance(other, Vector2D) :
      pass

    else :
      raise TypeError("[ERROR] A vector can only be added to a list or to another vector.")



# =============================================================================
# NOTE
# =============================================================================
class Note :

  def __init__(self, startTime, stopTime, pitch, noteIndex, hand = UNDEFINED_HAND, finger = 0) :
    self.startTime = startTime
    self.stopTime = stopTime
    self.hand = hand
    self.finger = finger
    self.pitch = pitch
    self.noteIndex = noteIndex
    
  

# =============================================================================
# KEYBOARD
# =============================================================================
class Keyboard :

  # ---------------------------------------------------------------------------
  # Constructor
  # ---------------------------------------------------------------------------
  def __init__(self, loc) :
    self.loc = loc
    self.keyboardPolygons = []
    self.activeNotes = []
    
    # Color palette
    self.whiteNoteRGB = (255, 255, 255)
    self.blackNoteRGB = (0, 0, 0)
    self.fingeringFontRGB = (240, 240, 240)

    self.sqWhiteNoteLeftRGB = (0, 200, 10)
    self.sqBlackNoteLeftRGB = (0, 200, 10)

    self.sqWhiteNoteRightRGB = (200, 10, 0)
    self.sqBlackNoteRightRGB = (200, 10, 0)

    self.sqWhiteNoteNeutralRGB = (195, 195, 195)
    self.sqBlackNoteNeutralRGB = (155, 155, 155)

    self.sqWhiteNoteOverlapLeftRGB = (140, 255, 146)
    self.sqBlackNoteOverlapLeftRGB = (140, 255, 146)

    self.sqWhiteNoteOverlapRightRGB = (255, 138, 132)
    self.sqBlackNoteOverlapRightRGB = (255, 138, 132)

    self.litKeysPolygons = []

    # Define the size of the keys
    self.a = 150; self.b = 25
    self.c = 100; self.d = 12
    self.s = 2
    self.e = 1
    
    # Fill the self.keyboardPolygons variable
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
    x0 = self.loc[0]-(12*b); y0 = self.loc[1]

    # Initialise output
    self.keyboardPolygons = [[] for _ in range(128)]

    # Generate polygons for each note
    for i in range(0,128,12) :
      
      # Note C
      if (grandPianoMode and (i == 108)) :
        self.keyboardPolygons[i] = [(x0+e, y0)]
        self.keyboardPolygons[i] += Vector2D(0,a-s)
        self.keyboardPolygons[i] += Vector2D(s,s)
        self.keyboardPolygons[i] += Vector2D(b-(2*s)-(2*e),0)
        self.keyboardPolygons[i] += Vector2D(s,-s)
        self.keyboardPolygons[i] += Vector2D(0,-(a-s))
      else :
        self.keyboardPolygons[i] = [(x0+e, y0)]
        self.keyboardPolygons[i] += Vector2D(0,a-s)
        self.keyboardPolygons[i] += Vector2D(s,s)
        self.keyboardPolygons[i] += Vector2D(b-(2*s)-(2*e),0)
        self.keyboardPolygons[i] += Vector2D(s,-s)
        self.keyboardPolygons[i] += Vector2D(0,-(a-c-e-s))
        self.keyboardPolygons[i] += Vector2D(-2*d//3,0)
        self.keyboardPolygons[i] += Vector2D(0,-(c+e))

      # Note Db
      self.keyboardPolygons[i+1] = [(x0+b-(2*d//3)+e, y0)]
      self.keyboardPolygons[i+1] += Vector2D(0,c-e)
      self.keyboardPolygons[i+1] += Vector2D(d-(2*e),0)
      self.keyboardPolygons[i+1] += Vector2D(0,-(c-e))

      # Note D
      self.keyboardPolygons[i+2] = [(x0+b+(d//3)+e, y0)]
      self.keyboardPolygons[i+2] += Vector2D(0,c+e)
      self.keyboardPolygons[i+2] += Vector2D(-d//3,0)
      self.keyboardPolygons[i+2] += Vector2D(0,a-c-e-s)
      self.keyboardPolygons[i+2] += Vector2D(s,s)
      self.keyboardPolygons[i+2] += Vector2D(b-(2*s)-(2*e),0)
      self.keyboardPolygons[i+2] += Vector2D(s,-s)
      self.keyboardPolygons[i+2] += Vector2D(0,-(a-c-e-s))
      self.keyboardPolygons[i+2] += Vector2D(-d//3,0)
      self.keyboardPolygons[i+2] += Vector2D(0,-(c+e))

      # Note Eb
      self.keyboardPolygons[i+3] = [(x0+(2*b)-(d//3)+e, y0)]
      self.keyboardPolygons[i+3] += Vector2D(0,c-e)
      self.keyboardPolygons[i+3] += Vector2D(d-(2*e),0)
      self.keyboardPolygons[i+3] += Vector2D(0,-(c-e))

      # Note Eb
      self.keyboardPolygons[i+4] = [(x0+(2*b)+(2*d//3)+e, y0)]
      self.keyboardPolygons[i+4] += Vector2D(0,c+e)
      self.keyboardPolygons[i+4] += Vector2D(-2*d//3,0)
      self.keyboardPolygons[i+4] += Vector2D(0,a-c-e-s)
      self.keyboardPolygons[i+4] += Vector2D(s,s)
      self.keyboardPolygons[i+4] += Vector2D(b-(2*s)-(2*e),0)
      self.keyboardPolygons[i+4] += Vector2D(s,-s)
      self.keyboardPolygons[i+4] += Vector2D(0,-(a-s))

      # Note F
      self.keyboardPolygons[i+5] = [(x0+(3*b)+e, y0)]
      self.keyboardPolygons[i+5] += Vector2D(0,a-s)
      self.keyboardPolygons[i+5] += Vector2D(s,s)
      self.keyboardPolygons[i+5] += Vector2D(b-(2*s)-(2*e),0)
      self.keyboardPolygons[i+5] += Vector2D(s,-s)
      self.keyboardPolygons[i+5] += Vector2D(0,-(a-c-e-s))
      self.keyboardPolygons[i+5] += Vector2D(-2*d//3,0)
      self.keyboardPolygons[i+5] += Vector2D(0,-(c+e))

      # Note Gb
      self.keyboardPolygons[i+6] = [(x0+(4*b)-(2*d//3)+e, y0)]
      self.keyboardPolygons[i+6] += Vector2D(0,c-e)
      self.keyboardPolygons[i+6] += Vector2D(d-(2*e),0)
      self.keyboardPolygons[i+6] += Vector2D(0,-(c-e))

      # Note G
      self.keyboardPolygons[i+7] = [(x0+(4*b)+(d//3)+e, y0)]
      self.keyboardPolygons[i+7] += Vector2D(0,c+e)
      self.keyboardPolygons[i+7] += Vector2D(-d//3,0)
      self.keyboardPolygons[i+7] += Vector2D(0,a-c-e-s)
      self.keyboardPolygons[i+7] += Vector2D(s,s)
      self.keyboardPolygons[i+7] += Vector2D(b-(2*s)-(2*e),0)
      self.keyboardPolygons[i+7] += Vector2D(s,-s)
      self.keyboardPolygons[i+7] += Vector2D(0,-(a-c-e-s))
      self.keyboardPolygons[i+7] += Vector2D(-d//2,0)
      self.keyboardPolygons[i+7] += Vector2D(0,-(c+e))

      if ((i+8) < 127) :

        # Note Ab
        self.keyboardPolygons[i+8] = [(x0+(5*b)-(d//2)+e, y0)]
        self.keyboardPolygons[i+8] += Vector2D(0,c-e)
        self.keyboardPolygons[i+8] += Vector2D(d-(2*e),0)
        self.keyboardPolygons[i+8] += Vector2D(0,-(c-e))

        # Note A
        if (grandPianoMode and ((i+9) == 21)) :
          self.keyboardPolygons[i+9] = [(x0+(5*b)+e, y0)]
          self.keyboardPolygons[i+9] += Vector2D(0,a-s)
          self.keyboardPolygons[i+9] += Vector2D(s,s)
          self.keyboardPolygons[i+9] += Vector2D(b-(2*s)-(2*e),0)
          self.keyboardPolygons[i+9] += Vector2D(s,-s)
          self.keyboardPolygons[i+9] += Vector2D(0,-(a-c-e-s))
          self.keyboardPolygons[i+9] += Vector2D(-d//3,0)
          self.keyboardPolygons[i+9] += Vector2D(0,-(c+e))
        else :
          self.keyboardPolygons[i+9] = [(x0+(5*b)+(d//2)+e, y0)]
          self.keyboardPolygons[i+9] += Vector2D(0,c+e)
          self.keyboardPolygons[i+9] += Vector2D(-d//2,0)
          self.keyboardPolygons[i+9] += Vector2D(0,a-c-e-s)
          self.keyboardPolygons[i+9] += Vector2D(s,s)
          self.keyboardPolygons[i+9] += Vector2D(b-(2*s)-(2*e),0)
          self.keyboardPolygons[i+9] += Vector2D(s,-s)
          self.keyboardPolygons[i+9] += Vector2D(0,-(a-c-e-s))
          self.keyboardPolygons[i+9] += Vector2D(-d//3,0)
          self.keyboardPolygons[i+9] += Vector2D(0,-(c+e))

        # Note Bb
        self.keyboardPolygons[i+10] = [(x0+(6*b)-(d//3)+e, y0)]
        self.keyboardPolygons[i+10] += Vector2D(0,c-e)
        self.keyboardPolygons[i+10] += Vector2D(d-(2*e),0)
        self.keyboardPolygons[i+10] += Vector2D(0,-(c-e))

        # Note B
        self.keyboardPolygons[i+11] = [(x0+(6*b)+(2*d//3)+e, y0)]
        self.keyboardPolygons[i+11] += Vector2D(0,c+e)
        self.keyboardPolygons[i+11] += Vector2D(-2*d//3,0)
        self.keyboardPolygons[i+11] += Vector2D(0,a-c-e-s)
        self.keyboardPolygons[i+11] += Vector2D(s,s)
        self.keyboardPolygons[i+11] += Vector2D(b-(2*s)-(2*e),0)
        self.keyboardPolygons[i+11] += Vector2D(s,-s)
        self.keyboardPolygons[i+11] += Vector2D(0,-(a-s))

      x0 += 7*b



  # ---------------------------------------------------------------------------
  # Method <drawKeys>
  # Draw the keyboard using the polygons generated for each note.
  # ---------------------------------------------------------------------------
  def drawKeys(self, screenInst) :

    # Draw keys from MIDI code 21 (A0) to MIDI code 108 (C8)
    # aka the span of a grand piano.
    for i in range(LOW_KEY_MIDI_CODE, HIGH_KEY_MIDI_CODE+1) :
      if ((i % 12) in [1,3,6,8,10]) :
        pygame.draw.polygon(screenInst, self.blackNoteRGB, self.keyboardPolygons[i])
      else :
        pygame.draw.polygon(screenInst, self.whiteNoteRGB, self.keyboardPolygons[i])



  # ---------------------------------------------------------------------------
  # Method <keyPress>
  # Highlights a note on the keyboard, eventually indicating the hand and the 
  # finger.
  # ---------------------------------------------------------------------------
  def keyPress(self, screenInst, pitch, hand = None, finger = None) :
    
    # ------------------
    # Black note drawing
    # ------------------
    if ((pitch % 12) in [1, 3, 6, 8, 10]) :
      eps = 3
      u = [x[0] for x in self.keyboardPolygons[pitch]]
      x0 = min(u); y0 = self.loc[1] + 50
      h = self.c - self.e - (2*eps) - 50
      w = self.d - (2*self.e) - (2*eps)
      sq = [(x0 + eps, y0 + eps)]
      sq += Vector2D(0, h)
      sq += Vector2D(w,0)
      sq += Vector2D(0,-h)

      # Note: function is called to plot the keypress from keyboard first. 
      # Then for the notes in MIDI file.
      # This has an impact on overlap handling
      if (hand == LEFT_HAND) :
        if (pitch in self.activeNotes) :
          pygame.draw.polygon(screenInst, self.sqBlackNoteOverlapLeftRGB, sq)
        else :
          pygame.draw.polygon(screenInst, self.sqBlackNoteLeftRGB, sq)

      if (hand == RIGHT_HAND) :
        if (pitch in self.activeNotes) :
          pygame.draw.polygon(screenInst, self.sqBlackNoteOverlapRightRGB, sq)
        else :
          pygame.draw.polygon(screenInst, self.sqBlackNoteRightRGB, sq)

      if (hand == UNDEFINED_HAND) :
        pygame.draw.polygon(screenInst, self.sqBlackNoteNeutralRGB, sq)

      # Show fingering
      if (finger in [1,2,3,4,5]) :
        fu.renderText(screenInst, str(finger), (x0+3, y0+23), 1, (240, 240, 240))
    
    # ------------------
    # White note drawing
    # ------------------
    else :
      eps = 3
      u = [x[0] for x in self.keyboardPolygons[pitch]]
      x0 = min(u); y0 = self.loc[1] + self.c + self.e
      h = self.a - (self.c + self.e) - (2*eps)
      w = self.b - (2*self.e) - (2*eps)
      sq = [(x0 + eps, y0 + eps)]
      sq += Vector2D(0, h)
      sq += Vector2D(w,0)
      sq += Vector2D(0,-h)
      
      if (hand == LEFT_HAND) :
        if (pitch in self.activeNotes) :
          pygame.draw.polygon(screenInst, self.sqWhiteNoteOverlapLeftRGB, sq)
        else :
          pygame.draw.polygon(screenInst, self.sqWhiteNoteLeftRGB, sq)
      
      if (hand == RIGHT_HAND) :
        if (pitch in self.activeNotes) :
          pygame.draw.polygon(screenInst, self.sqWhiteNoteOverlapRightRGB, sq)
        else :
          pygame.draw.polygon(screenInst, self.sqWhiteNoteRightRGB, sq)

      if (hand == UNDEFINED_HAND) :
        pygame.draw.polygon(screenInst, self.sqWhiteNoteNeutralRGB, sq)

      # Show fingering
      if (finger in [1,2,3,4,5]) :
        #fu.renderText(screenInst, str(finger), (x0+10,y0+23), 1, self.fingeringFontRGB)
        fu.renderText(screenInst, str(finger), (x0+7,y0+19), 2, self.fingeringFontRGB)

    # Register this keypress for note overlap management
    self.activeNotes.append(pitch)
    
    # Store the polygons that are lit
    if ((hand == LEFT_HAND) or (hand == RIGHT_HAND)) :
      # This makes the hitbox for click on the lit part of the key only
      #self.litKeysPolygons.append((sq, pitch))

      # This makes the hitbox for click on the entire key
      self.litKeysPolygons.append((self.keyboardPolygons[pitch], pitch))

  # ---------------------------------------------------------------------------
  # Method <reset>
  # The object keeps track of all calls to <keyPress>.
  # This function resets all notes stored.
  # Useful for the note overlapping detection.
  # ---------------------------------------------------------------------------
  def reset(self) :
    self.activeNotes = []
    self.litKeysPolygons = []



# =============================================================================
# PIANOROLL
# =============================================================================
class PianoRoll :

  # ---------------------------------------------------------------------------
  # Constructor
  # ---------------------------------------------------------------------------
  def __init__(self, x, yTop, yBottom) :
    # Drawing localisation
    self.x = x
    self.yTop = yTop
    self.yBottom = yBottom

    self.nTracks = 0
    self.noteArray = [[] for _ in range(128)]
    self.noteOnTimecodes = []
    self.noteOnTimecodesMerged = []
    self.avgNoteDuration = 0

    self.bookmarks = []
    
    self.teacherNotes = []
    self.teacherNotesPolygons = []
    self.teacherMidi = []

    # TODO: add comments to explain the meaning of this
    self.activeNoteClicked = ()

    # Color scheme
    self.keyLineRGB = (50, 50, 50)        # Color of the lines separating each notes in the piano roll
    self.noteOutlineRGB = (0, 0, 0)       # Border color for the notes in the piano roll
    self.noteLeftRGB = (165, 250, 200)    # Color of a left hand note in piano roll
    self.noteRightRGB = (250, 165, 165)   # Color of a left hand note in piano roll
    self.backgroundRGB = (143, 140, 213)  # Background color for the piano roll

    self.b = 25
    self.d = 12
    self.e = 1



  # ---------------------------------------------------------------------------
  # METHOD <importFromMIDIFile>
  #
  # Builds the piano roll (i.e. a 128-elements array) from a MIDI file.
  # 
  # Input:
  # The MIDI file to read.
  #
  # Outputs:
  # - pianoRoll.noteArray
  # - pianoRoll.noteOnTimecodes
  # - pianoRoll.avgNoteDuration
  #
  # pianoRoll.noteArray[t][p] = [note0, note1, ...]
  # is the list of all notes played on track <t>, on pitch <p>. 
  # Each element of the list is an instance of the Note() class.
  # A Note() class has attributes:
  # - noteXXX.start/.end (integer) : timestamp of its beginning/end
  # - noteXXX.hand (string: "l", "r" or ""): hand used to play the note.
  #
  # pianoRoll.noteOnTimecodes[t] = [t0, t1, ...]
  # ---------------------------------------------------------------------------
  def importFromMIDIFile(self, midiFile) :

    mid = mido.MidiFile(midiFile)

    self.nTracks = len(mid.tracks)
    print(f"Tracks found: {self.nTracks}")

    # Allocate outputs
    self.noteArray = [[[] for _ in range(128)] for _ in range(self.nTracks)]
    self.noteOnTimecodes = [[] for _ in range(self.nTracks)]

    nNotes = 0; noteDuration = 0

    # Loop on the tracks
    for (trackID, track) in enumerate(mid.tracks) :

      currTime = 0
      for msg in track :

        # Update the current date ---------------------------------------------
        currTime += msg.time
        
        # Keypress event ------------------------------------------------------
        if (msg.type == 'note_on') and (msg.velocity > 0) :
          
          # There was a note before this one. Is it done?
          if (len(self.noteArray[trackID][msg.note]) > 0) :
            for i in self.noteArray[trackID][msg.note] :
              if (i.stopTime < 0) :
                print(f"[ERROR] MIDI note {msg.note}: key is pressed again while a previous one is pending.")

            l = len(self.noteArray[trackID][msg.note])
            self.noteArray[trackID][msg.note].append(Note(currTime, -1, hand = trackID, pitch = msg.note, noteIndex = l))
            
            if not(currTime in self.noteOnTimecodes[trackID]) : 
              self.noteOnTimecodes[trackID].append(currTime)
          
          # New note
          else :
            # Its duration is unknown for now, so set its endtime to "-1"
            l = len(self.noteArray[trackID][msg.note])
            self.noteArray[trackID][msg.note].append(Note(currTime, -1, hand = trackID, pitch = msg.note, noteIndex = l))
            
            if not(currTime in self.noteOnTimecodes[trackID]) : 
              self.noteOnTimecodes[trackID].append(currTime)

        # Keyrelease event ----------------------------------------------------
        if ((msg.type == 'note_off') or ((msg.type == 'note_on') and (msg.velocity == 0))) :
          
          # Take the latest event in the piano roll for this note
          # noteObj = self.noteArray[trackID][msg.note][-1]
          
          # Close it
          self.noteArray[trackID][msg.note][-1].stopTime = currTime
          noteDuration += (self.noteArray[trackID][msg.note][-1].stopTime - self.noteArray[trackID][msg.note][-1].startTime)
          nNotes += 1.0

          # if (noteObj.startTime == noteObj.stopTime) :
          #   print(f"[WARNING] MIDI note {msg.note} ({noteName(msg.note)}): ignoring note with null duration (start time = stop time = {noteObj.startTime})")
          #   self.noteArray[msg.note].pop()

        # Others --------------------------------------------------------------
        # Other MIDI events are ignored.

    
    # Merge note ON time codes of tracks
    timecodesMerged = [item for sublist in self.noteOnTimecodes for item in sublist]
    timecodesMerged = list(set(timecodesMerged))
    self.noteOnTimecodesMerged = sorted(timecodesMerged)

    # Estimate average note duration
    self.avgNoteDuration = noteDuration/nNotes
    print(f"[NOTE] Average note duration = {self.avgNoteDuration:.2f}")



  # ---------------------------------------------------------------------------
  # Method <drawKeyLines> (private)
  # Draw the lines leading to each key
  # ---------------------------------------------------------------------------
  def _drawKeyLines(self, screenInst) :

    # Some shortcuts
    x0 = self.x
    b = self.b
    d = self.d

    self.xLines = [
      x0,                 # begin(A0)
      x0+(1*b)-(d//3),    # begin(Bb0)
      x0+(1*b)+(2*d//3),  # begin(B0)
    ]
    x0 = x0+(2*b)         # end(B0) = begin(C0)
    
    for oct in range(7) :
      self.xLines += [
        x0,
        x0+(1*b)-(2*d//3),
        x0+(1*b)+(d//3),
        x0+(2*b)-(d//3),
        x0+(2*b)+(2*d//3),
        x0+(3*b),
        x0+(4*b)-(2*d//3),
        x0+(4*b)+(d//3),
        x0+(5*b)-(d//2),
        x0+(5*b)+(d//2),
        x0+(6*b)-(d//3),
        x0+(6*b)+(2*d//3)
      ]

      x0 += 7*b

    self.xLines += [
      x0,
      x0+(1*b)
    ]

    # Draw the background rectangle
    backRect = [
      (self.xLines[0], self.yBottom),
      (self.xLines[-1], self.yBottom),
      (self.xLines[-1], self.yTop),
      (self.xLines[0], self.yTop)
    ]
    pygame.draw.polygon(screenInst, self.backgroundRGB, backRect)


    # Draw the lines
    for x in self.xLines :
      pygame.draw.line(screenInst, self.keyLineRGB, (x, self.yTop), (x, self.yBottom), 1)

    # Close the rectangle
    pygame.draw.line(screenInst, self.keyLineRGB, (self.xLines[0], self.yTop), (self.xLines[-1], self.yTop), 1)



  # ---------------------------------------------------------------------------
  # Method <drawPianoRoll>
  # Draw the piano roll
  # ---------------------------------------------------------------------------
  def drawPianoRoll(self, screenInst, startTimeCode) :
    
    self._drawKeyLines(screenInst)

    for track in range(self.nTracks) :
      for pitch in range(LOW_KEY_MIDI_CODE, HIGH_KEY_MIDI_CODE+1) :
        for note in self.noteArray[track][pitch] :
          a = startTimeCode; b = startTimeCode + (5*self.avgNoteDuration)
          c = note.startTime; d = note.stopTime
        
          # Does the note span intersect the current view window?
          if (((c >= a) and (c < b)) or ((d >= a) and (d < b)) or ((c <= a) and (d >= b))) :
            
            # Convert the size measured in "time" to a size in pixels
            rectBottom = -((self.yBottom-self.yTop)*(c-b)/(b-a)) + self.yTop
            rectTop = -((self.yBottom-self.yTop)*(d-b)/(b-a)) + self.yTop
            
            # Trim the rectangle representing the note to the current view
            rectBottom = max([rectBottom, self.yTop]); rectBottom = min([rectBottom, self.yBottom])
            rectTop = max([rectTop, self.yTop]); rectTop = min([rectTop, self.yBottom])

            sq = [(self.xLines[pitch-21]+2, rectBottom),
                  (self.xLines[pitch-21]+2, rectTop),
                  (self.xLines[pitch+1-21]-2, rectTop),
                  (self.xLines[pitch+1-21]-2, rectBottom)
                ]
            
            # Draw the note outline
            pygame.draw.line(screenInst, self.noteOutlineRGB, sq[0], sq[1], 3)
            pygame.draw.line(screenInst, self.noteOutlineRGB, sq[1], sq[2], 3)
            pygame.draw.line(screenInst, self.noteOutlineRGB, sq[2], sq[3], 3)
            pygame.draw.line(screenInst, self.noteOutlineRGB, sq[3], sq[0], 3)
            
            if (track == 0) :
              pygame.draw.polygon(screenInst, self.noteLeftRGB, sq)
            
            if (track == 1) :
              pygame.draw.polygon(screenInst, self.noteRightRGB, sq)


  # ---------------------------------------------------------------------------
  # Method <getTeacherNotes>
  # Build the list (<teacherNotes>) of current expected notes to be played at that time
  # ---------------------------------------------------------------------------
  def getTeacherNotes(self, currTime, activeHands) :
    
    self.teacherNotes = []
    self.teacherMidi = [0 for _ in range(128)]    # same information as teacherNotes but different structure
    
    # Two hands mode
    if (activeHands == "LR") :
      for pitch in range(LOW_KEY_MIDI_CODE, HIGH_KEY_MIDI_CODE+1) :
        for track in range(self.nTracks) :
          for (noteIndex, noteObj) in enumerate(self.noteArray[track][pitch]) :
            if (noteObj.startTime == self.noteOnTimecodesMerged[currTime]) :
              self.teacherNotes.append((track, pitch, noteIndex))
              self.teacherMidi[pitch] = 1

    # Left hand practice
    if (activeHands == "L ") :
      track = 0
      for pitch in range(LOW_KEY_MIDI_CODE, HIGH_KEY_MIDI_CODE+1) :
        for (noteIndex, noteObj) in enumerate(self.noteArray[track][pitch]) :
          if (noteObj.startTime == self.noteOnTimecodes[track][currTime]) :
            self.teacherNotes.append((track, pitch, noteIndex))
            self.teacherMidi[pitch] = 1

    # Right hand practice
    if (activeHands == " R") :
      track = 1
      for pitch in range(LOW_KEY_MIDI_CODE, HIGH_KEY_MIDI_CODE+1) :
        for (noteIndex, noteObj) in enumerate(self.noteArray[track][pitch]) :
          if (noteObj.startTime == self.noteOnTimecodes[track][currTime]) :
            self.teacherNotes.append((track, pitch, noteIndex))
            self.teacherMidi[pitch] = 1



  # ---------------------------------------------------------------------------
  # Method <showTeacherNotes>
  # Build the polygons to show the note and display the note
  # ---------------------------------------------------------------------------
  def showTeacherNotes(self, screen, keyboardObj) :
    
    for noteObj in self.teacherNotes :
      (track, pitch, noteIndex) = noteObj
      keyboardObj.keyPress(screen, pitch, hand = track, finger = self.noteArray[track][pitch][noteIndex].finger)



  # ---------------------------------------------------------------------------
  # METHOD <exportToPrFile>
  # Export the piano roll and all metadata (finger, hand, comments etc.) in 
  # a .pr file (JSON)
  # ---------------------------------------------------------------------------
  def exportToPrFile(self, pianoRollFile) :
    
    # Create the dictionnary containing all the things we want to save
    exportDict = {}

    # Export "manually" elements of the PianoRoll object to the export dictionary.
    # Not ideal but does the job for now as there aren't too many properties.
    exportDict["nTracks"] = self.nTracks
    exportDict["noteOnTimecodes"] = self.noteOnTimecodes
    exportDict["noteOnTimecodesMerged"] = self.noteOnTimecodesMerged
    exportDict["avgNoteDuration"] = self.avgNoteDuration
    exportDict["bookmarks"] = self.bookmarks

    # Convert the Note() objects to a dictionnary before pushing them in the export dict
    exportDict["noteArray"] = [[[noteObj.__dict__ for noteObj in noteList] for noteList in trackList] for trackList in self.noteArray]

    with open(pianoRollFile, "w") as fileHandler :
      json.dump(exportDict, fileHandler)

    print(f"[NOTE] Saved to {pianoRollFile}!")



  # ---------------------------------------------------------------------------
  # METHOD <importFromPrFile>
  # Import the piano roll and all metadata (finger, hand, comments etc.)
  # from a .pr file (JSON) and restore them in the current session.
  # ---------------------------------------------------------------------------
  def importFromPrFile(self, pianoRollFile) :
    
    with open(pianoRollFile, "r") as fileHandler :
      importDict = json.load(fileHandler)

    # Import "manually" elements of the PianoRoll object to the export dictionary.
    # Not ideal but does the job for now as there aren't too many properties.
    self.nTracks = importDict["nTracks"]
    self.noteOnTimecodes = importDict["noteOnTimecodes"]
    self.noteOnTimecodesMerged = importDict["noteOnTimecodesMerged"]
    self.avgNoteDuration = importDict["avgNoteDuration"]
    self.bookmarks = importDict["bookmarks"]

    # Convert the Note() objects to a dictionnary before pushing them in the export dict
    self.noteArray = [[[Note(**noteDict) for noteDict in noteList] for noteList in trackList] for trackList in importDict["noteArray"]]

    print(f"[NOTE] {pianoRollFile} successfully loaded!")
    


  # Based on a click coordinates, indicate whether it is a key that is lit or not
  # Return value: True or False
  # Updates the attribute <activeNoteClicked> with the info about the note
  # that has been clicked.
  def isActiveNoteClicked(self, clickX, clickY, litKeysPolygons) :

    for (sq, pitchCurr) in litKeysPolygons :
      pol = Polygon(sq)
      p = Point(clickX, clickY)

      # Intersection!
      if p.within(pol) :

        # Find the corresponding note in pianoRoll
        for (track, pitch, noteIndex) in self.teacherNotes :
          if (pitch == pitchCurr) :
            print(f"You try to edit the following note in pianoRoll:")
            print(f"- startTime = {self.noteArray[track][pitch][noteIndex].startTime}")
            print(f"- stopTime = {self.noteArray[track][pitch][noteIndex].stopTime}")
            self.activeNoteClicked = self.noteArray[track][pitch][noteIndex]
            return True

    return False
  


  def getActiveNoteClicked(self) :
    return self.activeNoteClicked
  


  def updateNoteProperties(self, note) :
    self.noteArray[note.hand][note.pitch][note.noteIndex].finger = note.finger

    