import os
import atexit

import mido

from . import driver


class MidiDriver(driver.Driver):
    """Driver that reads messages from a virtual MIDI input port. Intended
    for reading notes on a MIDI track in DAW software such as Ableton.

    On Windows, using this requires external software to create a loopback
    port.
    """

    def __init__(self, name="", portname="vibrance"):
        super().__init__(name)
        self.portname = portname

    def _open(self):
        if os.name == "posix":
            self.midi = mido.open_input(self.portname, virtual=True)
        elif os.name == "nt":
            try:
                potential_ports = [port for port in mido.get_input_names()
                                   if " ".join(port.split(" ")[:-1])
                                   == self.portname]
                self.midi = mido.open_input(potential_ports[0])
            except OSError as e:
                raise OSError("It looks like you're trying to use Vibrance's "
                              "MIDI interface on a Windows device. Vibrance "
                              "MIDI uses 'virtual' MIDI ports in order to "
                              "function properly. However, Windows does not "
                              "support virtual ports. Please install the "
                              "program 'loopMIDI' and create a loopback "
                              "port manually before running Vibrance.") from e
        else:
            raise ValueError("unsupported OS")

        atexit.register(self.close)

    def _close(self):
        self.midi.close()
        self.midi = None

    def _read(self):
        events = []
        for msg in self.midi.iter_pending():
            if msg.type not in ("note_on", "note_off"):
                return tuple()

            event_attrs = {"note": msg.note,
                           "velocity": msg.velocity,
                           "channel": msg.channel,
                           "time": msg.time}

            events.append({"driver": "midi",
                           "type": msg.type, **event_attrs})

            events.append({"driver": "midi",
                           "type": f"{msg.type}_{msg.note}", **event_attrs})

            octave = msg.note // 12 - 2

            events.append({"driver": "midi",
                           "type": f"{msg.type}_oct_{octave}", **event_attrs})

        return tuple(events)

    def getStatus(self):
        status = {}

        if self.enabled:
            status["health"] = "success"
            status["message"] = "MIDI Enabled"
        else:
            status["health"] = "inactive"
            status["message"] = "MIDI Disabled"

        return status
