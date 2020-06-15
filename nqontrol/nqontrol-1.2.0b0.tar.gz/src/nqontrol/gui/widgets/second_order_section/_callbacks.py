import base64
import datetime
import logging as log

import plotly.graph_objs as go
from dash.exceptions import PreventUpdate
from fastnumbers import fast_real
from openqlab import io
from openqlab.analysis.servo_design import Filter
from plotly import subplots

from nqontrol.general import settings
from nqontrol.gui.dependencies import DEVICE, THEME, THEME2

############################################################
#################### Filter Widget #########################
############################################################


#################### Getters ###############################


def getFilterOptions():
    """Return all possible filter types defined by the :obj:`ServoDesign` library of `openqlab`.
    Used to automate UI lists of possible filter types.

    Returns
    -------
    :obj:`list`
        List containing all possible filter types as Strings.

    """
    return Filter.__subclasses__()


def getFilterEnabled(filterIndex):
    """Load state of an individual filter.

    The UI in the second order section requires individual checkboxes, thus,
    filter states have to be loaded individually.

    Returns a list which is either empty or contains the filter index,
    signifying whether it is active or not (Checkbox UI elements work only with lists).
    The default state for a None filter however is active.
    So the only case in which the checkbox is set to inactive if an inactive filter is specified.

    This loads a state for the Second Order Section of the UI, not the servo sections!
    The getters for the servo section are :obj:`controller.getActiveFilters()`
    and :obj:`controller.getFiltersEnabled()`.

    Parameters
    ----------
    filterIndex : :obj:`int`
        filter index on :obj:`openqlab.analysis.servo_design.ServoDesign`

    Returns
    -------
    :obj:`list`
        List containing the filter index or empty list.

    """

    fil = DEVICE.servoDesign.get(filterIndex)
    if fil is not None:
        if not fil.enabled:
            return []
    return [filterIndex]


def getFilterDropdown(filterIndex):
    """Initialize the dropdown state of the filter UI for given index.
    If empty return None. Concerns the Second Order Section of the UI,
    not the servo's filter section!

    Parameters
    ----------
    filterIndex : :obj:`int`
        filter index on :obj:`openqlab.analysis.servo_design.ServoDesign`

    Returns
    -------
    :obj:`String`
        Name of the active filter class. None if inactive.

    """
    fil = DEVICE.servoDesign.get(filterIndex)
    if fil is not None:
        return fil.__class__.__name__
    return ""


def getFilterMainPar(filterIndex):
    """Initialize the main parameter of the filter UI for given index.
    If no filter exists at given index return None.
    Concerns the Second Order Section of the UI.

    Parameters
    ----------
    servoNumber : :obj:`int`
        Servo index :obj:`servo.channel`

    Returns
    -------
    :obj:`float`
        Parameter as a float or None.

    """
    fil = DEVICE.servoDesign.get(filterIndex)
    if fil is not None:
        return fil.corner_frequency
    return ""


def getFilterSecondPar(filterIndex):
    """Initialize the second parameter of the filter UI for given index.
    If no filter exists at given index return None.
    Concerns the Second Order Section of the UI.

    Parameters
    ----------
    servoNumber : :obj:`int`
        Servo index :obj:`servo.channel`

    Returns
    -------
    :obj:`float`
        Secondary parameter as float or None.

    """
    fil = DEVICE.servoDesign.get(filterIndex)
    if fil is not None:
        return fil.second_parameter
    return ""


def getFilterDescription(filterIndex):
    """Initialize the description of the filter UI for given index.
    If no filter exists at given index return None.
    Concerns the Second Order Section of the UI.

    Parameters
    ----------
    servoNumber : :obj:`int`
        Servo index :obj:`servo.channel`

    Returns
    -------
    :obj:`String`
        Filter description as a string or None.

    """
    fil = DEVICE.servoDesign.get(filterIndex)
    if fil is not None:
        return fil.description
    return None


#################### Callbacks##############################


