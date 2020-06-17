#! /usr/bin/env python3

import os
import subprocess
from itertools import cycle
from pyguppy_client_lib.client_lib import GuppyClient

try:
    import h5py
except Exception:
    H5PY_UNAVAILABLE = True

# Counter that cycles [0, 2**32)
_COUNT = cycle(range(0, int(2 ** 32), 1))
FINISH_TIMEOUT = 300

def pull_read(filename):
    with h5py.File(filename, "r") as handle:
        reads_group = handle["Raw/Reads"]
        read_group_name = list(reads_group.keys())[0]
        read_group = reads_group[read_group_name]
        signal_ds = read_group["Signal"]
        raw = signal_ds[()]
        read_id = read_group.attrs["read_id"].decode("utf-8")
        channel_id_attrs = handle["UniqueGlobalKey/channel_id"].attrs
        digi = channel_id_attrs["digitisation"]
        rng = channel_id_attrs["range"]
        off = channel_id_attrs["offset"]
        read = {
            "raw_data": raw,
            "read_id": read_id,
            "daq_offset": off,
            "daq_scaling": rng / digi,
        }
    return read


def basecall_with_pyguppy(client, input_path, save_file=None):
    if save_file is not None:
        out = open(save_file, "w")
        out.write("read_id\tsequence_length\n")
    else:
        out = None

    try:
        num_files_sent = 0
        num_files_called = 0
        called_ids = []
        called_reads = []
        files = [f for f in os.listdir(input_path) if f.endswith(".fast5")]
        all_files = files.copy()
        file_count = len(files)
        while num_files_sent < file_count:
            filename = os.path.join(input_path, all_files[num_files_sent])
            read = pull_read(filename)
            read["read_tag"] = num_files_sent
            result = client.pass_read(read)
            if result == GuppyClient.success:
                num_files_sent += 1
                files.pop(0)
            else:
                raise Exception("Attempt to pass read to server failed. Return value is {}.".format(result))
            completed_reads, result = client.get_completed_reads()
            if GuppyClient.success != result:
                raise Exception("Request for completed reads failed. Return value is {}.".format(result))
            for read in completed_reads:
                read_id = read["metadata"]["read_id"]
                sequence_length = read["metadata"]["sequence_length"]
                called_ids.append(read["read_tag"])
                called_reads.append(read)
                num_files_called += 1
                if out is not None:
                    out.write("{}\t{}\n".format(read_id, sequence_length))

        result = client.finish(FINISH_TIMEOUT)
        if GuppyClient.success != result:
            raise Exception("Call to final() method did not complete quickly enough. Return value is {}.".format(result))
        completed_reads, result = client.get_completed_reads()
        assert GuppyClient.success == result
        for read in completed_reads:
            read_id = read["metadata"]["read_id"]
            sequence_length = read["metadata"]["sequence_length"]
            called_ids.append(read["read_tag"])
            called_reads.append(read)
            num_files_called += 1
            if out is not None:
                out.write("{}\t{}\n".format(read_id, sequence_length))
    except Exception:
        raise
    finally:
        if out is not None:
            out.close()
    unique_ids = set(called_ids)
    assert file_count == num_files_sent
    assert file_count == num_files_called
    assert file_count == len(unique_ids)
    return called_reads


def run_server(options, bin_path=None):
    """
    Start a basecall server with the specified parameters.
    :param options: List of command line options for the server.
    :param bin_path: Optional path to basecall server binary executable.
    :return: A tuple containing the handle to the server process, and the port the server is listening on.

    If the server cannot be started, the port will be returned as 'ERROR'.
    Use the 'auto' option for the port to have the server automatically select an available port.
    """
    executable = "guppy_basecall_server"
    if bin_path is not None:
        executable = os.path.join(bin_path, executable)
    server_args = [executable]
    server_args.extend(options)

    print("Server command line: ", " ".join(server_args))
    server = subprocess.Popen(server_args, stdout=subprocess.PIPE)
    for line in iter(server.stdout.readline, ""):
        message_to_find = b"Starting server on port: "
        if message_to_find in line:  # This will be true when the server has started up.
            port_string = line[len(message_to_find) :].decode("ascii").strip()
            break
        if len(line) == 0:  # If something goes wrong, this prevents an endless loop.
            return server, "ERROR"
    print("Server started on port: {}".format(port_string))
    return server, port_string


def package_read(
    read_id: str,
    raw_data: "numpy.ndarray[numpy.int16]",
    daq_offset: float,
    daq_scaling: float,
    read_tag: int = None,
) -> dict:
    """Package a read for pyguppy_client_lib

    :param read_id: Read ID for the read, doesn't need to be unique but must
        not be empty
    :type read_id: str
    :param raw_data: 1d numpy array of signed 16 bit integers
    :type raw_data: numpy.ndarray[numpy.int16]
    :param daq_offset: Offset for pA conversion
    :type daq_offset: float
    :param daq_scaling: Scale factor for pA conversion
    :type daq_scaling: float
    :param read_tag: 32 bit positive integer, must be unique to each read. If
        ``None`` will be assigned a value from the pyguppy global counter
    :type read_tag: int

    :returns: read data packaged for guppy
    :rtype: dict
    """
    if read_tag is None:
        read_tag = next(_COUNT)
    return {
        "read_tag": read_tag,
        "read_id": read_id,
        "raw_data": raw_data,
        "daq_offset": daq_offset,
        "daq_scaling": daq_scaling,
    }


def get_barcode_kits(address: str, timeout: int) -> list:
    """Get available barcode kits from server

    :param address: guppy_basecall_server address eg: 127.0.0.1:5555
    :type address: str
    :param timeout: Timeout in milliseconds
    :type timeout: int

    :raises RuntimeError: When

    :return: List of barcode kits supported by the server
    :rtype: list
    """
    result, status = GuppyClient.get_barcode_kits(address, timeout)
    if status != GuppyClient.success:
        raise RuntimeError("Could not get barcode kits")
    return result
