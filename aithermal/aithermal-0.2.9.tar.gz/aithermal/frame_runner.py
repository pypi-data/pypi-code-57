import os
import re
from collections import defaultdict

import pandas as pd


def derivative(df):
    df = df.iloc[40:]
    local_df = df.reset_index()
    delta = local_df[["Time", "Unsubtracted Weight"]].diff().dropna()
    delta["Unsubtracted Weight"] = (
        delta["Unsubtracted Weight"].ewm(span=50).mean().div(delta["Time"])
    )
    delta = (
        pd.concat([delta, local_df["Sample Temperature"]], axis=1)
        .dropna()
        .drop(columns=["Time", "Sample Temperature"], errors="ignore")
    )
    delta.rename(columns={"Unsubtracted Weight": "Derivative Weight"}, inplace=True)
    return delta


def percentage(df, column):
    percent = df[column]
    percent = percent.div(percent.max())
    percent = percent.multiply(100)
    return percent


def correct(data_frame, baseline_frame, column):
    data = data_frame
    if not baseline_frame.empty:
        data = data_frame.get(column)
        correction = baseline_frame.get(column)
        data = data - correction
    return data


def baseline_load(file_path: str, columns_to_use):
    baselines = os.listdir(file_path)
    baseline_dataframes = {}
    for file in baselines:
        full = os.path.join(file_path, file)
        isograd, *temperature = [
            os.path.splitext(f)[0].lower() for f in file.split(" ")
        ]
        if temperature:
            data_frame = pd.read_csv(full, engine="python", usecols=columns_to_use)
            if not baseline_dataframes.get(isograd):
                baseline_dataframes[isograd] = {temperature[0]: data_frame}
            else:
                baseline_dataframes[isograd][temperature[0]] = data_frame
        else:
            data_frame = pd.read_csv(full, engine="python", usecols=columns_to_use)
            baseline_dataframes[isograd] = data_frame

    return baseline_dataframes


def wl_ext(frame, wavelength):
    wave_list = []
    for wl in wavelength:
        try:
            wave_list.append(frame[wl])
        except KeyError:

            def jitter(jitter_frame, n):
                return n if n in jitter_frame.columns else jitter(jitter_frame, n + 1)

            wave_list.append(frame[jitter(frame, wl + 1)])
    extracted_frame = pd.DataFrame(wave_list).transpose()
    return extracted_frame


def load_dsc(path, baseline_path=None, rms=False, wavelengths=None, ms_offset=None):
    some_dict = defaultdict()
    for method, data_list in path.items():
        gradient_files = data_list.get("gradient", [])
        isotherm_files = data_list.get("isotherm", [])

        gradient_args = {
            "data": gradient_files,
            "method": method,
            "ms_offset": ms_offset,
        }
        isotherm_args = {
            "data": isotherm_files,
            "method": method,
            "ms_offset": ms_offset,
        }

        if method == "STA":
            gradient_args["columns"] = [
                "Time",
                "Unsubtracted Weight",
                "Sample Temperature",
                "Unsubtracted Heat Flow",
            ]
            isotherm_args["columns"] = [
                "Time",
                "Unsubtracted Weight",
                "Sample Temperature",
                "Unsubtracted Heat Flow",
            ]

            gradient_args["baseline_path"] = baseline_path
            isotherm_args["baseline_path"] = baseline_path

        if method == "IR":

            gradient_args["wavelength"] = [wave for wave in wavelengths if wave]
            isotherm_args["wavelength"] = [wave for wave in wavelengths if wave]
            if rms:
                rms_pattern = r"(RMS Intensity Profile)"
                gradient_rms = list(
                    filter(lambda x: re.search(rms_pattern, x), gradient_files)
                )
                isotherm_rms = list(
                    filter(lambda x: re.search(rms_pattern, x), isotherm_files)
                )
                gradient_args["data"] = gradient_rms
                isotherm_args["data"] = isotherm_rms
                gradient_args["rms"] = rms
                isotherm_args["rms"] = rms
        if method == "GC":
            gradient_args["data"] = [
                tic_file for tic_file in gradient_files if "tic" in tic_file.lower()
            ]
            isotherm_args["data"] = [
                tic_file for tic_file in gradient_files if "tic" in tic_file.lower()
            ]
        if not some_dict.get(method):
            some_dict[method] = {}
        some_dict[method]["gradient"] = helper(**gradient_args)
        some_dict[method]["isotherm"] = helper(**isotherm_args)

    return some_dict


