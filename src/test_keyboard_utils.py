# -*- coding: utf-8 -*-
# =============================================================================
# Module name     : gangQin
# File name       : gangQin.py
# Purpose         : projet gangQin
# Author          : Quentin Biache
# Creation date   : September 1st, 2023
# =============================================================================

# =============================================================================
# Imports 
# =============================================================================
import pygame
import keyboard_utils as ku



# =============================================================================
# Main code
# =============================================================================
pygame.init()

# Define screen dimensions
screenWidth = 1320
screenHeight = 500

# Create window
screen = pygame.display.set_mode((screenWidth, screenHeight))


pygame.display.set_caption("test poly_utils")

# Create objects
keyboard = ku.Keyboard((10,300))
pianoRoll = ku.PianoRoll((10,300))

# Set the background color
backgroundRGB = (60, 120, 120)

pianoRoll.midiToPianoRollArray("Rachmaninoff_Piano_Concerto_No2_Op18.mid")

# =============================================================================
# Main loop
# =============================================================================
running = True
while running:
  for event in pygame.event.get() :
    if (event.type == pygame.QUIT) :
      running = False

    # Clear the screen
    screen.fill(backgroundRGB)

    # Draw the keyboard on screen
    keyboard.drawKeys(screen)
    
    # Draw the piano roll on screen
    pianoRoll.drawKeyLines(screen)

    for i in range(21,90) :
      keyboard.keyPress(screen, i, hand = "left") 

    # keyboard.keyPress(screen, 60, hand = "left") 
    # keyboard.keyPress(screen, 62, hand = "left")
    # keyboard.keyPress(screen, 80, hand = "left") 

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()


