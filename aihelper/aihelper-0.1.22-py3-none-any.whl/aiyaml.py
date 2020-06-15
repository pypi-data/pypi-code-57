import os

def write_basic_yaml():
    return {
        "DIRECTORY": None,
        "WAVE LENGTHS": [None],
        "RMS": False,
    }

def write_yaml():
    return {
        "DIRECTORY": "",
        "WAVE LENGTHS": [None, None, None, None],
        "RMS": False
    }

def write_acd_thermal_yaml():
    return {
        "DIRECTORY": "",
        "WAVE LENGTHS": [None, None, None, None],
        "RMS": False,
        "MS Deadtime (Seconds)": 30
    }

def write_directories(data=None):
    if data:
        r_dict = {
            "DIRECTORY": data.get("DIRECTORY"),
            "BASELINE DIRECTORY": data.get("BASELINE DIRECTORY"),
            "GRADIENT": data.get("GRADIENTS", [10]),
            "ISOTHERMS": data.get("ISOTHERMS", [190, 220, 350]),
            "WAVE LENGTHS": data.get("WAVE LENGTHS", [None, None, None, None]),
            "RMS": data.get("RMS", True),
            "TECHNIQUES": data.get("TECHNIQUES"),
        }
    else:
        r_dict = {
            "DIRECTORY": os.getcwd(),
            "PROJECT": "DESCRIPTIVE PROJECT TITLE",
            "TOPICS": ["TANGO", "VOYAGER", "APOSTOLIC", "UNICORN"],
            "GRADIENTS": [10],
            "ISOTHERMS": [190, 220, 350],
            "TECHNIQUES": ["STA", "IR", "GC", "MS", "TG"],
        }
    return r_dict