def helper(**kwargs):
    data_files = kwargs.get("data")
    method = kwargs.get("method")
    wavelength = kwargs.get("wavelength")
    rms = kwargs.get("rms")
    columns_to_use = kwargs.get("columns")
    baseline = kwargs.get("baseline_path")
    ms_offset = kwargs.get("ms_offset")
    topic_pattern = r"\\(Topic.*?)\\"
    frame_dictionary = {}

    for file in data_files:
        data_frame = pd.DataFrame()
        topic_name, name = naming(file, topic_pattern)

        if method == "IR":
            data_frame = ir_runner(file, rms, wavelength)

        if method == "STA":
            data_frame = sta_runner(file, columns_to_use, baseline)

        if method == "MS":
            data_frame = ms_runner(file, ms_offset)

        if method == "MS":
            ion = os.path.splitext(file.split("\\")[-1])[0]
            name = " ".join([name, "-", ion])

        if frame_dictionary.get(topic_name):
            frame_dictionary[topic_name][name] = data_frame

        else:
            frame_dictionary[topic_name] = {name: data_frame}

    return frame_dictionary


def ms_runner(file, ms_offset=None, norm=True):
    data_frame = pd.read_table(
        file, sep="\s+", header=None, names=["Time", "Absorbance"], index_col="Time"
    )
    if ms_offset:
        data_frame.index = data_frame.index.astype(float).map(
            lambda x: x - (ms_offset / 60)
        )
        data_frame = data_frame[data_frame.index >= 0]
    data_frame["Absorbance"] = data_frame["Absorbance"].ewm(span=5).mean()
    if norm:
        data_frame = series_normalizer(data_frame)
    return data_frame


def sta_runner(file, columns_to_use, baseline=None):
    data_frame = pd.read_csv(
        file, engine="python", usecols=columns_to_use, index_col="Time"
    )
    sta = percentage(data_frame, ["Unsubtracted Weight"])
    sta.rename(columns={"Unsubtracted Weight": "Percent Weight"}, inplace=True)
    method, isograd, temperature = mit_extract(file)
    isograd = isograd.lower()

    baseline_frames = baseline_load(baseline, columns_to_use)
    if temperature.isdigit():
        corrective_frame = baseline_frames.get(
            isograd, {temperature: pd.DataFrame()}
        ).get(temperature)
    else:
        corrective_frame = baseline_frames.get(isograd, pd.DataFrame())
    baseline_corrected = correct(
        data_frame, corrective_frame, ["Unsubtracted Heat Flow"]
    )
    baseline_corrected.rename(
        columns={"Unsubtracted Heat Flow": "Corrected Heat Flow"}, inplace=True
    )
    dsc = percentage(baseline_corrected, ["Corrected Heat Flow"])
    dsc.rename(columns={"Corrected Heat Flow": "Percent Heat Flow"}, inplace=True)

    return [sta, dsc]


def mit_extract(file):
    remaning_file, method = os.path.split(file)
    remaning_file, temperature = os.path.split(remaning_file)
    remaning_file, isograd = os.path.split(remaning_file)
    return method, isograd, temperature


def ir_runner(file, rms, wavelength):

    if rms:
        data_frame = pd.read_csv(file, engine="python", header=2, index_col=0).dropna()
        if data_frame.index.name == "Time (secs)":
            data_frame.index = data_frame.index.map(lambda x: round((x / 60), 2))
        data_frame = series_normalizer(data_frame)
        return data_frame
    data_frame = pd.read_csv(file, engine="python", header=3).dropna().transpose()
    header = data_frame.iloc[0]
    header = header.astype(float).astype(int)
    data_frame = data_frame[1:]
    data_frame.columns = header
    data_frame = wl_ext(data_frame, wavelength)
    if data_frame.index.name == "Time (secs)":
        data_frame.index = data_frame.index.map(lambda x: round((x / 60), 2))
    data_frame = series_normalizer(data_frame)

    return data_frame


def naming(file, topic_pattern=r"\\(Topic.*?)\\"):
    topic_name = re.search(topic_pattern, file)[1]
    topic_name = topic_name.replace("Topic", "").strip()
    method, isograd, temperature = mit_extract(file)
    if temperature.isdigit():
        name = " ".join([topic_name, "-", temperature])
    else:
        name = " ".join([topic_name, "-", isograd])
    return topic_name, name


def series_normalizer(data_frame):
    data_frame = (data_frame - data_frame.min()) / (data_frame.max() - data_frame.min())
    return data_frame
