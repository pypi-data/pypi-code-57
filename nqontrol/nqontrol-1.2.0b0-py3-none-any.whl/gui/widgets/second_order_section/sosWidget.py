"""NQontrol UI: Second order section (SOS) Widget. Wrapper for header section widget (containing filter widgets) and the plot of the servo design section."""
# -*- coding: utf-8 -*-
# pylint: disable=duplicate-code
# ----------------------------------------------------------------------------------------
# For documentation please read the comments. For information about Dash and Plotly go to:
#
# https://dash.plot.ly/
# ----------------------------------------------------------------------------------------
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from nqontrol.gui.dependencies import app
from nqontrol.gui.widgets.second_order_section import FilterWidget, sosHeaderWidget

from . import _callbacks

_uiFilters = [
    FilterWidget(filterIndex, "sos_servo_apply_target")
    for filterIndex in range(_callbacks.getMaxFilters())
]

layout = html.Div(
    children=[
        html.H2("Servo Design"),
        html.Div([sosHeaderWidget.layout], className="row"),
        # now all the filter rows
        html.Div(
            html.Div([uiFilter.layout for uiFilter in _uiFilters], className="col-12"),
            className="row",
        ),
        html.Div(
            children=[
                html.Div(
                    ["Plots the Second Order Section implemented by the Servo Design."],
                    className="col-12",
                ),
                html.Div(
                    children=[dcc.Graph(id="sdGraph", animate=False)],
                    className="col-12",
                ),
            ],
            className="row",
        ),
    ],
    className="col-12 col-lg-6",
)


def setCallbacks():
    """Initialize all callbacks for the given element."""
    for filter_ in _uiFilters:
        filter_.setCallbacks()
    sosHeaderWidget.setCallbacks()

    graph = "sdGraph"
    uploadOutput = "uploadOutput"
    inputs = [Input(uploadOutput, "data")]

    for i in range(_callbacks.getMaxFilters()):
        inputs.append(Input(f"filter_update_{i}", "data"))

    inputs.append(Input("sos_gain_label", "children"))

    app.callback(Output(graph, "figure"), inputs)(_graphCallback)


# callback for updating the servo design plot
# *args will just be all the other inputs (one for each filter parameter field, etc.)
def _graphCallback(_unplantTrigger, *_args):
    return _callbacks.callPlotServoDesign()
