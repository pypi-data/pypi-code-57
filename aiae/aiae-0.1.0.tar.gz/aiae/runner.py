import os
from aithermal import ms_runner
import pandas as pd
import xlsxwriter
import simplelogging
import oyaml as yaml
from aihelper import aifile
import numpy as np
from scipy import integrate
import PySimpleGUI


def main():
    calculated_data, conversion_data, path = load()
    calculated_data.to_csv(
        os.path.join(path, "calculated data.csv"), sep=";", index=False
    )
    conversion_data.to_csv(os.path.join(path, "conversion data.csv"), sep=";")


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
            lambda g: integrate.simps(g)
        )
        sums = normalized_frame.apply(lambda x: integrate.simps(x))
        alpha = rolling_integral.div(sums)
        alphacs = alpha.cumsum()
        alphacs.columns = [f"Alpha Cumulative Sum"]
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
            conv_value = frame["Alpha Cumulative Sum"][
                frame["Alpha Cumulative Sum"] < conv
            ].idxmax()
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
