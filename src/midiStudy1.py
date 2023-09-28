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
import mido
import rtmidi


input_port = mido.open_input("UMX 49 0")

try:
    for message in input_port:
        if message.type == 'note_on':
            print(f"Note On: Note={message.note}, Velocity={message.velocity}")
        elif message.type == 'note_off':
            print(f"Note Off: Note={message.note}, Velocity={message.velocity}")
except KeyboardInterrupt:
    print("\nExiting...")
finally:
    input_port.close()
