# -*- coding: utf-8 -*-
import logging
import altair as alt
from altair import pipe, limit_rows, to_values
from pandas import DataFrame

logger = logging.getLogger()
TU = {
    0: {"u": "yearmonth", "l": "année - mois", "f": "%b-%y"},
    1: {"u": "yearmonthdate", "l": "date et mois", "f": "%d-%b"},
    2: {"u": "yearmonthdatehours", "l": "date et heure", "f": "%Hh %d-%b"},
    3: {"u": "yearmonthdatehoursminutes", "l": "date et minute", "f": "%H:%M %d/%m"},
    4: {"u": "month", "l": "mois", "f": "%b"},
    5: {"u": "day", "l": "jour", "f": "%A"},
    6: {"u": "hours", "l": "heure", "f": "%Hh"},
    7: {"u": "hoursminutes", "l": "heure et minute", "f": "%H:%M"},
    8: {"u": "minutes", "l": "minute", "f": "%M\\'"},
}


def set_row_limit(num=5000):
    """
    set a new limit to the number of rows that altair can handle.
    Creates and register a new data_transformer "myPipe"
    Keyword Arguments:
    num -- the number of row that can be handle by altair. default 5000

    Returns: DataTransformerRegistry
    """

    def myPipe(data):
        return pipe(data, lambda D: limit_rows(D, num), to_values)

    alt.data_transformers.register("myPipe", myPipe)
    return alt.data_transformers.enable("myPipe")


def def_chart(data, w=600, h=400, bg="white", sample=None, mark=None):
    """ Define a default chart.
    Sample is the portion of data to display as a fraction of the whole. if the data lenght is bigger than 3000 and no sample give then reduce the data to approximatively 3000 datum"""
    if len(data) > 3000 and sample is None:
        sample = round(3000 / len(data), 4)

    if sample is None or sample == 1:
        df = data
    else:
        assert sample < 1 and sample > 0, f"sample={sample} must be in ]O;1["
        df = data.sample(int(len(data) * sample))

    # base chart
    BC = alt.Chart(df).configure(background=bg).properties(height=h, width=w)
    return BC.mark_bar() if mark == "bar" else BC


def base_graph_gen(df=None, chart_base=None, tu=None):
    """ Generate a standard stack graph for df based on group, topics and time.
    One of df or chart_base must be set.
    if bool customtu set use cutom Time Units else use altair's default,
    chart_base is an instance of alt.Chart with general stuff configured. if None use def_chart defaults"""

    # encoding channels
    assert not (
        df is None and chart_base is None
    ), f"One of df={df} or chart_base={chart_base} must be set."

    if tu is not None:
        tuUnit, tuLabel, tuFormat = [TU[tu][x] for x in ["u", "l", "f"]]
        ex = alt.X(
            "msgTS:T",
            timeUnit=tuUnit,
            axis=alt.Axis(format=tuFormat, title=f"Msgs. par {tuLabel}"),
        )
    else:
        ex = alt.X("msgTS:T")

    ey = alt.Y(
        "msgID:Q", aggregate="count", axis=alt.Axis(title="Nb msgs."), stack="zero"
    )

    ec = alt.Color(
        "group_name",
        legend=alt.Legend(title="Groupes"),
        scale=alt.Scale(scheme="category20"),
    )

    # pour la config {'mark': {'tooltip': None}, 'view': {'height': 300, 'width': 400}},
    # At = At.sort_values(by="group_name")

    if not chart_base:
        chart_base = def_chart(df)
    else:
        logger.warning(f"ignoring df")

    return chart_base.mark_bar().encode(
        x=ex, y=ey, color=ec, order=alt.Order("group_size", sort="ascending")
    )


def trim_json(_from, items=None):
    """ remove D json's keys if in remove iterable  """
    new = {}
    if items is None:
        return _from

    for k in items:
        new = {dk: _from[dk] for dk in _from.keys() if k not in dk}

    return new
