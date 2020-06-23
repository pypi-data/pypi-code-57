"""
Use Leaflet JavaScript API to display an interactive web map within a QWidget
"""
import sys

import pkg_resources
from PyQt5.Qt import PYQT_VERSION_STR
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QDir
from PyQt5.QtCore import QObject
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from lcmap_tap.Controls import UNITS
from lcmap_tap.logger import exc_handler
from lcmap_tap.logger import log
from lcmap_tap.MapCanvas import geojson
from lcmap_tap.RetrieveData.retrieve_geo import GeoInfo


try:
    # noinspection PyUnresolvedReferences
    from PyQt5.QtWebEngineWidgets import QWebEngineView

    USE = "UseWebEngineView"

except ImportError as e:
    log.error("Exception: %s", e, exc_info=True)

    # noinspection PyUnresolvedReferences
    from PyQt5.QtWebKitWidgets import QWebView

    USE = "UseWebView"

HTML = pkg_resources.resource_filename(
    "lcmap_tap", "/".join(("MapCanvas", USE, "index.html"))
)

log.info("PyQt version=%s", PYQT_VERSION_STR)
log.info("Qt Web Map using %s", USE)

sys.excepthook = exc_handler


class Backend(QObject):
    """
    Only used with QWebEngineView
    """

    pointChanged = pyqtSignal(float, float)

    @pyqtSlot(float, float)
    def pointClicked(self, x, y):
        """
        Capture the point clicked on the map and send
        to a backend function for display on the bottom of the window.
        """
        self.pointChanged.emit(x, y)


class MapCanvas(QWidget):
    """
    Locator map class for displaying the html/javascript map in a window.
    """

    def __init__(self, gui, parent=None):
        super(MapCanvas, self).__init__(parent)

        icon = QIcon(
            QPixmap(
                pkg_resources.resource_filename(
                    "lcmap_tap", "/".join(("Auxiliary", "icon.PNG"))
                )
            )
        )

        # Ensure the tile overlay file exists
        geojson.write_tile_overlay(grid="cu", dataset="ard")

        self.setWindowIcon(icon)

        self.setWindowTitle("Locator Map")

        self.gui = gui

        self.setMinimumSize(400, 400)

        self.text = QLabel()

        self.text.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.file = QDir.current().absoluteFilePath(HTML)

        if USE == "UseWebEngineView":
            self.map_view = QWebEngineView()

            self.backend = Backend(self)

            self.backend.pointChanged.connect(self.onPointChanged)

            self.channel = QWebChannel(self)

            self.channel.registerObject("backend", self.backend)

            self.map_view.page().setWebChannel(self.channel)

        else:
            self.map_view = QWebView()

            self.map_view.page().mainFrame().addToJavaScriptWindowObject(
                "MapCanvas", self
            )

        self.map_view.load(QUrl.fromLocalFile(self.file))

        self.layout = QVBoxLayout(self)

        self.layout.addWidget(self.map_view)

        self.layout.addWidget(self.text)

    @pyqtSlot(float, float)
    def onPointChanged(self, lat, lng):
        """
        Retrieve the coordinate values in decimal degrees from the leaflet map

        Note: This should work for either usage type of PyQt(WebView and WebEngineView)

        Args:
            lat: Latitude of mouse-click
            lng: Longitude of mouse-click

        Returns:
            None

        """
        coords = GeoInfo.get_geocoordinate(xstring=str(lng), ystring=str(lat))

        xy = GeoInfo.unit_conversion(coord=coords, src="lat/long", dest="meters")

        h, v = GeoInfo.get_hv(xy.x, xy.y)

        tile = "h{:02}v{:02}".format(h, v)

        log.info("New point selected from locator map: %s", str(coords))

        # If necessary, convert to meters before updating the coordinate text on the GUI
        if UNITS[self.gui.selected_units]["unit"] == "meters":
            coords = GeoInfo.unit_conversion(coords, src="lat/long", dest="meters")

            coords = GeoInfo.get_geocoordinate(str(int(coords.x)), str(int(coords.y)))

        # Update the X and Y coordinates in the GUI with the new point
        self.gui.ui.LineEdit_x1.setText(str(coords.x))

        self.gui.ui.LineEdit_y1.setText(str(coords.y))

        self.gui.check_values()

        # Clear the list of previously clicked ARD observations
        # because they can't be referenced in the new time-series
        self.gui.ui.ListWidget_selected.clear()

        # Display the coordinate in the QLabel window below the map
        self.text.setText(
            f"SELECTED - Tile {tile} | Lat/Lng {lat}, {lng} | Meters XY {int(xy.x)}, {int(xy.y)}"
        )

        return None
