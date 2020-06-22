import os

import PySimpleGUI
import numpy as np
import pandas as pd
from aihelper import aifile
from aithermal import ms_runner
from scipy import integrate
import matplotlib.pyplot as plt

plt.style.use("ggplot")

ACS = "Alpha Cumulative Sum"


def main():
    calculated_data, conversion_data, path = load()
    print("Saving Data")
    try:
        calculated_data.to_csv(
            os.path.join(path, "calculated data.csv"), sep=";", index=False
        )
    except PermissionError:
        print("Permission denied to write Calculated Data")

    try:
        conversion_data.to_csv(os.path.join(path, "conversion data.csv"), sep=";")
    except PermissionError:
        print("Permission denied to write Conversion Data")

    i = 0
    print("Plotting Graphs")
    for n in range(len(calculated_data.columns) // 5):
        oo = calculated_data.iloc[:, i : i + 5].replace("", np.nan).dropna()
        oo.set_index("Temperature (K)", inplace=True)
        ax = oo.plot.area(stacked=False)
        for conv in np.arange(0.2, 0.7, 0.2):
            conv = conv.round(1)
            conv_temp = int(oo[oo >= conv].idxmin()[ACS].round(0))
            ax.annotate(
                f"Conversion\n {conv}",
                xy=(conv_temp, conv),
                xycoords="data",
                xytext=(-100, 60),
                textcoords="offset points",
                size=8,
                arrowprops=dict(
                    arrowstyle="fancy",
                    fc="red",
                    ec="none",
                    connectionstyle="angle3,angleA=0,angleB=-90",
                ),
            )
        plt.legend(frameon=False)
        plt.legend(framealpha=0.0)
        plt.savefig(os.path.join(path, f"Gradient - {conversion_data.iloc[:,n].name}"))
        i += 5
        print(f"Gradient Plot {conversion_data.iloc[:,n].name} Finished")


def load():
    layout = [
        [PySimpleGUI.Text("Ion to Calculate"), PySimpleGUI.InputText(key="ion")],
        [
            PySimpleGUI.Text("MS Offset (Default 30)"),
            PySimpleGUI.InputText(key="offset"),
        ],
        [
            PySimpleGUI.Text("Directory for data"),
            PySimpleGUI.InputText(key="browse"),
            PySimpleGUI.FolderBrowse(),
        ],
        [PySimpleGUI.Submit()],
    ]

    PySimpleGUI.ChangeLookAndFeel("TealMono")
    window = PySimpleGUI.Window("Tools", layout)
    event, result = window.Read()
    window.Close()

    path = result.get("browse")
    ion = result.get("ion")
    offset = result.get("offset", 30)
    calculated_data, conversion_data = load_data(path, ion, offset)
    return calculated_data, conversion_data, path


def load_data(path, ion, offset):
    files = aifile.activation_energy(path, ion)
    ms_data = {a: ms_runner(f, offset) for a, f in files.items()}
    calculated_data, conversion_data = do_the_work(ms_data)
    return calculated_data, conversion_data


def do_the_work(data: dict):
    """

        :param data: (frames, gradients)
        :return:
        """
    calculated_frames = {}
    for gradient, frame in data.items():
        normalized_frame = frame.div(frame.max())
        normalized_frame.index = (normalized_frame.index * int(gradient) + 30) + 273.15
        rolling_integral = normalized_frame.rolling(2).apply(
            lambda g: integrate.simps(g, x=g.index)
        )
        sums = normalized_frame.apply(lambda g: integrate.simps(g, x=g.index))
        alpha = rolling_integral.div(sums)
        alphacs = alpha.cumsum()
        alphacs.columns = [ACS]
        rolling_integral.columns = [f"Rolling Integral"]
        alpha.columns = [f"Alpha"]
        df = pd.concat([normalized_frame, rolling_integral, alpha, alphacs], axis=1)
        df.index.name = "Temperature (K)"
        calculated_frames[gradient] = df
    conversion_values = {}
    conversion = np.arange(0.1, 1.1, 0.1)
    for gradient, frame in calculated_frames.items():
        conversion_values[gradient] = {}
        for conv in conversion:
            conv = round(conv, 1)
            conv_value = frame[ACS][frame[ACS] < conv].idxmax()
            if conversion_values.get(gradient):
                conversion_values[gradient][conv] = conv_value
            else:
                conversion_values[gradient] = {conv: conv_value}
    unique_index_calculated_frame = [
        a.reset_index() for a in calculated_frames.values()
    ]

    calculated_data = pd.concat(unique_index_calculated_frame, axis=1).fillna("")
    conversion_factor = pd.DataFrame.from_dict(conversion_values)
    conversion_factor.index.name = "Conversion Factor"
    return calculated_data, conversion_factor


if __name__ == "__main__":
    main()