def callFilterDescription(  # pylint: disable=unused-argument,too-many-branches
    dropdown, main, sec, filterIndex
):
    """Updates the filter description labels in the Second Order Section of the UI
    when the dropdown selection (filter type) changes.

    Parameters
    ----------
    dropdown : :obj:`String`
        Value passed by the dropdown. Filter type as a string.
    main : :obj:`String`
        Main filter parameter. Contents of the UI input as a string. None if empy.
    sec : :obj:`String`
        Secondary filter parameter. Contentes of the UI input as a string. None if empy.
    filterIndex : :obj:`int`
        Index of the filter in the :obj:`ServoDesign`.

    Returns
    -------
    :obj:`String`
        The description string if a filter type is selected or None.

    """
    if dropdown is None or dropdown == "":
        return ""
    fil = None
    for subclass in Filter.__subclasses__():
        if dropdown in subclass.__name__:
            fil = subclass
    if fil is None:
        log.warning(f"Could not find a filter with name {dropdown}.")
        raise PreventUpdate()
    s = ""
    if main is None:
        return "Main value expected."
    try:
        main = float(fast_real(main, raise_on_invalid=True))
        # Checking for secInput
    except (ValueError, TypeError):
        s = "Invalid main value."
    else:
        if sec != "" and sec is not None:
            try:
                sec = float(fast_real(sec, raise_on_invalid=True))
            except (ValueError, TypeError):
                s = "Invalid secondary value."
            else:
                try:
                    s = str(fil(main, sec).description)
                except OverflowError:
                    s = f"Overflow error, inf in human_readable."
                except ZeroDivisionError:
                    s = f"Will divide by 0 and create a black hole."
        else:
            s = str(fil(main).description)

    return s


def _handleFilter(dropdown, main, sec, active, filterIndex):
    log.warning((main, sec))
    # Determining filter type
    fil = None
    for subclass in Filter.__subclasses__():
        if subclass.__name__ == dropdown:
            fil = subclass
    if fil is None:
        log.warning(f"Could not find a filter with name {dropdown}.")
        raise PreventUpdate()
    log.info((dropdown, main, sec, active, filterIndex))
    servoDesign = DEVICE.servoDesign
    if main != "" and main is not None:
        try:
            main = float(fast_real(main, raise_on_invalid=True))
        except (ValueError, TypeError) as e:
            log.warning(f"No real number input in main field, was {main}.")
            raise PreventUpdate()
    else:
        log.warning("No main parameter.")
        raise PreventUpdate()
    if sec != "" and sec is not None:
        try:
            sec = float(fast_real(sec, raise_on_invalid=True))
            log.warning(sec)
        except (ValueError, TypeError) as e:
            log.warning(f"No real number input in secondary field, was {sec}.")
            raise PreventUpdate()
        # only add filter with second parameter if sec was set,
        # since the filters have different default values for the secondary parameter
        # and shouldnt be overwritten with None
        try:
            servoDesign.add(fil(main, sec, enabled=bool(active)), index=filterIndex)
        except ZeroDivisionError as e:
            log.warning(
                f"0 is not valid as a second parameter in this case. Encountered {e}."
            )
            raise PreventUpdate()
    else:
        # add filter with just main value
        servoDesign.add(fil(main, enabled=bool(active)), index=filterIndex)


def callFilterField(dropdown, main, sec, active, filterIndex):
    """Handle input changes for both the main and secondary parameter fields of filters in the
    Second Order Section of the UI.
    Applies the changes to :obj:`ServoDevice.servoDesign` accordingly.

    Parameters
    ----------
    dropdown : :obj:`String`
        Value passed by the dropdown. Filter type as a string.
    main : :obj:`String`
        Main filter parameter. Contents of the UI input as a string. None if empy.
    sec : :obj:`String`
        Secondary filter parameter. Contentes of the UI input as a string. None if empy.
    active : :obj:`list`
        List indicating whether a checkbox is enabled for the filter or not.
        If active contains the filter index, empty if inactive.
    filterIndex : :obj:`int`
        Index of the filter in the :obj:`ServoDesign`.

    Returns
    -------
    :obj:`String`
        Datetime string to pass to output. The output triggers a callback chain as well.

    """
    servoDesign = DEVICE.servoDesign
    if dropdown != "" and dropdown is not None:
        _handleFilter(dropdown, main, sec, active, filterIndex)
    else:
        servoDesign.remove(filterIndex)
    return str(datetime.time())


