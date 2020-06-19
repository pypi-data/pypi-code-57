import os
from pathlib import Path

REMO_HOME = os.getenv('REMO_HOME', str(Path.home().joinpath('.remo')))
