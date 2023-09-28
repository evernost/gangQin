# -*- coding: utf-8 -*-
# =============================================================================
# Module name     : pygameStudy6
# File name       : pygameStudy6.py
# Purpose         : yet another study on pygame
# Author          : Quentin Biache
# Creation date   : September 22nd, 2023
# =============================================================================

# =============================================================================
# Imports 
# =============================================================================
import pygame

charPolygons = {}

charPolygons["0"] = [
  [0, 1, 1, 1, 0],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 1, 1],
  [1, 0, 1, 0, 1],
  [1, 1, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [0, 1, 1, 1, 0]
]

charPolygons["1"] = [
  [0, 0, 1, 0, 0],
  [0, 1, 1, 0, 0],
  [0, 0, 1, 0, 0],
  [0, 0, 1, 0, 0],
  [0, 0, 1, 0, 0],
  [0, 0, 1, 0, 0],
  [0, 1, 1, 1, 0]
]

charPolygons["2"] = [
  [0, 1, 1, 1, 0],
  [1, 0, 0, 0, 1],
  [0, 0, 0, 0, 1],
  [0, 0, 0, 1, 0],
  [0, 0, 1, 0, 0],
  [0, 1, 0, 0, 0],
  [1, 1, 1, 1, 1]
]

charPolygons["3"] = [
  [1, 1, 1, 1, 1],
  [0, 0, 0, 1, 0],
  [0, 0, 1, 0, 0],
  [0, 0, 0, 1, 0],
  [0, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [0, 1, 1, 1, 0]
]

charPolygons["4"] = [
  [0, 0, 0, 1, 0],
  [0, 0, 1, 1, 0],
  [0, 1, 0, 1, 0],
  [1, 0, 0, 1, 0],
  [1, 1, 1, 1, 1],
  [0, 0, 0, 1, 0],
  [0, 0, 0, 1, 0]
]

charPolygons["5"] = [
  [1, 1, 1, 1, 1],
  [1, 0, 0, 0, 0],
  [1, 1, 1, 1, 0],
  [0, 0, 0, 0, 1],
  [0, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [0, 1, 1, 1, 0]
]

# charPolygons["1"] = [
#   [0, 0, 0, 0, 0],
#   [0, 0, 0, 0, 0],
#   [0, 0, 0, 0, 0],
#   [0, 0, 0, 0, 0],
#   [0, 0, 0, 0, 0],
#   [0, 0, 0, 0, 0],
#   [0, 0, 0, 0, 0]
# ]

def Qprint(screenInst, char, loc, size) :
  x0 = loc[0]; y0 = loc[1]
  w = size; h = size
  col = (40,50,60)

  for l in charPolygons[char] :
    for c in l :
      if (c > 0) :
        p = [(x0, y0), (x0 + (w-1), y0), (x0 + (w-1), y0 + (h-1)), (x0, y0 + (h-1))]
        pygame.draw.polygon(screenInst, col, p)

      x0 += w
    
    x0 = loc[0]; y0 += h



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

# Set the background color
backgroundRGB = (60, 120, 120)



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

    Qprint(screen, "0", (100,100))
    Qprint(screen, "1", (200,100))
    Qprint(screen, "2", (300,100))
    Qprint(screen, "3", (400,100))
    Qprint(screen, "4", (500,100))
    Qprint(screen, "5", (600,100))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()


