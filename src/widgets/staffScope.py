# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : 
# File name     : staffScope.py
# Purpose       : viewer widget on the actual music score
# Author        : QuBi (nitrogenium@hotmail.com)
# Creation date : Sunday, 20 October 2024
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================


# Specs:
# - draws the staffScope widget
# - loads and resizes the score snapshot efficiently (loads and reshapes once)
# - draws the rectangle overlay on the score snapshot
# - handles the user interactions


# =============================================================================
# External libs 
# =============================================================================


import src.scoreShot.database as database

import pygame
import os



# =============================================================================
# Constants pool
# =============================================================================



# =============================================================================
# Main code
# =============================================================================
class StaffScope :

  """
  The StaffScope widget is ...
  """
  def __init__(self, songFile) :
    
    self.screen = None
    






    # User interaction queues
    self.msgQueueIn = []
    self.msgQueueOut = []


    # Internal initialisation
    self._loadDatabase(songFile)


    


  # ---------------------------------------------------------------------------
  # METHOD Database._loadDatabase()
  # ---------------------------------------------------------------------------
  def _loadDatabase(self, songFile) :
    """
    Generates the various names of files and directories associated with the 
    database.
    """
    
    self.db = database.Database(songFile)
    
    
    # (rootDir, rootNameExt) = os.path.split(prFile)
    # (rootName, _) = os.path.splitext(rootNameExt)
    # self.songName     = rootName
    # self.songFile     = rootNameExt
    # self.jsonName     = rootName + ".json"          # Example: "my_song.json"
    # self.jsonFile     = f"./snaps/{self.jsonName}"  # Example: "./snaps/my_song.json"
    # self.depotFolder  = f"./snaps/db__{rootName}"   # Example: "./snaps/db__my_song"



  # ---------------------------------------------------------------------------
  # METHOD Database._loadDatabase()
  # ---------------------------------------------------------------------------
  def loadScreen(self, screenObj) :
    self.screen = screenObj


