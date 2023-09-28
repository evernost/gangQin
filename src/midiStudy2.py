import mido
from mido import MidiFile

# Create an empty list to store MIDI events
midi_events = []

# Define a function to handle incoming MIDI messages
def midi_callback(message):
    # Append the MIDI message to the list
    midi_events.append(message)
    print(message.note)

# Open a MIDI input port (replace 'YourMIDIPortName' with your actual MIDI device name)
input_port = mido.open_input('UMX 49 0', callback=midi_callback)

# Keep the script running to listen for MIDI events
try:
    print("Listening for MIDI events. Press Ctrl+C to exit.")
    while True:
        pass
except KeyboardInterrupt:
    print("\nExiting...")

# Close the MIDI input port when done
input_port.close()

# Save the recorded MIDI events to a MIDI file (optional)
with MidiFile() as midi_file:
    for event in midi_events:
        midi_file.tracks.append([event])

print("MIDI events recorded.")
