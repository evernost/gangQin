import mido
import tkinter as tk
from tkinter import ttk

def get_midi_devices():
  return mido.get_input_names()

def select_midi_device(event) :
  selected_device = device_combo.get()
  print(f"Selected MIDI Device: {selected_device}")
  root.destroy()

# Create the main window
root = tk.Tk()
root.title("MIDI Device Selector")
# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the window's position to center it on the screen
window_width = 300  # You can adjust the window size
window_height = 150
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Get the list of MIDI devices
midi_devices = get_midi_devices()

# Create a label
label = tk.Label(root, text = "Select a MIDI device:")
label.pack(pady=10)

# Create a dropdown list
device_combo = ttk.Combobox(root, values = midi_devices)
device_combo.pack(pady=5)

# Create a button to select the device
select_button = tk.Button(root, text = "Select", command = lambda : select_midi_device(None))
select_button.pack(pady=10)

root.mainloop()

print('chatte flamande')