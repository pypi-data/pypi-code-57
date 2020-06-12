"""
LCMAP Time Series and Analysis Plotting Tool
"""
import os
import sys
from PyQt5.QtWidgets import QApplication
import lcmap_tap
from lcmap_tap.logger import log, exc_handler
from lcmap_tap.Controls.controls import MainControls
from lcmap_tap.storage import local

try:
    from pip._internal.operations import freeze
except ImportError:
    from pip.operations import freeze

sys.excepthook = exc_handler


def main():
    """
    TAP main entry point
    Setup working directory and execute Qt main window
    """
    lcmap_tap.mkdirs(lcmap_tap.home())
    log.debug("*** System Information ***")
    log.debug("Platform: %s", sys.platform)
    log.debug("Python: %s", str(sys.version).replace("\n", ""))
    log.debug("Pip: %s", ", ".join(freeze.freeze()))
    log.info("Working directory is: %s", lcmap_tap.home())
    log.info("Running lcmap-tap version %s", lcmap_tap.version())

    # Retrieve config file required for tap to get external data
    config_file = os.path.join(lcmap_tap.top_dir(), "config.yaml")
    cfg = local.load_config(config_file)

    if not cfg:
        log.error("Could not find config file: %s", config_file)
        log.critical(
            "Configuration file not present, TAP Tool will not be able to retrieve data.  Exiting"
        )
        sys.exit(1)

    log.debug("Using config: %s", config_file)

    # Create a QApplication object, necessary to manage the GUI control flow and settings
    app = QApplication(sys.argv)
    control_window = MainControls(config=cfg)

    if control_window:
        # Enter the main event loop
        # begin event handling for application widgets until exit() is called

        sys.exit(app.exec_())


if __name__ == "__main__":
    main()
