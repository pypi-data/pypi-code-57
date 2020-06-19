import sys
import os

import mido

portname = sys.argv[1]

# Find Vibrance Port
if os.name == "posix":
    # macOS or Linux systems
    # Just create a virtual port
    outport = mido.open_output(portname)
elif os.name == "nt":
    # Windows system
    # Rely on external MIDI loopback software
    outport = mido.open_output(f"{portname} 4")
else:
    raise ValueError("unsupported OS")

try:
    while True:
        note = int(input("Note> "))

        msg = mido.Message("note_on")
        msg.note = note

        if outport.closed:
            break

        outport.send(msg)
finally:
    outport.close()
