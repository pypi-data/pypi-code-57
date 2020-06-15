"""NQontrol UI: Monitor Channel Widget for assignment of physical monitor outputs on ADwin device"""
# -*- coding: utf-8 -*-
# pylint: disable=duplicate-code
# ----------------------------------------------------------------------------------------
# For documentation please read the comments. For information about Dash and Plotly go to:
#
# https://dash.plot.ly/
# ----------------------------------------------------------------------------------------
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from nqontrol.general import settings
from nqontrol.gui.dependencies import app

from . import _callbacks

layout = html.Details(  # pylint: disable=attribute-defined-outside-init
    children=[
        html.Summary(["ADwin Monitor Channels"], className="col-12"),
        html.P(
            "Send a servo channel to one of the ADwin's physical monitor outputs.",
            className="col",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        # Channel index label
                        html.P(f"{i}", className="col-auto align-self-center m-0"),
                        # Servo target dropdown
                        html.Div(
                            children=[
                                dcc.Dropdown(
                                    options=[
                                        {"label": f"Servo {j}", "value": j}
                                        for j in range(1, settings.NUMBER_OF_SERVOS + 1)
                                    ],
                                    value=_callbacks.getMonitorsServo(i),
                                    placeholder="Servo channel",
                                    id=f"adwin_monitor_channel_target_{i}",
                                )
                            ],
                            className="col",
                        ),
                        # Channel card dropdown
                        html.Div(
                            children=[
                                dcc.Dropdown(
                                    options=[
                                        {"label": "Input", "value": "input"},
                                        {"label": "Aux", "value": "aux"},
                                        {"label": "Output", "value": "output"},
                                        {"label": "TTL", "value": "ttl"},
                                    ],
                                    value=_callbacks.getMonitorsCard(i),
                                    placeholder="Card",
                                    id=f"adwin_monitor_channel_card_{i}",
                                )
                            ],
                            className="col",
                        ),
                        dcc.Store(id=f"store_adwin_monitor_channel_{i}"),
                    ],
                    className="row",
                )
                for i in range(1, settings.NUMBER_OF_MONITORS + 1)
            ],
            className="col-12",
        ),
    ],
    className="row p-0",  # The detail itself is a row
    style={
        "margin": ".1vh .5vh",
        "border": ".5px solid #4C78A8",
        "border-radius": "4.5px",
    },
)


# The channel parameter is the monitor channel corresponding with the hardware channel on the device
# Here, we want to use this kind of syntax, because we declare multiple callbacks in a loop (see setCallbacks())
def __setADwinMonitorCallback(channel):
    # inp1 and inp2 are only used as triggers, servo and card refer to the servo that's being assigned to the channel and the monitoring data (input, output, aux, ttl)
    def callback(_inp1, _inp2, servo, card):
        return _callbacks.callADwinMonitor(channel, servo, card)

    return callback


def setCallbacks():
    """Initialize all callbacks for the given element."""

    for i in range(1, settings.NUMBER_OF_MONITORS + 1):
        # setting the function for each individual i
        # all HTML IDs relevant to the callback
        servoDropdown = f"adwin_monitor_channel_target_{i}"
        cardDropdown = f"adwin_monitor_channel_card_{i}"
        # stores the information, mainly Output dummy
        store = f"store_adwin_monitor_channel_{i}"
        # configuring the callback
        app.callback(
            Output(store, "data"),
            [Input(servoDropdown, "value"), Input(cardDropdown, "value")],
            [State(servoDropdown, "value"), State(cardDropdown, "value")],
        )(__setADwinMonitorCallback(i))
