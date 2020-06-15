"""NQontrol UI: Servo Widget."""
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

from nqontrol.gui import widgets
from nqontrol.gui.dependencies import app

from . import _callbacks


class ServoWidget(widgets.NQWidget):
    """Servo Section"""

    def __init__(self, servoNumber):
        self._servoNumber = servoNumber

    def setCallbacks(self):
        """Initialize all callbacks for the given element."""
        app.callback(
            Output(f"servoName_{self._servoNumber}", "children"),
            [Input(f"servoNameInput_{self._servoNumber}", "n_submit")],
            [State(f"servoNameInput_{self._servoNumber}", "value")],
        )(self._servoNameCallback)
        widgets.servo_section.ServoSwitchesWidget(self._servoNumber).setCallbacks()
        widgets.servo_section.AutoLockWidget(self._servoNumber).setCallbacks()

    @property
    def layout(self):
        """Return the elements' structure to be passed to a Dash style layout, usually with html.Div() as a top level container. For additional information read the Dash documentation at https://dash.plot.ly/.

        Returns
        -------
        html.Div
            The html/dash layout.

        """
        return html.Details(
            children=[
                html.Summary(
                    children=[
                        html.Span(
                            [_callbacks.getServoName(self._servoNumber)],
                            id=f"servoName_{self._servoNumber}",
                            style={"width": "50%"},
                        )
                    ],
                    className="col-12 d-flex",
                ),
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                # Servo controls, including Input, Offset, Gain, Filters, Output
                                widgets.servo_section.ServoSwitchesWidget(
                                    self._servoNumber
                                ).layout,
                                html.Div(
                                    children=[
                                        html.Div(
                                            [
                                                widgets.servo_section.AutoLockWidget(
                                                    self._servoNumber
                                                ).layout
                                            ],
                                            className="row m-0 p-0",
                                        ),
                                        html.Div(
                                            children=[
                                                html.P(
                                                    "Name", className="col-auto mb-0"
                                                ),
                                                html.Div(
                                                    children=[
                                                        dcc.Input(
                                                            id=f"servoNameInput_{self._servoNumber}",
                                                            className="form-control",
                                                        )
                                                    ],
                                                    className="col col-sm-4 col-md-2",
                                                ),
                                            ],
                                            className="row m-0 pt-1 justify-content-end align-self-end",
                                        ),
                                    ],
                                    className="col-12 col-xl-6 p-0",
                                ),
                            ],
                            className="row",
                        )
                    ],
                    className="col-12",
                ),
            ],
            className="row p-0 justify-content-start align-items-center",  # each html.Detail is a bootstrap row
            style={
                "margin": ".1vh .5vh",
                "border": ".5px solid #4C78A8",
                "border-radius": "4.5px",
            },
        )

    # Callback for assigning a name to the individual servos
    def _servoNameCallback(self, submit, name):
        return _callbacks.callServoName(self._servoNumber, submit, name)
