"""
__init__.py for ipywidgets_game_maze
"""
__version__ = '0.1'
from .Object3D import Object3D
from .StaticObject import StaticObject
from .value_player_widget import ValuePlayerWidget
from .timer import PerpetualTimer
from .Ant import Ant
from .Visualisation import Visualisation
from .Maze import Maze

__all__=["Object3D","StaticObject","value_player_widget","timer","Ant","Visualisation", "Maze"]

def _jupyter_nbextension_paths():
    return [dict(
        section="notebook",
        src="static",
        dest="ipywidgets_game_maze",
        require="")]

