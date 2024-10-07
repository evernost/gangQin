# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : database
# File name     : database.py
# Purpose       : score capture database class
# Author        : QuBi (nitrogenium@hotmail.com)
# Creation date : Tuesday, 01 October 2024
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================






# =============================================================================
# External libs 
# =============================================================================
import json
import os
import random
import snapshot
import string



# =============================================================================
# Constants pool
# =============================================================================




# =============================================================================
# Main code
# =============================================================================
class Database :
  def __init__(self, prFile) :
    
    self.nSnapshots = 0
    self.snapshots = []
    
    self.songName = ""      # Name of the song file
    self.jsonName = ""      # Name of the database file
    self.jsonFile = ""      # Full name of the databse file (path + filename)
    
    self.snapFolder = ""    # Directory where all the snapshots of the song are stored
    
    self._makeDatabaseFileName(prFile)
    self._init()
    self._sanityCheck()



  # ---------------------------------------------------------------------------
  # METHOD Database._makeDatabaseFileName()
  # ---------------------------------------------------------------------------
  def _makeDatabaseFileName(self, prFile) :
    """
    Generates the name of the database file based on the .pr file.
    """
    
    # TODO: forbid any whitespace in the name.
    
    (rootDir, rootNameExt) = os.path.split(prFile)
    (rootName, _) = os.path.splitext(rootNameExt)
    self.songName   = rootNameExt
    self.jsonName   = rootName + ".json"          # Example: "my_song.json"
    self.jsonFile   = f"./snaps/{self.jsonName}"  # Example: "./snaps/my_song.json"
    self.snapFolder = f"./snaps/db__{rootName}"   # Example: "./snaps/db__my_song"



  # ---------------------------------------------------------------------------
  # METHOD Database._init()
  # ---------------------------------------------------------------------------
  def _init(self) :
    """
    Loads the database file (JSON), creates one if it does not exist.
    
    NOTE: the JSON and the snapshot folder are seen as one. 
    If any is missing, it starts over with a new database.
    We do not want to deal with partial databases, attempt recoveries or any sort
    of thing. Just don't touch the database files and let the app access and manage it!
    """
        
    # Snapshot folder inexistent: the JSON is discarded for a new one.
    if not(os.path.exists(self.snapFolder)) :
      os.makedirs(self.snapFolder)

      # This is where we would eventually initialise the rest of the 
      # Database attributes. 
      # But try to avoid it and design the default attributes so that
      # we don't have to.
      # Otherwise it creates a double init and that's ugly.
      # self.nSnapshots = 0
      # ...


    # Snapshot folder exists
    else :
      if not(os.path.exists(self.jsonFile)) :
        print("[DEBUG] The snapshot directory exists, but there is no JSON.")
        exit()
      
      else : 
        with open(self.file, "r") as jsonFile :
          data = json.load(jsonFile)
        
        


    
  
  def _sanityCheck(self) :
    """
    Make sure the all the files listed in the database exist.
    """
    print("[WARNING] Method '_sanityCheck' is todo!")
  
  
  
  def insertAfter(self) :
    print("todo")
  

  
  def delete(self) :
    print("todo")

  
  
  def getListBoxDescriptor(self) :
    """
    Returns the list of items that need to be shown in the scoreShot GUI's listbox.
    """
    print("[WARNING] Method 'getListBoxDescriptor' is todo!")
  
  
  def createFileName(self) :
    allowedChars = string.ascii_uppercase + string.digits
    
    return "".join(random.choice(allowedChars) for _ in range(5))