# -*- coding: utf-8 -*-
# =============================================================================
# Module name     : gangQin
# File name       : gangQin.py
# Purpose         : projet gangQin
# Author          : Quentin Biache
# Creation date   : September 1st, 2023
# =============================================================================

# TODO, par ordre décroissant de priorité :
# 1. cette version force à relâcher les touches avant de jouer les suivantes,
#   alors que parfois il faut les maintenir
# 2. permettre de faire une avance rapide
# 3. afficher un pianoroll pour savoir où on en est et connaître la durée des 
#    notes
# 4. ajouter un slider pour naviguer dans une partition longue 
#    (un vieux cercle qu'on drag&drop le long d'une droite suffit amplement)
# 5. ajouter des marqueurs et des boutons/raccourcis pour naviguer de l'un à 
#    l'autre



# =============================================================================
# Imports 
# =============================================================================
# For graphics
import pygame
import keyboardUtils as ku
import midiUtils as mu

# For MIDI
import mido
import rtmidi



# =============================================================================
# Settings
# =============================================================================
# Defines the criteria to decide when to move onto the next notes
# - exact: won't go further until the expected notes only are pressed, nothing else
# - allowSustain: accepts that the last valid notes are sustained
playComparisonMode = "exact"



# =============================================================================
# Main code
# =============================================================================

# Open the MIDI interface selection GUI
selectedDevice = mu.midiInterfaceGUI()
print(selectedDevice)

pygame.init()

# Define screen dimensions
screenWidth = 1320
screenHeight = 500
FPS = 60

# Create window
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("gangQin v1.0")

# Time management
clock = pygame.time.Clock()

# Create objects
keyboard = ku.Keyboard((10,300))
pianoRoll = ku.PianoRoll((10,300))

# Set the background color
backgroundRGB = (80, 120, 150)

# Read the MIDI file
#pianoRoll.loadPianoRollArray("Rachmaninoff_Piano_Concerto_No2_Op18.mid")
#pianoRoll.loadPianoRollArray("Sergei_Rachmaninoff_-_Moments_Musicaux_Op._16_No._4_in_E_Minor.mid")
pianoRoll.loadPianoRollArray("12_Etudes_Op.8__Alexander_Scriabin__tude_in_A_Major_-_Op._8_No._6.mid")



# =============================================================================
# Open MIDI keyboard interface
# =============================================================================
midiCurr = [0 for _ in range(128)]

def midiCallback(message) :
  if (message.type == 'note_on') :
    print(f"Note On: Note={message.note}, Velocity={message.velocity}")
    midiCurr[message.note] = 1
  elif (message.type == 'note_off') :
    print(f"Note Off: Note={message.note}, Velocity={message.velocity}")
    midiCurr[message.note] = 0

midiPort = mido.open_input(mu.selectedDevice, callback = midiCallback)



# =============================================================================
# Main loop
# =============================================================================
running = True
currTime = 0
timeCodes = [item for sublist in pianoRoll.eventTimeCodes for item in sublist]
timeCodes = list(set(timeCodes))
timeCodes.sort() 

while running:
  for event in pygame.event.get() :
    if (event.type == pygame.QUIT) :
      running = False

    if (event.type == pygame.KEYDOWN) :
      # if (event.key == pygame.K_q) :
      #   midiPort.close()
      #   pygame.quit()

      # # Rewind, 1 step
      # if (event.key == pygame.K_LEFT) :
      #   if (currTime > 0) :
      #     currTime -= 1
      #     print(currTime)

      # # Forward, 1 step
      # if (event.key == pygame.K_RIGHT) :
      #   if ((currTime+1) < (len(timeCodes)-1)) :
      #     currTime += 1
      #     print(currTime)

      keys = pygame.key.get_pressed()

      if keys[pygame.K_q] :
        midiPort.close()
        pygame.quit()

      # Jump backward: 1 step
      if (keys[pygame.K_LEFT] and not(keys[pygame.K_LCTRL])) :
        if (currTime > 0) :
          currTime -= 1
          print(f"Cursor: {currTime}")

      # Fast rewind: 10 steps
      if (keys[pygame.K_LEFT] and keys[pygame.K_LCTRL]) :
        if (currTime > 10) :
          currTime -= 10
          print(f"Cursor: {currTime}")

      # Jump forward: 1 step
      if (keys[pygame.K_RIGHT] and not(keys[pygame.K_LCTRL])) :
        if ((currTime+1) < (len(timeCodes)-1)) :
          currTime += 1
          print(f"Cursor: {currTime}")

      # Fast forward: 10 steps
      if (keys[pygame.K_RIGHT] and keys[pygame.K_LCTRL]) :
        if ((currTime+10) < (len(timeCodes)-1)) :
          currTime += 10
          print(f"Cursor: {currTime}")

      # TODO: auto-increase the step size if CTRL+left/right is hit multiple times in a row 


  # Clear the screen
  screen.fill(backgroundRGB)

  # Draw the keyboard on screen
  keyboard.drawKeys(screen)
  
  # Draw the piano roll on screen
  pianoRoll.drawKeyLines(screen)


  midiTeacher = [0 for _ in range(128)]
  for i in range(21, 108+1) :
    for trackID in range(pianoRoll.nTracks) :
      for evt in pianoRoll.noteArray[trackID][i] :
        if (evt.startTime == timeCodes[currTime]) :
          midiTeacher[i] = 1
          if (trackID == 0) :
            keyboard.keyPress(screen, i, hand = "left", finger = 1) 
          
          if (trackID == 1) :
            keyboard.keyPress(screen, i, hand = "right", finger = 2) 


  for i in range(21, 108+1) :
    if (midiCurr[i] == 1) :
      keyboard.keyPress(screen, i, hand = "neutral") 
  

  if (playComparisonMode == "exact") :
    if (midiTeacher == midiCurr) :
      currTime += 1
      print(f"currTime = {currTime}")



  # Handle keypresses
  # keys = pygame.key.get_pressed()
  
  # if (keys[pygame.K_LEFT]) :
  #   if (currTime > 0) :
  #     currTime -= 1
  #     print(currTime)

  # if (keys[pygame.K_RIGHT]) :
  #   if ((currTime+1) < (len(timeCodes)-1)) :
  #     currTime += 1
  #     print(currTime)

  # if (keys[pygame.K_q]) :
  #   midiPort.close()
  #   pygame.quit()





  clock.tick(FPS)

  # Update the display
  pygame.display.flip()

# Quit Pygame
pygame.quit()


