import datetime
import os
import re
from pandas import DataFrame


def write_sheets(frames, method, writer):
    for key in frames:
        for name, frame in frames[key].items():
            frame.to_excel(writer, sheet_name=f"{method} {name}", index=False)


def write_csv(frames, method):
    for key in frames:
        for name, frame in frames[key].items():
            frame.to_csv(os.path.join("out", f"{name}_{method}.csv"), index=False)


def write_topic_structured_csv(frames, method, out_path, wavelengths):
    tracer = []
    try:
        os.mkdir(os.path.join(out_path, "data_files_for_acd"))
    except OSError:
        pass
    out_path = os.path.join(out_path, "data_files_for_acd")
    for isograd in frames:
        # Gradient / Isotherm:
        for topic in frames[isograd]:
            # Topic
            for name, frame in frames[isograd][topic].items():
                # Frames
                if method == "STA":
                    sta_path = os.path.join(out_path, f"{name}_{'STA'}.csv")
                    dsc_path = os.path.join(out_path, f"{name}_{'DSC'}.csv")
                    sta_frame = frame[0]
                    dsc_frame = frame[1]

                    sta_meta = gather_meta(
                        topic, name, "STA", isograd, wavelengths, sta_path, frame
                    )
                    dsc_meta = gather_meta(
                        topic, name, "DSC", isograd, wavelengths, dsc_path, frame
                    )
                    sta_frame.to_csv(sta_path)
                    dsc_frame.to_csv(dsc_path)
                    tracer.append(sta_meta)
                    tracer.append(dsc_meta)

                else:
                    _path = os.path.join(out_path, f"{name}_{method}.csv")
                    meta_frame = gather_meta(
                        topic, name, method, isograd, wavelengths, _path, frame
                    )
                    tracer.append(meta_frame)

                    frame.to_csv(_path)
    return tracer


def gather_meta(topic, name, method, isograd, wavelengths, path, frame):
    meta_frame = base_meta_frame(isograd, name, path, topic)
    if method == "IR":
        meta_frame = ir_meta(topic, name, isograd, wavelengths, path)
    if method == "MS":
        meta_frame = ms_meta(topic, name, isograd, path, frame)
    if method == "STA":
        meta_frame = sta_meta(topic, name, isograd, path, frame)
    if method == "DSC":
        meta_frame = dsc_meta(topic, name, isograd, path, frame)
    return meta_frame


def ir_meta(
    topic, name, isograd, wavelengths, path,
):
    meta_frame = base_meta_frame(isograd, name, path, topic)
    wavelengths = [n for n in wavelengths if n]
    if wavelengths:
        meta_frame["Wavelengths"] = wavelengths
    else:
        meta_frame["Wavelengths"] = "RMS"
    meta_frame["Method"] = "IR"
    if isograd.lower() == "gradient":
        meta_frame["Gradient"] = name.split("-")[-1].strip()
    else:
        meta_frame["Isotherm Temperature"] = name.split("-")[-1].strip()
    return meta_frame


def sta_meta(topic, name, isograd, path, frame):
    meta_frame = base_meta_frame(isograd, name, path, topic)
    meta_frame["Method"] = "STA"
    meta_frame["STA Onset"] = ""
    if isograd.lower() == "gradient":
        meta_frame["Gradient"] = name.split("-")[-1].strip()
    else:
        meta_frame["Isotherm Temperature"] = name.split("-")[-1].strip()

    return meta_frame


def dsc_meta(topic, name, isograd, path, frame):
    meta_frame = base_meta_frame(isograd, name, path, topic)
    meta_frame["Method"] = "DSC"
    meta_frame["DSC Peak"] = ""
    if isograd.lower() == "gradient":
        meta_frame["Gradient"] = name.split("-")[-1].strip()
    else:
        meta_frame["Isotherm Temperature"] = name.split("-")[-1].strip()
    return meta_frame


def ms_meta(topic, name, isograd, path, frame):
    from scipy.signal import find_peaks

    n, f = 0, 0
    while n < 1:
        n = frame.index[f] - frame.index[0]
        f += 1
    peaks, peak_properties = find_peaks(frame.squeeze(), width=f, prominence=0.5)
    peak_start = peak_properties.get("left_ips") or 0
    peak_end = peak_properties.get("right_ips") or 0
    if peak_start:
        peak_start = frame.reset_index().iloc[peak_start].get("Time").squeeze()
    if peak_end:
        peak_end = frame.reset_index().iloc[peak_end].get("Time").squeeze()
    peak_width = peak_end - peak_start

    meta_frame = base_meta_frame(isograd, name, path, topic)

    meta_frame["Peak Start"] = peak_start
    meta_frame["Peak End"] = peak_end
    meta_frame["Peak Width"] = peak_width
    meta_frame["Method"] = "MS"
    ion = name.split("-")[-1].strip()

    temperature = name.split("-")[-2].strip()
    if isograd.lower() == "gradient":
        meta_frame["Gradient"] = temperature
    else:
        meta_frame["Isotherm Temperature"] = temperature
    meta_frame["Ion"] = ion
    return meta_frame


def base_meta_frame(isograd, name, path, topic):
    meta_frame = DataFrame(
        {"Name": name, "Scan-Type": isograd, "File": path}, index=[topic]
    )
    meta_frame.index.name = "Topic"
    meta_frame = meta_frame.reset_index()
    return meta_frame
