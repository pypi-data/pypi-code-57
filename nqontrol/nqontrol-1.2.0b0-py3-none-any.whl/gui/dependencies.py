"""App dependencies"""
import dash
from plotly.express import colors as clrs

from nqontrol import ServoDevice
from nqontrol.general import settings

THEME = clrs.qualitative.T10
THEME2 = clrs.qualitative.G10

DEVICE = ServoDevice(
    deviceNumber=settings.DEVICE_NUM, readFromFile=settings.SETTINGS_FILE
)

app = dash.Dash(__name__)
