from collections import Counter

import pandas as pd  # pytype: disable=import-error
import plotly.express as px  # pytype: disable=import-error


class PlottableCounter(Counter):
    def get_figure(self):
        df = (
            pd.DataFrame.from_dict(self, orient="index")
            .reset_index()
            .rename(columns={"index": "item", 0: "count"})
        )
        fig = px.bar(df, x="item", y="count")
        return fig
