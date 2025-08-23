# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : database
# File name     : database.py
# File type     : Python script (Python 3)
# Purpose       : visual database for music scores
# Author        : QuBi (nitrogenium@outlook.fr)
# Creation date : Tuesday, 01 October 2024
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# EXTERNALS
# =============================================================================
import src.scoreShot.snapshot as snapshot

import json
import os       # For file name manipulation / file existence check
import random



# =============================================================================
# CONSTANTS
# =============================================================================
# None.



# =============================================================================
# CLASS DEFINITION
# =============================================================================
class Database :

  """
  DATABASE object
  
  Class definition for the snapshot database.
  
  This class manages the snapshots files and their arrangement within 
  the database.
  """
  def __init__(self, jsonFile) :
    
    self.nSnapshots = 0             # Number of score snapshots available in the database
    self.snapshots = []             # List of Snapshot objects
    
    self.songName     = ""          # Name of the song
    self.jsonName     = ""          # Name of the database file
    self.jsonFile     = ""          # Full name of the databse file (path + filename)
    self.depotFolder  = ""          # Directory where all the snapshots of the song are stored
    
    self.description  = ""          # Description string for the database
                                    # e.g. name of the PDF file for the score, display settings used etc.

    self.hasUnsavedChanges = False  # Turns True if anything has been modified in the database
    self.changeLog = []

    self.indexLastInsertion = -1    # Index where the last snapshot insertion occured (needed for TODO)

    # Initialisation procedures
    self._initFileNames(jsonFile)
    self._loadJSON()
    self._integrityCheck()



  # ---------------------------------------------------------------------------
  # METHOD Database._initFileNames()                                  [PRIVATE]
  # ---------------------------------------------------------------------------
  def _initFileNames(self, jsonFile) :
    """
    Generates the various names of files and directories associated with the 
    database.
    """
    
    (_, rootNameExt) = os.path.split(jsonFile)
    (rootName, _) = os.path.splitext(rootNameExt)
    self.songName     = rootName
    self.jsonFile     = jsonFile
    self.jsonName     = rootName + ".json"          # Example: "my_song.json"
    self.depotFolder  = f"./snaps/db__{rootName}"   # Example: "./snaps/db__my_song"



  # ---------------------------------------------------------------------------
  # METHOD Database._loadJSON()                                       [PRIVATE]
  # ---------------------------------------------------------------------------
  def _loadJSON(self) -> None :
    """
    Loads the database file (JSON), creates one if it does not exist.
    
    NOTE: the 'jsonFile' and the 'depotFolder' are seen as one. 
    If one of them is missing, it starts over with a new database.
    
    We do not want to deal with partial databases ('depotFolder' exists but
    not 'jsonFile', etc.) attempt recoveries or any sort of thing.
    There is no obvious reason to edit these elements outside the app.
    
    Just don't touch the database files and let the app access and manage it!
    """

    if os.path.exists(self.jsonFile) :
      if os.path.exists(self.depotFolder) :
        with open(self.jsonFile, "r") as jsonFile :
          jsonData = json.load(jsonFile)
          self._initFromDict(jsonData)

      # The 'jsonFile' exists, but 'depotFolder' doesn't.
      # Possibly the database was just created
      else :
        print("[DEBUG] No depot folder found for the database.")
        os.makedirs(self.depotFolder)

        # This is where we would eventually initialise the rest of the 
        # Database attributes. 
        # But try to avoid it and design the default attributes so that
        # we don't have to.
        # Otherwise it creates a double init and that's ugly.
        # self.nSnapshots = 0
        # ...

    else :
      
      # The 'depotFolder' exists but not the 'jsonFile'.
      # There is now obvious way to recover from that.
      if os.path.exists(self.depotFolder) :
        print("[WARNING] No json associated with the depot folder. Can't load the StaffScope view!")
        #exit()
        
      # Nothing exists: they need to be created
      else :
        print("[INFO] Creating new database.")



  # ---------------------------------------------------------------------------
  # METHOD Database._integrityCheck()                                 [PRIVATE]
  # ---------------------------------------------------------------------------
  def _integrityCheck(self) :
    """
    Runs some checks on the database before yielding control to the user:
    - checks if all the snapshot files exist
    - checks if cursor ranges are inconsistent
    """
    
    if os.path.exists(self.jsonFile) :
      if os.path.exists(self.depotFolder) :
        with open(self.jsonFile, "r") as jsonFile :
          jsonData = json.load(jsonFile)
          
          if (self.songName != jsonData["songName"]) :
            print("[WARNING] Database._integrityCheck(): 'songName' attribute is inconsistent. Possible database corruption.")  

          if (self.jsonName != jsonData["jsonName"]) :
            print("[WARNING] Database._integrityCheck(): 'jsonName' attribute is inconsistent. Possible database corruption.")

          if (self.jsonFile != jsonData["jsonFile"]) :
            print("[WARNING] Database._integrityCheck(): 'jsonFile' attribute is inconsistent. Possible database corruption.")

          if (self.depotFolder != jsonData["depotFolder"]) :
            print("[WARNING] Database._integrityCheck(): 'depotFolder' attribute is inconsistent. Possible database corruption.")


    # TODO: check the snapshot attributes
    # ...



    # TODO: indicate what percentage of the cursor span has snapshot
    # associated to them.
    # ...


    # TODO: check if there are overlaps in the snapshots cursor span.
    # There should be none.
    # ...



  # ---------------------------------------------------------------------------
  # METHOD Database.isEmpty()
  # ---------------------------------------------------------------------------
  def isEmpty(self) :
    """
    Returns True if the Database contains no snapshot.
    """
    
    return (len(self.snapshots) == 0)



  # ---------------------------------------------------------------------------
  # METHOD Database.insert()
  # ---------------------------------------------------------------------------
  def insert(self, img, index = -1) :
    """
    Inserts a new snapshot (PIL image object) in the snapshot list at the 
    specified index.
    
    After the insertion, image will be located at 'self.snapshots[index]'.

    If index = -1 (default) the image is appened at the end of the list.
    """
    
    # Invalid input detection
    if (index < -1) :
      print(f"[DEBUG] Database.insert: index cannot be less than -1 (got: {index})")
      return None
    elif (index > self.nSnapshots) :
      print(f"[DEBUG] Database.insert: cannot insert beyond the last index (nSnapshots = {self.nSnapshots}, index = {index})")
      return None
    elif (index == -1) : 
      insertIndex = self.nSnapshots
    else : 
      insertIndex = index

    # Get a name for the snapshot file
    filename = self.generateFileName() + ".png"

    # Save the snapshot image
    img.save(f"{self.depotFolder}/{filename}")
    print(f"[DEBUG] Screenshot saved as '{filename}'")
    
    # Create the snapshot object 
    s = snapshot.Snapshot()
    s.dir         = self.depotFolder
    s.file        = filename
    s.index       = insertIndex
    s.displayName = f"Capture {insertIndex+1}"
    
    # Insert the snapshot in the list
    self.snapshots.insert(insertIndex, s)
    
    # If inserted before the end, all indices after need to be updated.
    if ((insertIndex >= 0) and (insertIndex <= (self.nSnapshots-1))) :
      for i in range(insertIndex+1, self.nSnapshots) :
        self.snapshots[i].index = i+1
    
    self.nSnapshots += 1
    self.isEmpty = False
    self.hasUnsavedChanges = True
    self.changeLog.append(f"- snap insertion at {insertIndex}")

    print(f"[DEBUG] nSnapshots = {self.nSnapshots}")

    

  # ---------------------------------------------------------------------------
  # METHOD Database.delete()
  # ---------------------------------------------------------------------------
  def delete(self, index) :
    """
    Deletes the snapshot from the snapshot list at the specified index.
    
    If index = -1 (default) the last item of the list is deleted.
    """
  
    print("[WARNING] Method 'Database.delete' is not implemented yet.")

    # Don't forget to update this flag
    self.isEmpty = (self.nSnapshots == 0)
    
    self.changeLog.append(f"- snap insertion at {index}")

  

  # ---------------------------------------------------------------------------
  # METHOD Database.getListBoxDescriptor()
  # ---------------------------------------------------------------------------  
  def getListBoxDescriptor(self) :
    """
    Returns the list of items that need to be shown in the scoreShot GUI's listbox.
    """
    
    L = [s.displayName for s in self.snapshots]
    return L
  


  # ---------------------------------------------------------------------------
  # METHOD Database.getSnapshotFileByIndex()
  # ---------------------------------------------------------------------------  
  def getSnapshotFileByIndex(self, index) :
    """
    Returns the full name (path + file) of the .png from its index in the database.
    Returns an empty string if the index is invalid.
    """
    
    if ((index >= 0) and (index <= (self.nSnapshots-1))) :
      s = self.snapshots[index]
      return f"{s.dir}/{s.file}"
    
    else :
      print(f"[DEBUG] Database.getSnapshotFileByIndex(): requested index {index} cannot be loaded.")
      return ""
    


  # ---------------------------------------------------------------------------
  # METHOD Database.getIndexByCursor()
  # ---------------------------------------------------------------------------  
  def getIndexByCursor(self, cursor) :
    """
    Finds the snapshot in the database that covers the cursor value passed as argument.
    Returns its index in the database if found, otherwise returns -1.
    """
    
    for (index, s) in enumerate(self.snapshots) :
      if ((cursor >= s.cursorMin) and (cursor <= s.cursorMax)) :
        return index
    
    return -1



  # ---------------------------------------------------------------------------
  # METHOD Database.generateFileName()
  # ---------------------------------------------------------------------------  
  def generateFileName(self) :
    """
    Generates a unique file name for a snapshot.
    
    NOTE: generation shall be done here (at the database level) because unicity 
    requires knowledge of all names in the db.
    """

    # Restrain to a subset of chars 
    allowedChars = "ABCDEFGHKMNPQRTUVWXYZ" + "23456789"    
    
    fileList = [f for f in os.listdir(self.depotFolder) if f.endswith(".png")]
    while True :
      generatedName = "".join(random.choice(allowedChars) for _ in range(6))
      if not(generatedName in fileList) :
        break
    
    return generatedName

    

  # ---------------------------------------------------------------------------
  # METHOD Database._initFromDict()                                   [PRIVATE]
  # ---------------------------------------------------------------------------
  def _initFromDict(self, jsonData) -> None :
    """
    Loads the content of the Database class from a dictionary for easier 
    serialisation.
    """
    
    self.nSnapshots         = jsonData["nSnapshots"]
    self.snapshots          = [(s := snapshot.Snapshot()).fromDict(snapData) or s for snapData in jsonData["snapshots"]]
    # self.songName           = jsonData["songName"]              # Already known
    # self.songFile           = jsonData["songFile"]              # Already known
    # self.jsonName           = jsonData["jsonName"]              # Already known
    # self.jsonFile           = jsonData["jsonFile"]              # Already known
    # self.depotFolder        = jsonData["depotFolder"]           # Already known
    # self.hasUnsavedChanges  = jsonData["hasUnsavedChanges"]     # Useless
    # self.indexLastInsertion = jsonData["indexLastInsertion"]    # Useless
    


  # ---------------------------------------------------------------------------
  # METHOD Database.toDict()
  # ---------------------------------------------------------------------------
  def toDict(self) :
    """
    Converts the content of the Database class to a dictionary for easier 
    serialisation.
    """

    # TODO: iterate over the attributes instead of manually listing all of them.
    return {
      "nSnapshots"        : self.nSnapshots,
      "snapshots"         : [s.toDict() for s in self.snapshots],
      "isEmpty"           : self.isEmpty,
      "songName"          : self.songName,
      "songFile"          : self.songFile,
      "jsonName"          : self.jsonName,
      "jsonFile"          : self.jsonFile,
      "depotFolder"       : self.depotFolder,
      "hasUnsavedChanges" : self.hasUnsavedChanges
    }



  # ---------------------------------------------------------------------------
  # METHOD Database.save()
  # ---------------------------------------------------------------------------  
  def save(self) :
    """
    Saves the current database state in a JSON file.
    """
    
    self._changeLogClear()

    d = self.toDict()
    with open(self.jsonFile, "w") as jsonFile :
      json.dump(d, jsonFile, indent = 2)

    print("Done.")

    

  # ---------------------------------------------------------------------------
  # METHOD Database._changeLogClear()
  # ---------------------------------------------------------------------------  
  def _changeLogClear(self) :
    """
    Clears the change log.
    """
    
    self.hasUnsavedChanges = False
    self.changeLog = []
    


# =============================================================================
# UNIT TESTS
# =============================================================================
if (__name__ == "__main__") :
  
  db = Database("./snaps/Rachmaninoff_Moment_Musical_Op_16_No_4.json")
  
  
  
  
  db = Database("TEST")
  
  s = db.generateFileName()
  print(f"[DEBUG] Sample internal file name: '{s}'")
