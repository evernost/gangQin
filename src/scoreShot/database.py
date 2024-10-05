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
import random
import string



# =============================================================================
# Constants pool
# =============================================================================




# =============================================================================
# Main code
# =============================================================================
class Database :
  def __init__(self) :
    
    self.nSnapshots = 0
    self.snapshots = []
    

    
  
  def sanityCheck(self) :
    """
    Make sure the file associated to each snapshot exists.
    """
    print("todo")
  
  
  
  def insertAfter(self) :
    print("todo")
  

  
  def delete(self) :
    print("todo")

  
  
  def getListBoxDescriptor(self) :
    print("todo")
  
  
  def createFileName(self) :
    allowedChars = string.ascii_uppercase + string.digits
    
    return "".join(random.choice(allowedChars) for _ in range(5))