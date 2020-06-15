"""NQontrol UI: In-browser `oscilloscope`"""
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
from nqontrol.gui.widgets.monitor_section import adwinMonitorsWidget

from . import _callbacks

layout = html.Div(
    # Monitoring Graph placeholder
    children=[
        # Monitor headline
        html.H2("Monitor"),
        # Servo target RadioItems
        html.Div(
            children=[
                html.Div("Servo", className="col-2 align-self-center"),
                dcc.RadioItems(
                    options=[
                        {"label": i, "value": i}
                        for i in range(1, settings.NUMBER_OF_SERVOS + 1)
                    ],
                    value=1,
                    id="monitorTarget",
                    className="col-10",
                    persistence=True,
                    inputClassName="form-check-input",
                    labelClassName="form-check form-check-inline",
                    inputStyle={"color": "#4C78A8"},
                ),
            ],
            className="row justify-content-start align-items-center",
        ),
        # Realtime graph
        html.Div(
            children=[
                html.Div(
                    children=[dcc.Graph(id="monitor_graph", animate=False)],
                    className="col-12 align-self-end",
                )
            ],
            className="row",
        ),
        # Visible channels checklist
        html.Div(
            children=[
                html.Div(["Channels: "], className="col-auto d-inline"),
                dcc.Checklist(
                    options=[
                        {"label": "Input", "value": "input"},
                        {"label": "Aux", "value": "aux"},
                        {"label": "Output", "value": "output"},
                    ],
                    persistence=True,
                    value=["input"],
                    inputClassName="form-check-input",
                    labelClassName="form-check form-check-inline",
                    id="monitor_check",
                ),
                # Callback output
                dcc.Store(id="checklistTarget"),
            ],
            className="row justify-content-start align-items-center",
        ),
        # Update timer
        dcc.Interval(id="update", interval=1000, n_intervals=0),
        # Physical ADwin monitor channels
        adwinMonitorsWidget.layout,
    ],
    className="col-12 col-lg-6",
)


def setCallbacks():
    """Initialize all callbacks for the given element."""

    # callbacks of the component which sets the ADwins internal monitoring Channels
    adwinMonitorsWidget.setCallbacks()

    # relevant HTML Ids
    servoInput = "monitorTarget"
    graph = "monitor_graph"
    checkList = "monitor_check"
    update = "update"

    app.callback(
        Output(graph, "figure"),
        [Input(update, "n_intervals"), Input(servoInput, "value")],
        [State(servoInput, "value"), State(checkList, "value")],
    )(_monitorCallback)

    app.callback(
        Output("checklistTarget", "data"),
        [Input(checkList, "value")],
        [State(servoInput, "value")],
    )(_channelCheckCallback)


# Callback to the monitor
def _monitorCallback(_intervals, _inputNum, servoNumber, checklistState):
    return _callbacks.callMonitorUpdate(servoNumber, checklistState)


# Callback for checklist of visible monitor channels
def _channelCheckCallback(visibleChannels, servoNumber):
    return _callbacks.callMonitorUpdateChannels(servoNumber, visibleChannels)
