"""NQontrol UI: Filter Widget."""
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

from nqontrol.gui.dependencies import app
from nqontrol.gui.widgets import NQWidget

from . import _callbacks


class FilterWidget(NQWidget):
    """Widget for a single filter of the SecondOrderSection of the UI. Basically a row in the layout, containing inputs for filter type, main and secondary parameter, as well as a description label and a checkbox to set filter state."""

    def __init__(self, filterIndex, parentServoTarget="sos_servo"):
        self._filterIndex = filterIndex
        self._parentServoTarget = parentServoTarget

    @property
    def layout(self):
        """Return the elements' structure to be passed to a Dash style layout, usually with html.Div() as a top level container. For additional information read the Dash documentation at https://dash.plot.ly/.

        Returns
        -------
        html.Div
            The html/dash layout.

        """
        # Setting up dropdown options
        options = [{"label": "None", "value": ""}]
        for filter_ in _callbacks.getFilterOptions():
            options.append({"label": filter_.__name__, "value": filter_.__name__})
        return html.Div(
            children=[
                # Active checkbox
                html.Div(
                    [
                        dcc.Checklist(
                            id=f"filter_active_{self._filterIndex}",
                            options=[{"label": "", "value": self._filterIndex}],
                            value=_callbacks.getFilterEnabled(self._filterIndex),
                            inputClassName="form-check-input",
                            labelClassName="form-check form-check-inline",
                        )
                    ],
                    className="col-2 col-sm-auto",
                ),
                # Dropdown filter type selection
                html.Div(
                    children=[
                        dcc.Dropdown(
                            options=options,
                            id=f"filter_unit_dropdown_{self._filterIndex}",
                            value=_callbacks.getFilterDropdown(self._filterIndex),
                            clearable=False,
                        )
                    ],
                    className="col-10 col-sm-3 col-lg-3",
                ),
                # Main filter parameter
                html.Div(
                    children=[
                        dcc.Input(
                            id=f"filter_frequency_input_{self._filterIndex}",
                            placeholder="fc",
                            className="form-control",
                            value=_callbacks.getFilterMainPar(self._filterIndex),
                        )
                    ],
                    className="col-5 col-sm pl-sm-0 pr-0 pr-sm-3 ml-auto ml-sm-0",
                ),
                # Secondary filter parameter (optional)
                html.Div(
                    children=[
                        dcc.Input(
                            id=f"filter_optional_input_{self._filterIndex}",
                            placeholder="fcslope",
                            className="form-control",
                            value=_callbacks.getFilterSecondPar(self._filterIndex),
                        )
                    ],
                    className="col-5 col-sm pl-0",
                ),
                # Description
                html.Div(
                    [_callbacks.getFilterDescription(self._filterIndex)],
                    id=f"filter_description_{self._filterIndex}",
                    className="col-10 col-sm-5 col-lg-4 filter-font ml-auto ml-sm-0 pl-sm-0",
                ),
                dcc.Store(id=f"filter_update_{self._filterIndex}"),
            ],
            className="row justify-content-start align-items-center",
        )

    def setCallbacks(self):
        """Initialize all callbacks for the given element."""
        # all of these are components of this widget
        dropdown = f"filter_unit_dropdown_{self._filterIndex}"
        mainInput = f"filter_frequency_input_{self._filterIndex}"
        secInput = f"filter_optional_input_{self._filterIndex}"
        description = f"filter_description_{self._filterIndex}"
        updateDiv = f"filter_update_{self._filterIndex}"
        activeCheck = f"filter_active_{self._filterIndex}"

        # Parameter/filter callback
        app.callback(
            Output(updateDiv, "data"),
            [
                Input(dropdown, "value"),
                Input(mainInput, "value"),
                Input(secInput, "value"),
                Input(self._parentServoTarget, "value"),
                Input("plantUpload", "filename"),
                Input(activeCheck, "value"),
            ],
            [
                State(dropdown, "value"),
                State(mainInput, "value"),
                State(secInput, "value"),
                State(activeCheck, "value"),
            ],
        )(self._filterFieldCallback)

        # Visibility callbacks
        app.callback(
            [Output(elem, "style") for elem in [mainInput, secInput, description]],
            [Input(dropdown, "value")],
        )(self._visibilityCallback)

        # Description callback
        app.callback(
            Output(description, "children"),
            [
                Input(dropdown, "value"),
                Input(mainInput, "value"),
                Input(secInput, "value"),
            ],
        )(self._descriptionCallback)

    #######################################################################################################
    # All callbacks need to return a function to be bound to that callback, defined below
    #######################################################################################################

    # Callback for visibility of filter input fields
    def _filterFieldCallback(
        self,  # pylint: disable=too-many-arguments
        _dropdownInput,
        _mainInput,
        _secInput,
        _servoTarget,
        _plant,
        _active,
        dropdown,
        main,
        sec,
        activeState,
    ):
        return _callbacks.callFilterField(
            dropdown, main, sec, activeState, self._filterIndex
        )

    def _descriptionCallback(self, dropdown, main, sec):
        return _callbacks.callFilterDescription(dropdown, main, sec, self._filterIndex)

    @classmethod
    def _visibilityCallback(cls, dropdownInput):
        return _callbacks.callFilterVisible(dropdownInput)
