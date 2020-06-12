"""These are artists on the plot figure that we want to set symbology for"""

import os
import yaml
import lcmap_tap
from lcmap_tap.logger import log
from lcmap_tap.Plotting import DEFAULTS, LOOKUP, LEG_DEFAULTS
from lcmap_tap.storage import local


config_file = os.path.join(lcmap_tap.home(), "plot_config.yml")


class PlotConfig:
    """
    Load, update, or save the plotting configuration.
    """

    def __init__(self):

        self.opts = local.load_config(config_file)

        if not self.opts:
            self.opts = {"DEFAULTS": DEFAULTS, "LEG_DEFAULTS": LEG_DEFAULTS}

    def update_config(self, item, params):
        """
        Update already loaded/initialized plotting configuration.
        """
        log.debug("PARAMS: %s", params)

        _id = LOOKUP[item]

        if _id is "highlight_pick":
            # 's' won't work for plots, only for scatters
            params["ms"] = params["s"]

            params["mec"] = params["color"]

            params.pop("s", None)

            params.pop("color", None)

        bg_color = params.pop("background")

        temp = self.opts["DEFAULTS"][_id]

        for key, value in params.items():
            temp[key] = value

        self.opts["DEFAULTS"][_id] = temp

        self.opts["DEFAULTS"]["background"]["color"] = bg_color

        temp = self.opts["LEG_DEFAULTS"][_id]

        for key, value in params.items():
            # Don't want to change symbol size on the legend
            if key is not "s":
                temp[key] = value

        self.opts["LEG_DEFAULTS"][_id] = temp

    def save_config(self):
        """
        Save plotting configuration to an external file.
        """
        with open(config_file, "w") as f:
            yaml.dump(self.opts, f, default_flow_style=False)
