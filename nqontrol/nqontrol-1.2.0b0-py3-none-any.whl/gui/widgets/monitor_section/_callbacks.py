import plotly.graph_objs as go
from dash.exceptions import PreventUpdate

from nqontrol.general import settings
from nqontrol.gui.dependencies import DEVICE, THEME

############################################################
#################### Getters ###############################
############################################################


def getMonitorsServo(monitorNumber):
    """Return the target of a monitor channel.
    A servo channel can be assigned to one of {} monitor channels.

    Concerns the monitor section of the UI.
    Please note that this does not relate to the live graph of the UI
    but to the hardware monitor channels on the ADwin.

    Parameters
    ----------
    monitorNumber : :obj:`int`
        Monitor index.

    Returns
    -------
    :obj:`int`
        Monitor channel index or None.

    """.format(
        settings.NUMBER_OF_MONITORS
    )
    channelData = DEVICE.monitors[monitorNumber - 1]
    # channel data is either a dict or None
    if channelData is not None:
        return channelData["servo"]
    return channelData


def getMonitorsCard(monitorNumber):
    """Return the card of a monitor channel.
    One of 'input', 'aux', 'output', 'ttl' or `None`.
    A servo channel can be assigned to one of {} monitor channels.

    Concerns the monitor section of the UI.
    Please note that this does not relate to the live graph of the UI
    but to the hardware monitor channels on the ADwin.

    Parameters
    ----------
    monitorNumber : :obj:`int`
        Monitor index.

    Returns
    -------
    :obj:`String`
        Card specifier or `None`.

    """.format(
        settings.NUMBER_OF_MONITORS
    )
    dev = DEVICE
    channelData = dev.monitors[monitorNumber - 1]
    if channelData is not None:
        return channelData["card"]
    return channelData


############################################################
#################### Callbacks #############################
############################################################


def callADwinMonitor(channel, servo, card):
    """Set a ADwin hardware monitor channel.

    Parameters
    ----------
    channel : :obj:`int`
        ADwin hardware monitor channel index.
    servo : :obj:`int`
        Servo channel index.
    card : :obj:`String`
        String specify which servo signal to monitor. One of 'input', 'aux', 'output' or 'ttl'.

    Returns
    -------
    :obj:`list`
        Summary list with all the parameters that have been passed.
        Mostly used because the callback requires some output.

    """
    if servo is None or card is None:
        raise PreventUpdate()
    DEVICE.enableMonitor(channel, servo, card)
    return [channel, servo, card]


def callMonitorUpdate(servoNumber, visibleChannels):
    """Handle live plotting functionality for the UI.

    Parameters
    ----------
    servoNumber : :obj:`int`
        Servo index :obj:`servo.channel`
    visibleChannels : :obj:`list`
        List of Strings specifying the signals to be shown, arbitrary choice of:
        ['input', 'aux', 'output'].

    Returns
    -------
    :obj:`plotly.graph_objs`
        Returns a plotly/Dash graph_object/figure, consisting of data and layout.
        See https://plot.ly/ for detailed info.

    """
    # a device has to be connected and only returns an updating figure
    # if channels are set to active via the Checklist element below the Graph UI
    if visibleChannels:
        servo = DEVICE.servo(servoNumber)
        # this should never happen anyway
        # if servo.fifoStepsize is None:
        #     servo.fifoStepsize = 10

        # Setting visible channels
        servo.realtime["ydata"] = visibleChannels
        # Would be a list containing at least one of the keywords used in `colors` below
        df = servo.takeData()
        # this will be a list of plotly.graph_objs
        traces = []
        # Assigning colors for specific channel tags, if not set manually,
        # colors are assigned by plotly but incosistently, depending on order of adding plots.
        colors = {"input": THEME[0], "aux": THEME[1], "output": THEME[2]}
        for label in visibleChannels:
            data = df[label]
            # For more options on styling the graphs, please look at the plotly documentation
            traces.append(
                go.Scattergl(
                    x=df.index,
                    y=data,
                    name=label,
                    mode="lines",
                    marker=dict(color=colors[label]),
                )
            )
        figure = {
            "data": traces,
            "layout": go.Layout(yaxis=dict(title="Amplitude (V)", uirevision="foo")),
        }
        return figure
    raise PreventUpdate()


def callMonitorUpdateChannels(servoNumber, visibleChannels):
    """Set visible channels attribute of :obj:`servo.realtime`.

    Parameters
    ----------
    servoNumber : :obj:`int`
        Servo index :obj:`servo.channel`
    visibleChannels : :obj:`list`
        List of Strings specifying the signals to be shown, arbitrary choice of:
        ['input', 'aux', 'output'].

    Returns
    -------
    :obj:`String`
        Feedback string on what was applied. Just for UI purposes.

    """
    if visibleChannels:
        servo = DEVICE.servo(servoNumber)
        servo.realtime["ydata"] = visibleChannels
        return "ydata set to" + str(visibleChannels)
    return "Empty channels"
