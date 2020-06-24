import enum
import os


class McFileTypes (enum.Enum):
    BEAGLE = "beagle"
    HEPMC2 = "hepmc2"
    EIC_PYTHIA6 = "eic_pythia6"
    LUND = "lund"
    G4E = "g4e"
    UNKNOWN = "unknown"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


def detect_mc_type(file_name):
    """Automatically detects file type. Returns one of McFileTypes"""
    filename, extension = os.path.splitext(file_name)

    if 'root' in extension:
        raise ValueError("Auto identification of .root files is not yet implemented. "
                         "Please use --input-format flag. Example '--imput-format=g4e'")
    return detect_text_mc_type(file_name)


def detect_text_mc_type(file_name):
    """Automatically detects text file types. Returns one of McFileTypes"""

    with open(file_name, 'r') as f:
        line = ""
        try:
            while not line:                 # Just to fake a lot of readlines and hit the end
                line = next(f).replace('\n', '')
        except StopIteration:
            return McFileTypes.UNKNOWN
        if "BEAGLE EVENT FILE" in line:
            return McFileTypes.BEAGLE
        elif "HepMC" in line:
            return McFileTypes.HEPMC2
        elif "PYTHIA EVENT FILE" in line:
            return McFileTypes.EIC_PYTHIA6
        elif len(line.split()) == 10:
            return McFileTypes.PYTHIA_LUND
    return McFileTypes.UNKNOWN