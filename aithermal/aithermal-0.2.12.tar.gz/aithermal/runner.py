import os
import argparse
import aithermal
import pandas as pd
import xlsxwriter
import simplelogging
import oyaml as yaml
from aihelper import aifile, aiyaml


def main():
    log = simplelogging.get_logger(file_name="aithermal.log", console=False)

    def represent_none(self, _):
        return self.represent_scalar("tag:yaml.org,2002:null", "")

    yaml.add_representer(type(None), represent_none)

    parameters = os.path.join(os.getcwd(), "project parameters.yaml")
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", help="root path")

    try:
        with open(parameters, "r") as stream:
            data_loaded = yaml.safe_load(stream)
    except FileNotFoundError as e:
        data_loaded = aiyaml.write_acd_thermal_yaml()
        with open("project parameters.yaml", "w") as outfile:
            yaml.dump(data_loaded, outfile, default_flow_style=False)
        print("Please fill out the project parameters.yaml document")
        log.exception(f"{FileNotFoundError} {e}")
        os.startfile(os.path.join(os.getcwd(), "project parameters.yaml"))
    try:
        _run(*decompress(data_loaded))
    except TypeError as e:
        raise (e)
        print("Please double-check your project parameters.yaml document'")
        log.exception(e)
        os.startfile(os.path.join(os.getcwd(), "project parameters.yaml"))


def decompress(data_loaded):
    wavelengths = data_loaded.get("WAVE LENGTHS")
    rms = data_loaded.get("RMS")
    root = data_loaded.get("DIRECTORY")
    ms_offset = data_loaded.get("MS Deadtime (Seconds)")
    directory_listing, method_listing, temperature_listing = aifile.topic_directories(
        root
    )

    return (method_listing, temperature_listing, root, wavelengths, rms, ms_offset)


def _run(method_listing, temperature_listing, root, wavelengths, rms, ms_offset):

    gradient_temp = temperature_listing.get("gradient", [])
    isotherm_temp = temperature_listing.get("isotherm", [])

    baseline_path = os.path.join(root, "Parameter\\Baseline\\")

    all_frames = aithermal.load_dsc(
        method_listing, baseline_path, rms, wavelengths, ms_offset
    )

    tracer = []
    for method, data in all_frames.items():
        tracer.extend(
            aithermal.write_topic_structured_csv(data, method, root, wavelengths)
        )
    df = pd.concat(tracer, axis=0, ignore_index=True)
    acd_trace_path = os.path.join(root, "ACD Traces")
    try:
        os.mkdir(acd_trace_path)
    except OSError:
        pass
    df.to_csv(os.path.join(acd_trace_path, "ACD Trace.csv"), index=False, sep=";")


def generate_results_csv_acd(frame, prefix):
    return pd.DataFrame.from_dict(frame, orient="index").add_prefix(f"{prefix} ")


if __name__ == "__main__":
    main()