def callFilterVisible(dropdownInput):
    """Handle visibility of filter input fields and description depending on
    whether a value is selected in the dropdown. Refers to the Second Order Section of the UI.

    Parameters
    ----------
    dropdownInput : :obj:`String`
        Either filter type as a string or "".

    Returns
    -------
    :obj:`Dictionary`
        Dictionary containing CSS style information for Dash.
        Changes 'display' style of filter inputs to either 'none' or 'inline-block'.

    """
    if dropdownInput != "":
        return (
            {"display": "inline-block"},
            {"display": "inline-block"},
            {"display": "inline-block"},
        )
    return {"display": "none"}, {"display": "none"}, {"display": "none"}


############################################################
#################### SOS Header Widget######################
############################################################


#################### Getters ###############################


def getSDGain():
    """Return :obj:`ServoDevice.servoDesign.gain`,
    the gain of the :obj:`ServoDesign` associated with the device.

    Concerns the Second Order Section of the UI.

    Please note that functionality wise this equates to :obj:`servo.gain`
    if a :obj:`ServoDesign` is applied to a servo.
    The servo and ServoDesign then share a gain.
    The Second Order Section of the UI thus needs a separate input to prevent
    override to default when applying. Please read the documentation for further information.

    Parameters
    ----------

    Returns
    -------
    :obj:`float`
        Gain of the device's :obj:`ServoDesign` as a float.

    """
    servoDesign = DEVICE.servoDesign
    return servoDesign.gain


#################### Callbacks##############################


def callPlantParse(  # pylint: disable=unused-argument
    filename, contents, n_clicks, timestamp, timestamp_old
):
    """Handle parsing of uploaded plant for :obj:`ServoDesign` of the Second Order Section.
    Also handles 'unplanting'.
    Has to be handled by one function as both callbacks would target the same output container.

    Parameters
    ----------
    filename : :obj:`String`
        Name of the input file. Dash does not send the full path.
    contents : :obj:`String`
        Base64 encoded string of the file contents.
    n_clicks : :obj:`int`
        Number of times the 'Unplant' button has been clicked

    Returns
    -------
    :obj:`String`
        Timestamp of the last time the button was clicked.

    """
    if n_clicks is None and contents is None:
        raise PreventUpdate()
    servoDesign = DEVICE.servoDesign
    # first check if the callback has been fired by the unplant button
    if timestamp_old != timestamp:
        servoDesign.plant = None
    elif contents is not None:
        _, content_string = contents.split(",")
        decoded = base64.b64decode(content_string).decode("utf-8", "ignore")
        try:
            df = io.reads(decoded)
            servoDesign.plant = df
        except Exception as e:
            log.warning(e)
            raise PreventUpdate(str(e))
    return timestamp


def callApplyServoDesign(servoNumber, n_clicks):
    """Callback for the 'Apply'-Button in the Second Order Section of the UI.

    Parameters
    ----------
    servoNumber : :obj:`int`
        Servo index :obj:`servo.channel`
    n_clicks : :obj:`int`
        Integer indicating times the Button has been clicked.
        Used to prevent callback from firing on start-up.

    Returns
    -------
    :obj:`String`
        String description to pass on to UI label.

    """
    if n_clicks is not None:
        # transfer device servo design to individual servo
        DEVICE.servo(servoNumber).applyServoDesign(DEVICE.servoDesign)
        log.debug(f"Applying servo design on {servoNumber}.")
        return f"Applied ServoDesign on {servoNumber} after {n_clicks}."
    raise PreventUpdate()


