# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : scoreShot_capture
# File name     : scoreShot_capture.py
# Purpose       : application entry point for the scoreShot capturing tool
# Author        : QuBi (nitrogenium@hotmail.com)
# Creation date : Monday, 24 September 2024
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# External libs 
# =============================================================================
import tkinter as tk
from PIL import ImageGrab



# =============================================================================
# Main code
# =============================================================================



def take_screenshot(event):
  
  x = root.winfo_x()
  y = root.winfo_y()
  width = root.winfo_width()
  height = root.winfo_height()
  
  
  bbox = (x, y, x + width, y + height)
  
  
  screenshot = ImageGrab.grab(bbox)
  screenshot.save("screenshot.png")
  print("[DEBUG] Screenshot saved as 'screenshot.png'.")




def update_mouse_position():
  x, y = root.winfo_pointerxy()
  print(f"Mouse Position: X: {x}, Y: {y}")
  
  root.after(200, update_mouse_position)

def on_quit(event) : 
  print("Exiting app...")
  root.destroy()











root = tk.Tk()
root.geometry("800x300")
root.config(bg = "gray")

root.title("scoreShot - Capture v0.1 [ALPHA] (September 2024)")
root.attributes('-topmost', True)

# Create a frame with a transparent background
frame = tk.Frame(root, bg = "red")
frame.pack(expand=True, fill="both", padx = 20, pady = 20)

# Make the frame background (content area) transparent
root.attributes("-transparentcolor", "red")

# Add some content (label) inside the frame
label = tk.Label(frame, text="This is a transparent window!", font=("Arial", 20), bg="white")
label.pack(pady=50)


root.bind('<s>', take_screenshot)
root.bind('<q>', on_quit)

update_mouse_position()

root.mainloop()
