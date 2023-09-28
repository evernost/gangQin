# -*- coding: utf-8 -*-
# =============================================================================
# Module name   : keyboardUtils
# File name     : keyboardUtils.py
# Purpose       : keyboard drawing library
# Author        : Quentin Biache
# Creation date : Friday, September 15th
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# External libs
# =============================================================================
import pygame
import mido
import fontUtils as fu



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
# Class: Note
# =============================================================================
class Note :

  def __init__(self, startTime, stopTime, hand = "", finger = 0) :
    self.startTime = startTime
    self.stopTime = stopTime
    self.hand = hand
    self.finger = finger
    


# =============================================================================
# Class: keyboard 
# =============================================================================
class Keyboard :

  # ---------------------------------------------------------------------------
  # Constructor
  # ---------------------------------------------------------------------------
  def __init__(self, loc) :
    self.loc = loc
    self.keyboardPolygons = []
    
    # Color scheme
    self.whiteNoteRGB = (255, 255, 255)
    self.blackNoteRGB = (0, 0, 0)

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
    for i in range(21, 108+1) :
    
      if ((i % 12) in [1,3,6,8,10]) :
        pygame.draw.polygon(screenInst, self.blackNoteRGB, self.keyboardPolygons[i])
      else :
        pygame.draw.polygon(screenInst, self.whiteNoteRGB, self.keyboardPolygons[i])



  # ---------------------------------------------------------------------------
  # Method <keyPress>
  # Highlights a note on the keyboard, eventually indicating the hand and the 
  # finger.
  # ---------------------------------------------------------------------------
  def keyPress(self, screenInst, note, hand = None, finger = None) :
    
    sqWhiteNoteLeftRGB = (200, 10, 0)
    sqBlackNoteLeftRGB = (200, 10, 0)

    sqWhiteNoteRightRGB = (0, 200, 10)
    sqBlackNoteRightRGB = (0, 200, 10)

    sqWhiteNoteNeutralRGB = (0, 10, 200)
    sqBlackNoteNeutralRGB = (0, 10, 200)

    alpha = 0.7
    sqWhiteNoteNeutralRGBAlpha = (
      alpha*(self.whiteNoteRGB[0]-sqWhiteNoteNeutralRGB[0]) + sqWhiteNoteNeutralRGB[0],
      alpha*(self.whiteNoteRGB[1]-sqWhiteNoteNeutralRGB[1]) + sqWhiteNoteNeutralRGB[1],
      alpha*(self.whiteNoteRGB[2]-sqWhiteNoteNeutralRGB[2]) + sqWhiteNoteNeutralRGB[2]
    )
    alpha = 0.1
    sqBlackNoteNeutralRGBAlpha = (
      alpha*(self.blackNoteRGB[0]-sqBlackNoteNeutralRGB[0]) + sqBlackNoteNeutralRGB[0],
      alpha*(self.blackNoteRGB[1]-sqBlackNoteNeutralRGB[1]) + sqBlackNoteNeutralRGB[1],
      alpha*(self.blackNoteRGB[2]-sqBlackNoteNeutralRGB[2]) + sqBlackNoteNeutralRGB[2]
    )
                                  

    # Black note drawing
    if ((note % 12) in [1,3,6,8,10]) :
      eps = 3
      u = [x[0] for x in self.keyboardPolygons[note]]
      x0 = min(u); y0 = self.loc[1] + 50
      h = self.c - self.e - (2*eps) - 50
      w = self.d - (2*self.e) - (2*eps)
      sq = [(x0 + eps, y0 + eps)]
      sq += Vector2D(0, h)
      sq += Vector2D(w,0)
      sq += Vector2D(0,-h)

      if (hand.lower() == "left") :
        pygame.draw.polygon(screenInst, sqBlackNoteLeftRGB, sq)

      if (hand.lower() == "right") :
        pygame.draw.polygon(screenInst, sqBlackNoteRightRGB, sq)

      if (hand.lower() == "neutral") :
        pygame.draw.polygon(screenInst, sqBlackNoteNeutralRGBAlpha, sq)

      # Show fingering
      if (finger in [1,2,3,4,5]) :
        fu.render(screenInst, str(finger), (x0+3,y0+23), 1, (240,240,240))
    
    # White note drawing
    else :
      eps = 3
      u = [x[0] for x in self.keyboardPolygons[note]]
      x0 = min(u); y0 = self.loc[1] + self.c + self.e
      h = self.a - (self.c + self.e) - (2*eps)
      w = self.b - (2*self.e) - (2*eps)
      sq = [(x0 + eps, y0 + eps)]
      sq += Vector2D(0, h)
      sq += Vector2D(w,0)
      sq += Vector2D(0,-h)
      
      if (hand.lower() == "left") :
        pygame.draw.polygon(screenInst, sqWhiteNoteLeftRGB, sq)
      
      if (hand.lower() == "right") :
        pygame.draw.polygon(screenInst, sqWhiteNoteRightRGB, sq)

      if (hand.lower() == "neutral") :
        pygame.draw.polygon(screenInst, sqWhiteNoteNeutralRGBAlpha, sq)

      # Show fingering
      if (finger in [1,2,3,4,5]) :
        fu.render(screenInst, str(finger), (x0+10,y0+23), 1, (240,240,240))