def callApplyFiltersToServo(applyNumber, servoNumber, n_clicks):
    """Handle updating filter checklist values in the servo control section
    when 'Apply' button is pressed for the Second Order Section.

    Due to the callback mechanic, an additional parameter `applyNumber` has to be passed,
    to ensure the checklist values are only updated in the corresponding section.

    Parameters
    ----------
    applyNumber : :obj:`int`
        Parameter compared to the `servoNumber`. Only fires if they are the same.
    servoNumber : :obj:`int`
        Servo index :obj:`servo.channel`
    n_clicks : :obj:`int`
        Indicates times the button has been clicked. Used to prevent callback execution on start-up.

    Returns
    -------
    :obj:`list`
        List containing the values of all active filters for checklist UI element.
        The value corresponding to each filter is its respective index.
    :obj:`list`
        List containing the new labels of the checklist UI element.
        Each label is defined as {`label`: xxx, `value`: xxx}.
        The value will always correspond to the filter index.

    """
    if not 1 <= servoNumber <= settings.NUMBER_OF_SERVOS:
        raise IndexError(
            f"Please use a correct servo index in range 1 to {settings.NUMBER_OF_SERVOS}, was{servoNumber}."
        )
    if (applyNumber == servoNumber) and (n_clicks is not None):
        servoDesign = DEVICE.servoDesign
        values = []
        labels = []
        for i in range(servoDesign.MAX_FILTERS):
            fil = servoDesign.get(i)
            if fil is not None:
                if fil.enabled:
                    values.append(i)
                labels.append(fil.description)
            else:
                labels.append(f"Filter {i}")
        labels = [
            {"label": labels[i], "value": i} for i in range(servoDesign.MAX_FILTERS)
        ]
    else:
        raise PreventUpdate()
    return values, labels, n_clicks


def callServoDesignGain(gain):
    """Handle the dummy ServoDesign gain callback for the UI.
    The :obj:`ServoDesign` is associated with the :obj:`nqontrol.ServoDevice`
    and can then be applied to a :obj:`servo`.

    Parameters
    ----------
    gain: :obj:`String`
        String from the input field.

    Returns
    -------
    :obj:`String`
        The gain embedded in a string for the html.P label.

    """
    try:
        gain = fast_real(gain, raise_on_invalid=True)
    except (ValueError, TypeError):
        raise PreventUpdate("Empty or no real number input.")
    servoDesign = DEVICE.servoDesign
    if servoDesign.gain != gain:
        servoDesign.gain = gain
    return "Gain (" + str(servoDesign.gain) + ")"


############################################################
######################### SOS Widget #######################
############################################################


#################### Getters ###############################


def getMaxFilters():
    """Return the maximum number of filters for the :obj:`ServoDevice.servoDesign`.

    This is a used multiple times in the UI and not part of a specific component.

    Returns
    -------
    :obj:`int`
        Maximum number of filters for the associated :obj:`ServoDesign`.

    """
    servoDesign = DEVICE.servoDesign
    return servoDesign.MAX_FILTERS


#################### Callbacks##############################


def callPlotServoDesign():
    """Handle plotting of amplitude and phase of the ServoDesign
    associated with the device over frequency.
    Part of the UI's Second Order Section.

    Returns
    -------
    :obj:`plotly.graph_objs`
        Returns a plotly/Dash graph_object/figure, consisting of data and layout.
        See https://plot.ly/ for detailed info.

    """
    fig = subplots.make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        subplot_titles=("Amplitude", "Phase"),
        print_grid=False,
    )
    servoDesign = DEVICE.servoDesign
    fig.update_xaxes(exponentformat="e", tick0=0, tickmode="linear", dtick=1)
    fig.update_xaxes(type="log")
    fig["layout"]["yaxis1"].update(title="Amplitude (dB)")
    fig["layout"]["yaxis2"].update(title="Phase (Hz)")
    fig["layout"].update(title="Transfer Function")
    fig["layout"].update(showlegend=False)
    # return an empty figure if no filters exist in ServoDesign - needed to make plot appear empty.
    # Preventing the update would keep the previous figure.
    if servoDesign.is_empty():
        return {}
    df = servoDesign.plot(plot=False)
    fig.add_trace(
        go.Scattergl(x=df.index, y=df["Servo A"], marker=dict(color=THEME[0])), 1, 1
    )
    fig.add_trace(
        go.Scattergl(x=df.index, y=df["Servo P"], marker=dict(color=THEME[1])), 2, 1
    )
    if "Servo+TF A" in df:
        fig.add_trace(
            go.Scattergl(x=df.index, y=df["Servo+TF A"], marker=dict(color=THEME2[0])),
            1,
            1,
        )
        fig.add_trace(
            go.Scattergl(x=df.index, y=df["Servo+TF P"], marker=dict(color=THEME2[1])),
            2,
            1,
        )
    return fig
