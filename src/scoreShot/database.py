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
    self.isEmpty = True
    
    self.songName = ""      # Name of the song file
    self.jsonName = ""      # Name of the database file
    self.jsonFile = ""      # Full name of the databse file (path + filename)
    
    self.snapFolder = ""    # Directory where all the snapshots of the song are stored
    
    self.hasUnsavedChanges = False

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
    
    # TODO: forbid any whitespace in the name, or dots, commas, etc.
    
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
    
    NOTE: the JSON and the snapshot folder are seen as inseparable. 
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
        
        # Rename the current snapshot folder
        # ...
        

        # Create a brand new one
        # ...
        
        
      
      else : 
        with open(self.file, "r") as jsonFile :
          data = json.load(jsonFile)
        
        


    
  # ---------------------------------------------------------------------------
  # METHOD Database._sanityCheck()
  # ---------------------------------------------------------------------------
  def _sanityCheck(self) :
    """
    Make sure the all the files listed in the database exist.
    """
    print("[WARNING] Method 'Database._sanityCheck' is not implemented yet.")
  
  
  
  # ---------------------------------------------------------------------------
  # METHOD Database.insert()
  # ---------------------------------------------------------------------------
  def insert(self, img, index = -1) :
    """
    Inserts a new snapshot (PIL image object) in the snapshot list at the 
    specified index.
    
    After the insertion, image will be located at 'self.snapshots[index]'.

    If index = -1 (default) the image is inserted at the end of the list.
    """
    
    # Get a name for the snapshot file
    name = self.generateFileName()

    # Save the file
    img.save(f"{self.snapFolder}/{name}.png")
    print(f"[DEBUG] Screenshot saved as '{name}.png'")
    
    # Create the snapshot object 
    s = snapshot.Snapshot()
    s.dir         = self.snapFolder
    s.name        = name
    s.index       = index
    s.displayName = f"Capture {index}"

    # Insert the snapshot in the list.
    # If inserted before the end, all indices need to be updated.
    if ((index >= 0) and (index <= (self.nSnapshots-2))) :
      self.snapshots.insert(index, s)

      for i in range(index+1, self.nSnapshots) :
        self.snapshots[i].index = i+1

      self.nSnapshots += 1
      self.hasUnsavedChanges = True

    elif ((index == -1) or (index == (self.nSnapshots-1))) :
      self.snapshots.insert(index, s)
      self.nSnapshots += 1
      self.hasUnsavedChanges = True

    else :
      print("[ERROR] Invalid index.")

    print(f"[DEBUG] nSnapshots = {self.nSnapshots}")

    


  # ---------------------------------------------------------------------------
  # METHOD Database.delete()
  # ---------------------------------------------------------------------------
  def delete(self) :
    """
    Deletes the snapshot from the snapshot list at the specified index.
    
    If index = -1 (default) the last item of the list is deleted.
    """
    print("[WARNING] Method 'Database.delete' is not implemented yet.")

  

  # ---------------------------------------------------------------------------
  # METHOD Database.getListBoxDescriptor()
  # ---------------------------------------------------------------------------  
  def getListBoxDescriptor(self) :
    """
    Returns the list of items that need to be shown in the scoreShot GUI's listbox.
    """
    print("[WARNING] Method 'Database.getListBoxDescriptor' is not implemented yet.")

  
  

  # ---------------------------------------------------------------------------
  # METHOD Database.generateFileName()
  # ---------------------------------------------------------------------------  
  def generateFileName(self) :
    """
    Generates a unique file name for a snapshot.
    
    NOTE: generation shall be done at the database level (not Snapshot object level)
    because unicity requires knowledge of all names in the db.
    """

    # Restrain to a subset of chars 
    allowedChars = "ABCDEFGHKMNPQRTUVWXYZ" + "23456789"    
    return "".join(random.choice(allowedChars) for _ in range(6))
  


  # ---------------------------------------------------------------------------
  # METHOD Database.save()
  # ---------------------------------------------------------------------------  
  def save(self) :
    """
    Saves the current database state in a JSON file.
    """
    print("[WARNING] Method 'Database.getListBoxDescriptor' is not implemented yet.")



# =============================================================================
# Unit tests
# =============================================================================
if (__name__ == "__main__") :
  db = Database("TEST")
  
  s = db.generateFileName()
  print(f"[DEBUG] Sample internal file name: '{s}'")