# =============================================================================
# Class: pianoRoll 
# =============================================================================
class PianoRoll :

  # ---------------------------------------------------------------------------
  # Constructor
  # ---------------------------------------------------------------------------
  def __init__(self, loc) :
    self.loc = loc
    self.noteArray = [[] for _ in range(128)]
    self.nTracks = 0
    self.eventTimeCodes = []
    
    # Color scheme
    self.keyLineRGB = (80, 140, 140)

    self.b = 25
    self.d = 12
    self.e = 1



  # ---------------------------------------------------------------------------
  # Method <loadPianoRollArray>
  # Converts a MIDI file to a piano roll i.e. a 128-elements array.
  # Input:
  # The MIDI file to read
  #
  # Output:
  # Fills the noteArray attribute of the object.
  #
  # pianoRollArray[60] = [note0, note1, ...]
  # noteXXX = instance of note() class
  # A note class has:
  # - noteXXX.start/.end (integer) : timestamp of its beginning/end
  # - noteXXX.hand (string: "l", "r" or ""): hand used to play the note
  # ---------------------------------------------------------------------------
  def loadPianoRollArray(self, midiFile) :

    mid = mido.MidiFile(midiFile)

    self.nTracks = len(mid.tracks)
    print(f"Tracks found: {self.nTracks}")

    # Allocate outputs
    self.noteArray = [[[] for _ in range(128)] for _ in range(self.nTracks)]
    self.eventTimeCodes = [[] for _ in range(self.nTracks)]

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
              
            self.noteArray[trackID][msg.note].append(Note(currTime, -1))
            
            if not(currTime in self.eventTimeCodes[trackID]) : 
              self.eventTimeCodes[trackID].append(currTime)
          
          # New note
          else :
            # Its duration is unknown for now, so set its endtime to "-1"
            self.noteArray[trackID][msg.note].append(Note(currTime, -1))
            
            if not(currTime in self.eventTimeCodes[trackID]) : 
              self.eventTimeCodes[trackID].append(currTime)



        # Keyrelease event ----------------------------------------------------
        if ((msg.type == 'note_off') or ((msg.type == 'note_on') and (msg.velocity == 0))) :
          
          # Take the latest event in the piano roll for this note
          noteObj = self.noteArray[trackID][msg.note][-1]
          
          # Close it
          self.noteArray[trackID][msg.note][-1].stopTime = currTime

          # if (noteObj.startTime == noteObj.stopTime) :
          #   print(f"[WARNING] MIDI note {msg.note} ({noteName(msg.note)}): ignoring note with null duration (start time = stop time = {noteObj.startTime})")
          #   self.noteArray[msg.note].pop()



        # Others --------------------------------------------------------------
        # Other MIDI events are ignored.



  # ---------------------------------------------------------------------------
  # Method <exportPianoRollArray>
  # TODO
  # ---------------------------------------------------------------------------
  def exportPianoRollArray(self, pianoRollFile) :
    print("TODO")




  # ---------------------------------------------------------------------------
  # Method <drawKeyLines>
  # Draw the lines leading to each key
  # ---------------------------------------------------------------------------
  def drawKeyLines(self, screenInst) :

    # Some shortcuts
    x0 = self.loc[0]; y0 = self.loc[1]
    b = self.b
    d = self.d

    xLines = [
      x0,                 # begin(A0)
      x0+(1*b)-(d//3),    # begin(Bb0)
      x0+(1*b)+(2*d//3),  # begin(B0)
    ]
    x0 = x0+(2*b)         # end(B0) = begin(C0)
    
    for oct in range(7) :
      xLines += [
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

    xLines += [
      x0,
      x0+(1*b)
    ]

    # Draw the lines
    for x in xLines :
      pygame.draw.line(screenInst, self.keyLineRGB, (x,100), (x,y0-5), 1)

    pygame.draw.line(screenInst, self.keyLineRGB, (xLines[0],100), (xLines[-1],100), 1)



  # ---------------------------------------------------------------------------
  # Method <drawPianoRoll>
  # Draw the piano roll
  # ---------------------------------------------------------------------------
  def drawPianoRoll(self, screenInst, startTimeCode) :
    print("todo")





