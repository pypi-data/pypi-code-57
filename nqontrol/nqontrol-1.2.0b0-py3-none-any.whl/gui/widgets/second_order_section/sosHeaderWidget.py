"""NQontrol UI: Second order section (SOS) Widget. Contains UI elements for designing the filter section for servos. Contains 5 `widgets.FilterWidget` widgets to assign different filters. Also containts an upload for a plant and displays a bode plot of the current filters."""
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

layout = html.Div(
    id="sos_unit",
    children=[
        html.Div(
            children=[
                # Servo number target
                html.Div(
                    children=[
                        dcc.Input(
                            type="number",
                            min=1,
                            max=settings.NUMBER_OF_SERVOS,
                            value=1,
                            persistence=True,
                            id="sos_servo_apply_target",
                            className="form-control",
                        )
                    ],
                    className="col-3 col-sm-2 pr-0",
                ),
                # Upload field
                html.Div(
                    [
                        dcc.Upload(
                            children=html.Div("Upload plant."),
                            id="plantUpload",
                            style={
                                "height": "2.25rem",
                                "line-height": "2.25rem",
                                "borderWidth": "1px",
                                "borderStyle": "dashed",
                                "borderRadius": "5px",
                                "textAlign": "center",
                                "margin": "10px 0",
                            },
                            className="wl-100",
                        )
                    ],
                    className="col-9 col-sm-4",
                ),
                # Unplant button
                html.Div(
                    [
                        html.Button(
                            "Unplant",
                            id="sosDelPlant",
                            className="btn btn-primary w-100",
                        )
                    ],
                    className="col-6 ml-sm-auto col-sm-2 col-lg-auto pl-sm-0",
                ),
                # Apply button
                html.Div(
                    [
                        html.Button(
                            "Apply",
                            id="sos_apply_button",
                            className="btn btn-primary w-100",
                        )
                    ],
                    className="col-6 col-sm-2 col-lg-auto pl-sm-0",
                ),
                dcc.Store(id="sosSwitchStorage"),
            ],
            className="row align-items-center",
        ),
        html.Div(
            children=[
                # Gain label
                html.Div(["Gain"], id="sos_gain_label", className="col-3 col-sm-2"),
                # Gain input field
                html.Div(
                    [
                        dcc.Input(
                            placeholder="Enter gain...",
                            value=_callbacks.getSDGain(),
                            id="sos_gain",
                            className="form-control w-100",
                        )
                    ],
                    className=" col-3 col-sm-4 pl-0 pl-sm-3",
                ),
                # Plant button timestamp storage to determine how _callbacks.callPlantParse was triggered
                dcc.Store(id="uploadOutput"),
            ],
            className="row align-items-center",
        ),
    ],
    className="col-12",
)


def setCallbacks():
    """Initialize all callbacks for the given element."""

    app.callback(
        Output("sosSwitchStorage", "data"),
        [Input("sos_apply_button", "n_clicks")],
        [State("sos_servo_apply_target", "value")],
    )(_applyServoCallback)

    for i in range(1, settings.NUMBER_OF_SERVOS + 1):
        # this here is part of the Servo section of the UI!!!
        sectionCheck = f"filterSectionCheck_{i}"
        # this is a component from the servo section
        # used to trigger an update of the gain label when a servo design is applied
        gainStore = f"gainStore_{i}"

        # also note that the callback below is part of a chain!
        # first is the callback above, which then triggers this callback

        # Apply values and labels
        app.callback(
            [
                Output(sectionCheck, "value"),
                Output(sectionCheck, "options"),
                Output(gainStore, "data"),
            ],
            [Input("sosSwitchStorage", "data")],
            [
                State("sos_servo_apply_target", "value"),
                State("sos_apply_button", "n_clicks"),
            ],
        )(_applyFiltersCallback(i))

    delPlant = "sosDelPlant"
    plantUpload = "plantUpload"

    app.callback(
        Output("uploadOutput", "data"),
        [
            Input(plantUpload, "filename"),
            Input(plantUpload, "contents"),
            Input(delPlant, "n_clicks"),
        ],
        [State(delPlant, "n_clicks_timestamp"), State("uploadOutput", "data")],
    )(_uploadCallback)

    # Gain callback
    gain = "sos_gain"
    app.callback(Output("sos_gain_label", "children"), [Input(gain, "value")])(
        _sosGainCallback
    )


#######################################################################################################
# All callbacks need to return a function to be bound to that callback, defined below
#######################################################################################################


def _uploadCallback(filename, contents, n_clicks, timestamp, timestamp_old):
    return _callbacks.callPlantParse(
        filename, contents, n_clicks, timestamp, timestamp_old
    )


def _applyServoCallback(n_clicks, servoNumber):
    return _callbacks.callApplyServoDesign(servoNumber, n_clicks)


# Callback for the SOS Gain Input Field
def _sosGainCallback(inputValue):
    # gain gets applied
    return _callbacks.callServoDesignGain(inputValue)


# unified callback for filter values and labels
def _applyFiltersCallback(servoNumber):
    def callback(_hiddenInput, applyNumber, n_clicks):
        return _callbacks.callApplyFiltersToServo(applyNumber, servoNumber, n_clicks)

    return callback
