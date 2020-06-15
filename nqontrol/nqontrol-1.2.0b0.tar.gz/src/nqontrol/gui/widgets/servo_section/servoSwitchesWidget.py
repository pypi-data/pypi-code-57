"""NQontrol UI: Servo Switches Widget."""
# -*- coding: utf-8 -*-
# pylint: disable=duplicate-code
# ----------------------------------------------------------------------------------------
# For documentation please read the comments. For information about Dash and Plotly go to:
#
# https://dash.plot.ly/
# ----------------------------------------------------------------------------------------

import dash_core_components as dcc
import dash_html_components as html
from dash import callback_context
from dash.dependencies import Input, Output

from nqontrol.gui.dependencies import app
from nqontrol.gui.widgets import NQWidget

from . import _callbacks


class ServoSwitchesWidget(NQWidget):
    """Servo Section"""

    def __init__(self, servoNumber):
        self._servoNumber = servoNumber

    @property
    def layout(self):
        """Return the elements' structure to be passed to a Dash style layout, usually with html.Div() as a top level container. For additional information read the Dash documentation at https://dash.plot.ly/.

        Returns
        -------
        html.Div
            The html/dash layout.

        """
        return html.Div(
            children=[
                html.Div(
                    [
                        # Input Section
                        html.Div(
                            [
                                html.H3("Filter Input", className="w-100 mt-0 pl-0"),
                                dcc.Checklist(
                                    options=[
                                        {"label": "Enable Input", "value": "input"},
                                        {"label": "Offset", "value": "offset"},
                                    ],
                                    value=_callbacks.getInputStates(self._servoNumber),
                                    id=f"inputSectionCheck_{self._servoNumber}",
                                    className="w-100 pl-0",
                                    inputClassName="form-check-input",
                                    labelClassName="form-check",
                                ),
                                html.P(
                                    "Input sensitivity (Limit: (V), Mode: )",
                                    className="w-100 mb-0",
                                    id=f"input_sens_label_{self._servoNumber}",
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dcc.Dropdown(
                                                    options=[
                                                        {"label": i, "value": i}
                                                        for i in range(4)
                                                    ],
                                                    value=_callbacks.getInputSensitivity(
                                                        self._servoNumber
                                                    ),
                                                    clearable=False,
                                                    id=f"input_sensitivity_dropdown_{self._servoNumber}",
                                                )
                                            ],
                                            className="col-12 align-self-center",
                                        )
                                    ],
                                    className="row",
                                ),
                            ],
                            className="col-3",
                        ),
                        # Offset and Gain, also part of the input
                        html.Div(
                            children=[
                                html.P(
                                    "Offset", id=f"offset_label_{self._servoNumber}"
                                ),
                                dcc.Input(
                                    placeholder="-10 bis 10V",
                                    value=_callbacks.getOffset(self._servoNumber),
                                    id=f"offset_{self._servoNumber}",
                                    className="form-control",
                                ),
                                # Gain
                                html.P("Gain", id=f"gain_label_{self._servoNumber}"),
                                dcc.Input(
                                    placeholder="Enter gain...",
                                    value=_callbacks.getGain(self._servoNumber),
                                    id=f"gain_{self._servoNumber}",
                                    className="form-control",
                                ),
                                # Store component in order to determine how callGain was triggered. Saves previous timestamp
                                dcc.Store(id=f"gainStore_{self._servoNumber}"),
                                # Storage component to use as input channels checklist target in callbacks
                                dcc.Store(
                                    id=f"channelChecklistStorage_{self._servoNumber}"
                                ),
                            ],
                            className="col-3",
                        ),
                        # Filter section of the servo controls
                        html.Div(
                            children=[
                                html.H3("Filters", className="w-100 mt-0 pl-0"),
                                # Filter checklist
                                dcc.Checklist(
                                    options=_callbacks.getFilterLabels(
                                        self._servoNumber
                                    ),
                                    value=_callbacks.getActiveFilters(
                                        self._servoNumber
                                    ),
                                    id=f"filterSectionCheck_{self._servoNumber}",
                                    className="w-100",
                                    inputClassName="form-check-input",
                                    labelClassName="form-check",
                                ),
                                # Storage component to use as target for filter checklist target in callback
                                dcc.Store(
                                    id=f"filterChecklistStorage_{self._servoNumber}"
                                ),
                            ],
                            className="col-3",
                        ),
                        # Output section of the servo controls
                        html.Div(
                            [
                                html.H3("Output", className="w-100 mt-0 pl-0"),
                                # Channel Checklist for 'Aux' and 'Output'
                                dcc.Checklist(
                                    options=[
                                        {"label": "Enable Output", "value": "output"},
                                        {"label": "Aux to Out", "value": "aux"},
                                    ],
                                    value=_callbacks.getOutputStates(self._servoNumber),
                                    id=f"outputSectionCheck_{self._servoNumber}",
                                    className="w-100 pl-0",
                                    inputClassName="form-check-input",
                                    labelClassName="form-check",
                                ),
                                html.P(
                                    "Aux sensitivity (Limit: (V), Mode: )",
                                    className="w-100 mb-0",
                                    id=f"aux_sens_label_{self._servoNumber}",
                                ),
                                # The Aux sensitivity dropdown control
                                html.Div(
                                    # For some input components it helps to wrap them in an extra div and set that Div's properties instead, since the Dropdown will align with it. Therefore the nested row/col wrapper
                                    [
                                        html.Div(
                                            [
                                                dcc.Dropdown(
                                                    options=[
                                                        {"label": i, "value": i}
                                                        for i in range(4)
                                                    ],
                                                    value=_callbacks.getAuxSensitivity(
                                                        self._servoNumber
                                                    ),
                                                    clearable=False,
                                                    id=f"aux_sensitivity_dropdown_{self._servoNumber}",
                                                )
                                            ],
                                            className="col-12 align-self-center",
                                        )
                                    ],
                                    className="row",
                                ),
                            ],
                            className="col-3",
                        ),
                    ],
                    className="row",
                )
            ],
            className="col-12 col-xl-6 d-inline",
        )

    def setCallbacks(self):
        """Initialize all callbacks for the given element."""

        # Offset callback
        offset = f"offset_{self._servoNumber}"
        sensitivityDropdown = f"input_sensitivity_dropdown_{self._servoNumber}"
        app.callback(
            Output(f"offset_label_{self._servoNumber}", "children"),
            [Input(offset, "value"), Input(sensitivityDropdown, "value")],
        )(self._offsetCallback)

        # Gain callback
        gain = f"gain_{self._servoNumber}"
        gainStore = f"gainStore_{self._servoNumber}"
        app.callback(
            Output(f"gain_label_{self._servoNumber}", "children"),
            [Input(gain, "value"), Input(gainStore, "data")],
        )(self._gainCallback)

        # Servo channels callback
        inputCheck = f"inputSectionCheck_{self._servoNumber}"
        filterCheck = f"filterSectionCheck_{self._servoNumber}"
        outputCheck = f"outputSectionCheck_{self._servoNumber}"

        app.callback(
            Output(f"channelChecklistStorage_{self._servoNumber}", "data"),
            [Input(inputCheck, "value"), Input(outputCheck, "value")],
        )(self._channelCallback)

        app.callback(
            Output(f"filterChecklistStorage_{self._servoNumber}", "data"),
            [Input(filterCheck, "value")],
        )(self._filterCallback)

        # Input sensitivity callback initialization
        # corresponding html ids
        label = f"input_sens_label_{self._servoNumber}"
        dropdown = f"input_sensitivity_dropdown_{self._servoNumber}"
        # callback definition
        app.callback(Output(label, "children"), [Input(dropdown, "value")])(
            self._inputSensitivityCallback
        )

        # Aux sensitivity callback init
        # corresponding html ids
        label = f"aux_sens_label_{self._servoNumber}"
        dropdown = f"aux_sensitivity_dropdown_{self._servoNumber}"
        # callback definition
        app.callback(Output(label, "children"), [Input(dropdown, "value")])(
            self._auxSensitivityCallback
        )

    # Callback for the Offset Input Field
    def _offsetCallback(self, value, _dropdownTrigger):
        return _callbacks.callOffset(self._servoNumber, value)

    # Callback for the Gain Input Field
    def _gainCallback(self, value, _sosTrigger):
        context = callback_context
        return _callbacks.callGain(context, self._servoNumber, value)

    # Callback for the input channels checklist
    def _channelCallback(self, inputValues, inputValues2):
        return _callbacks.callServoChannels(
            self._servoNumber, inputValues + inputValues2
        )

    # filter switches checklist
    def _filterCallback(self, value):
        return _callbacks.callToggleServoFilters(self._servoNumber, value)

    # aux sensitivity dropdown
    def _auxSensitivityCallback(self, selected):
        return _callbacks.callAuxSensitivity(selected, self._servoNumber)

    def _inputSensitivityCallback(self, selected):
        return _callbacks.callInputSensitivity(selected, self._servoNumber)
