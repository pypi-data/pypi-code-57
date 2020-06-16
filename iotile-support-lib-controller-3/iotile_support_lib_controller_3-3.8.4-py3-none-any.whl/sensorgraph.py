"""Proxy plugin for accessing all sensorgraph related functionality."""
import struct
import datetime
from typedargs.annotate import docannotate, param, annotated, return_type, context
from iotile.core.hw.proxy.plugin import TileBusProxyPlugin
from iotile.core.utilities.packed import unpack
from iotile.core.utilities.hash_algorithms import KNOWN_HASH_ALGORITHMS
from iotile.core.exceptions import *
from iotile.core.hw.reports.report import IOTileReading
from iotile.core.utilities.console import ProgressBar
from .lib_controller_types.fw_streamerstatus import StreamerStatus
from .lib_controller_types.fw_configvariable import ConfigDescriptor


@context("SensorGraph")
class SensorGraphPlugin(TileBusProxyPlugin):
    def __init__(self, parent):
        super(SensorGraphPlugin, self).__init__(parent)

        self.saving_script = False
        self.no_exec = False
        self.ascii_script = []
        self.bin_script = []

    @return_type("map(string, integer)")
    def count_readings(self):
        """
        Count how many readings are stored in the device's sensor log
        """

        res = self.rpc(0x20, 0x01, result_type=(0, True))

        err, storage, streaming = unpack("<LLL", res['buffer'])
        if err:
            raise HardwareError("Error calling count_readings rpc", error_code=err)

        return {'storage': storage, 'streaming': streaming}

    @param("noexec", "bool", desc="Do not actually execute add_node, add_streamer, clear, reset and persist commands")
    def capture_graph(self, noexec=True):
        """Start saving the sensor graph created from now on to a file
        """

        self.saving_script = True
        self.ascii_script = []
        self.bin_script = []
        self.no_exec = noexec

    @param("binary", "bool", desc="Save graph in encoded format rather than human readable")
    @param("path", "path", "writeable", desc="Path to save output file")
    def save_graph(self, path, binary=False):
        """Save the sensor graph just created to a file

        Both a human readable/editable and an opaque encoded format are supported
        """

        if not self.saving_script:
            raise DataError("You must capature a graph using capture_graph before calling save_graph")

        with open(path, "wb") as out:
            if binary:
                out.write("Sensor Graph\nFormat: 1.0\nType: BINARY\n\n")

                for cmd, args in self.bin_script:
                    arghex = ''.join(['{:02x}'.format(x) for x in bytearray(args)])
                    out.write("0x{:04x}: {}\n".format(cmd, arghex))
            else:
                out.write("Sensor Graph\nFormat: 1.0\nType: ASCII\n\n")

                for line in self.ascii_script:
                    out.write(line + '\n')

        self.no_exec = False
        self.saving_script = False

    @return_type("integer")
    def count_nodes(self):
        """
        Count how many nodes are defined in this sensor graph
        """

        count, = self.rpc(0x20, 0x02, result_format="L")

        return count

    @docannotate
    def inspect_node(self, index, fmt=None):
        """Get a description of the graph node using its index.

        This is the same description that would be used to create that graph
        node using a call to add_node.  It can be used to verify that the
        sensor_graph was programmed correctly or to inspect a sensor_graph on
        an unknown device.

        **This function requires that you have iotile-sensorgraph installed.**

        Args:
            index (int): The index of the graph node that we want to
                inspect.  If this is >= the number of nodes in the graph an
                ArgumentError exception will be raised.
            fmt (string): How to format the return data


        Returns:
            str: A string description of the graph node at the given index. This
                string could be passed directly to add_node to create an instance
                of this graph node.
                If result_format=='hex' then the hex string representation of the node is returned,
                If result_format=='bin' then the binary node data is returned (useful for calculations)
        """

        res = self.rpc(0x20, 0x16, index, arg_format="H", result_type=(0, True))

        bindata = res['buffer']

        if fmt == 'hex':
            try:
                from binascii import hexlify
            except ImportError:
                raise ExternalError("You must pip install binascii to use inspect_node --result_format='hex'", suggestion="pip install binascii")

            return hexlify(bindata)

        elif fmt == 'bin':
            return bindata

        else:
            try:
                from iotile.sg.node_descriptor import parse_binary_descriptor
            except ImportError:
                raise ExternalError("You must pip install iotile-sensorgraph to use inspect_node", suggestion="pip install -U iotile-sensorgraph")

            return parse_binary_descriptor(bindata)

    @docannotate
    def sg_checksum(self, algorithm="sha256"):
        """ Calculate a checksum over the sensorgraph node data

        Args:
            algorithm (str): The algorithm to hash the data with

        Returns:
            string: The checksum of the sensorgraph
        """
        hash_algorithm = KNOWN_HASH_ALGORITHMS[algorithm]
        nodes_bytes = bytearray()
        nodes = self.count_nodes()
        if nodes > 0:
            for i in range(nodes):
                nodes_bytes += self.inspect_node(i,'bin')
            return hash_algorithm.calculate(hash_algorithm.algorithm, nodes_bytes)
        else:
            return ""

    @docannotate
    def inspect_streamer(self, index, fmt=None):
        """Get a descritpion of a streamer using its index.

        The description contains the following information:
        - type
        - format
        - selector
        - destination tile

        Args:
            index (int): The index of the graph streamer that you want to query.
                If this index does not correspond with an allocated streamer, an
                ArgumentError will be raised.
            fmt (string): How to format the return data

        Returns:
            DataStreamer show-as string: A description of the streamer at the given index.
        """

        try:
            from iotile.sg.streamer_descriptor import parse_binary_descriptor
        except ImportError:
            raise ExternalError("You must pip install iotile-sensorgraph to use inspect_streamer", suggestion="pip install -U iotile-sensorgraph")

        err, desc = self.rpc(0x20, 0x17, index, arg_format="H", result_format="L14s2x")
        if err:
            raise ArgumentError("Invalid streamer index that was not allocated", error_code=err)

        if fmt == 'hex':
            try:
                from binascii import hexlify
            except ImportError:
                raise ExternalError("You must pip install binascii to use inspect streamer --result_format='hex'", suggestion="pip install binascii")

            return hexlify(desc)

        elif fmt == 'bin':
            return desc

        return parse_binary_descriptor(desc)

    @docannotate
    def sg_streamer_checksum(self, algorithm="sha256"):
        """Calculate a checksum over the sensor graph's streamers
        This function will blindly iterate through streamers until the index
        of the streamer raises an exception that the streamer doesn't exist.
        This is how we iterate through all the streamers, since we don't have a
        RPC to return the number/indices of streamers.
        Args:
            algorithm (str): The algorithm to hash the data with
        Returns:
            string: The checksum of the sensorgraph
        """

        streamer_idx = 0

        hash_algorithm = KNOWN_HASH_ALGORITHMS[algorithm]
        streamers_bytes = bytearray()

        while True:
            try:
                streamers_bytes += self.inspect_streamer(streamer_idx, 'bin')
                streamer_idx += 1
            except ArgumentError:
                return hash_algorithm.calculate(hash_algorithm.algorithm,
                                                streamers_bytes)

    def inspect_config_variable(self, index):
        """Get a description of a config variable"""

        err, entry = self.rpc(0x2a, 0x0a, index, result_format="L16s")

        if err != 0:
            raise HardwareError("Could not get config variable information", error_code=err)

        info = ConfigDescriptor(bytearray(entry))

        var_data = bytearray()

        for i in range(0, info.data_length, 16):
            res = self.rpc(0x2a, 0x0d, index, i, result_type=(0, True))
            err, = struct.unpack_from("<L", res['buffer'])
            if err != 0:
                raise HardwareError("Could not get data for variable", error_code=err, index=index)

            data = res['buffer'][4:]
            var_data += data

        name, = struct.unpack("<H", var_data[0:2])
        data = var_data[2:]
        info.add_name(name)
        info.add_data(data)

        return info

    @docannotate
    def sg_config_var_checksum(self, algorithm="sha256", use_ignorelist=True,
                               ignoreconfigs_list_var=0x2102):
        """Calculate a checksum over the device's config variables
        The function iterates through all the config variables and adds it to
        a list. It will see if there is a config variable that is used to list
        config variables to exclude during the checksum calculation. It will
        then build a bytearray of the config variables except those listed
        in the ignore list, then it will calculate the checksum.
        Args:
            algorithm (str): The algorithm to hash the data with
        Returns:
            string: The checksum of the config variables
        """

        hash_algorithm = KNOWN_HASH_ALGORITHMS[algorithm]
        configs_bytes = bytearray()

        num_vars, = self.rpc(0x2a, 0x0b, result_format="L")

        config_list = []
        ignoreconfigs_bytes = bytearray()

        for i in range(1, num_vars + 1):
            config_desc = self.inspect_config_variable(i)
            config_list.append(config_desc)

            if config_desc.name == ignoreconfigs_list_var:
                ignoreconfigs_bytes = config_desc.data

        if use_ignorelist:
            ignore_list = _parse_ignoreconfigs(ignoreconfigs_bytes)
            for config in config_list:
                if _is_ignored_config(ignore_list, str(config.target), config.name):
                    continue
                configs_bytes += bytes(config.parse_descriptor(), 'utf-8')
        else:
            for config in config_list:
                configs_bytes += bytes(config.parse_descriptor(), 'utf-8')

        return hash_algorithm.calculate(hash_algorithm.algorithm,
                                        configs_bytes)

    @docannotate
    def sg_constants_checksum(self, algorithm="sha256"):
        """Get a description of a constant stream
        Args:
            algorithm (str): The algorithm to hash the data with
        Returns:
            string: The checksum of the constant streams
        """

        hash_algorithm = KNOWN_HASH_ALGORITHMS[algorithm]
        constants_bytes = bytearray()
        constant_idx = 0

        while True:
            constant_stream = 'constant ' + str(constant_idx)
            try:
                constant_val = self.inspect_virtualstream(constant_stream)
                constant_stream = "'{}' {}".format(constant_stream, constant_val)
                constants_bytes += bytes(constant_stream, 'utf-8')
            except HardwareError:
                pass
            except ValidationError as e:
                break

            constant_idx += 1

        return hash_algorithm.calculate(hash_algorithm.algorithm,
                                        constants_bytes)

    @docannotate
    def sg_metadata_checksum(self, algorithm="sha256"):
        """Calculate a checksum over the device's known metadata information
        The function calculates the checksum over the only two known and widely
        used metadata variables, which are the app tag and app version.
        Args:
            algorithm (str): The algorithm to hash the data with
        Returns:
            string: The checksum of the known metadata
        """

        hash_algorithm = KNOWN_HASH_ALGORITHMS[algorithm]
        metadata_bytes = bytearray()

        app_info = self.app_info()
        app_tag_entry = 'app_tag: ' + str(app_info['tag'])
        app_version_entry = 'app_version: ' + str(app_info['version_string'])

        metadata_bytes += bytes(app_tag_entry, 'utf-8')
        metadata_bytes += bytes(app_version_entry, 'utf-8')

        return hash_algorithm.calculate(hash_algorithm.algorithm,
                                        metadata_bytes)

    @docannotate
    def calculate_device_checksums(self, algorithm="sha256", use_ignorelist=True):
        """Returns the checksums of all the device's important actors
        This function calculates the checksum of checksums of the different
        configurations that make up the device.
        Args:
            algorithm (str): The algorithm to hash the data with
            use_ignorelist (bool): Whether to ignore variables in checksum
        Returns:
            basic_dict: All the checksums related to the device
        """

        print("Please allow the device about 1 minute to calculate checksums.")

        hash_algorithm = KNOWN_HASH_ALGORITHMS[algorithm]
        cumulative_bytes = bytearray()

        node_checksum = self.sg_checksum(algorithm=algorithm)
        streamer_checksum = self.sg_streamer_checksum(algorithm=algorithm)
        config_checksum = self.sg_config_var_checksum(algorithm=algorithm, use_ignorelist=use_ignorelist)
        constants_checksum = self.sg_constants_checksum(algorithm=algorithm)
        metadata_checksum = self.sg_metadata_checksum(algorithm=algorithm)

        # The following order is important and must match how iotile-sgcompile
        # calculates its checksum.
        # See iotilesensorgraph/iotile/sg/graph.py::add_checksum
        cumulative_bytes += bytes(node_checksum, 'utf-8')
        cumulative_bytes += bytes(streamer_checksum, 'utf-8')
        cumulative_bytes += bytes(config_checksum, 'utf-8')
        cumulative_bytes += bytes(constants_checksum, 'utf-8')
        cumulative_bytes += bytes(metadata_checksum, 'utf-8')

        device_checksum = hash_algorithm.calculate(hash_algorithm.algorithm,
                                                   cumulative_bytes)
        return {
            'nodes': node_checksum,
            'streamers': streamer_checksum,
            'configs': config_checksum,
            'constants': constants_checksum,
            'metadata': metadata_checksum,
            'device': device_checksum
        }

    @docannotate
    def compare_device_checksum(self, checksum_address=0x2100, hash_algorithm_address=0x2101):
        """Compares the calculated checksum with the programmed checksum
        Returns:
            bool: Whether the calculated checksum matches the programmed one
        """

        programmed_checksum = self.get_programmed_checksum(checksum_address=checksum_address)
        hash_algorithm = self.get_hash_algorithm(hash_algorithm_address=hash_algorithm_address)

        calculated_checksum = self.calculate_device_checksums(algorithm=hash_algorithm)['device']

        return True if calculated_checksum == programmed_checksum else False

    @docannotate
    def get_programmed_checksum(self, checksum_address=0x2100):
        """Returns the checksum that was programmed into its config var
        Returns:
            string: The checksum programmed into the variable
        """

        num_vars, = self.rpc(0x2a, 0x0b, result_format="L")

        for i in range(1, num_vars + 1):
            config_desc = self.inspect_config_variable(i)

            if config_desc.name == checksum_address:
                return config_desc.data.decode('utf-8')

        return

    @docannotate
    def get_hash_algorithm(self, hash_algorithm_address=0x2101):
        """Returns the hash algorithm that was programmed into its config var
        Returns:
            string: The hash algorithm used
        """

        num_vars, = self.rpc(0x2a, 0x0b, result_format="L")

        for i in range(1, num_vars + 1):
            config_desc = self.inspect_config_variable(i)

            if config_desc.name == hash_algorithm_address:
                return config_desc.data.decode('utf-8')

        return

    @param("node", "fw_graphnode", desc="SensorGraphNode object to add to the sensor graph")
    def add_node(self, node):
        """
        Add a node to the sensor graph.
        """

        descriptor = node.create_descriptor()

        if self.saving_script:
            self.ascii_script.append("add_node {%s}" % node.ascii)
            self.bin_script.append((0x2003, descriptor))

        if self.no_exec:
            return

        error, = self.rpc(0x20, 0x03, descriptor, result_format="L")

        if error != 0:
            raise HardwareError("Error adding node to sensor graph", code=error)

    @param("stream", "fw_stream", desc="Stream to send")
    @param("tile", "fw_tileselector", desc="Tile to stream readings to")
    @param("automatic", "bool", desc="Should streamer fire whenever there are readings?")
    @param("format", "string", desc="Format in which to package readings for streaming")
    @param("type", "string", desc="Type of stream to open ('broadcast', 'telegram', 'synchronous'")
    @param("withother", "integer", desc="Trigger this streamer when another streamer triggers")
    def add_streamer(self, stream, tile, automatic, format, type, withother=0xFF):
        """
        Add a streamer to the senor graph with default backoff properties
        """

        types = {'broadcast': 1, 'telegram': 1<<1, 'synchronous': 1<<2}
        formats = {'individual': 0, 'hashedlist': 1, 'signedlist_userkey': 2, 'signedlist_devicekey': 3}

        type_code = types[type]
        format_code = formats[format]

        if automatic and withother != 0xFF:
            raise ArgumentError("You cannot specify both automatic and withother for a streamer trigger")

        trigger = 0
        if automatic:
            trigger = 1
        elif withother != 0xFF:
            if withother >= 8 or withother < 0:
                raise ArgumentError("Invalid argument for withother.  You must specify a streamer number between 0 and 7 inclusive")

            trigger = (1 << 7) | withother

        args = struct.pack("<8sHBBB", tile.raw_data, stream.id, trigger, format_code, type_code)

        if self.saving_script:
            self.ascii_script.append("add_streamer {%s, %s, %s, %s, %s, %d}" % (str(stream), str(tile), str(automatic), str(format), str(type), withother))
            self.bin_script.append((0x2007, args))

        if self.no_exec:
            return

        error, = self.rpc(0x20, 0x07, args, result_format="L")
        if error != 0:
            raise HardwareError("Error adding streamer", code=error, stream=stream)

    @param("stream", "fw_stream", desc="Constant stream to set")
    @param("value", "integer", desc="Value to store")
    def set_constant(self, stream, value):
        """
        Set the value of a constant stream
        """

        if stream.type != stream.ConstantType:
            raise ValidationError("You can only call set_constant on constant streams")

        self.push_reading(stream, value)

    @annotated
    def clear(self):
        """
        Clear all stored readings in the sensor graph
        """

        if self.saving_script:
            self.ascii_script.append("clear")
            self.bin_script.append((0x200c, ""))

        if self.no_exec:
            return

        error, = self.rpc(0x20, 0x0c, result_format="L")
        if error != 0:
            raise HardwareError("Error clearing readings from flash", code=error)

    @param("ingraph", "path", "readable", desc="Path to the ascii sensor graph file to load")
    @param("outgraph", "path", "writeable", desc="Path to the binary sensor graph file to save")
    def convert_to_binary(self, ingraph, outgraph):
        """Convert an ascii sensorgraph file into a binary sensorgraph file
        """

        self.capture_graph(noexec=True)
        self.load_from_file(ingraph)
        self.save_graph(outgraph, binary=True)

    @param("graph", "path", "readable", desc="Path to the ascii sensor graph file to load")
    def load_from_file(self, graph):
        """Load a sensor graph from an ASCII file and upload to the device

        NB: No commands other than what is in the file are executed.  If the file
            does not include a reset command, this graph will be additive rather than
            replacing what may already be in the device.
        """

        with open(graph, "rb") as f:
            lines = f.readlines()

        if len(lines) < 3:
            raise DataError("Invalid sensorgraph file that did not have a header")

        header = lines[0].rstrip()
        version = lines[1].rstrip()
        filetype = lines[2].rstrip()

        if header != "Sensor Graph":
            raise DataError("Invalid sensorgraph file that had an unknown header", expected="Sensor Graph", read=header)

        if version != "Format: 1.0":
            raise DataError("Unknown sensorgraph file version", expected="Format: 1.0", read=version)

        if filetype != "Type: ASCII":
            raise DataError("Sensorgraph file is not in ascii format", excepted="Type: ASCII", read=filetype)

        cmds = [x.strip() for x in lines[3:] if not x.startswith('#') and not x.strip() == ""]

        for cmd in cmds:
            name, _, arg = cmd.partition(" ")

            if len(arg) > 0:
                if arg[0] != '{' or arg[-1] != '}':
                    raise DataError("Invalid command in sensorgraph file, argument is not contained in { and }", arg=arg, cmd=name)

                arg = arg[1:-1]

            if name == 'clear':
                self.clear()
            elif name == 'reset':
                self.reset()
            elif name == 'persist':
                self.persist()
            elif name == 'set_online':
                arg = arg.lower()
                if arg not in ['true', 'false']:
                    raise DataError("Invalid boolean in sensorgraph file", expected="true|false", read=arg, cmd=name)

                if arg == 'true':
                    arg = True
                else:
                    arg = False

                self.set_online(arg)
            elif name == 'add_node':
                self.add_node(arg)
            elif name == 'add_streamer':
                parts = [x.strip() for x in arg.split(",")]
                if len(parts) != 6:
                    raise DataError("There must be six arguments to add_streamer", args=arg)

                stream, dest, auto, packet, usage, trigger = parts
                auto = auto.lower()
                if auto not in ['true', 'false']:
                    raise DataError("Invalid boolean in sensorgraph file", expected="true|false", read=auto, cmd=name)

                self.add_streamer(stream, dest, auto, packet, usage, trigger)
            elif name == 'push_reading':
                parts = [x.strip() for x in arg.split(",")]
                if len(parts) != 2:
                    raise DataError("There must be two arguments to push_reading", args=arg)

                stream, value = parts
                self.push_reading(stream, value)
            else:
                raise DataError("Unsupported command in sensorgraph file", cmd=name)

    @annotated
    def reset(self):
        """
        Clear the sensor graph from RAM and flash
        """

        if self.saving_script:
            self.ascii_script.append("reset")
            self.bin_script.append((0x200d, ""))

        if self.no_exec:
            return

        error, = self.rpc(0x20, 0x0d, result_format="L")
        if error != 0:
            raise HardwareError("Error resetting sensor graph", code=error)

    @annotated
    def persist(self):
        """
        Save the current sensor graph to flash so that runs on powerup
        """

        if self.saving_script:
            self.ascii_script.append("persist")
            self.bin_script.append((0x200e, ""))

        if self.no_exec:
            return

        error, = self.rpc(0x20, 0x0e, result_format="L")
        if error != 0:
            raise HardwareError("Error persisting sensor graph", code=error)

    @return_type("fw_streamerstatus")
    @param("index", "integer", desc="Streamer to query")
    def query_streamer(self, index):
        res = self.rpc(0x20, 0x0a, index, result_type=(0, True))

        #Check if we got an error
        if len(res['buffer']) == 4:
            error, = unpack("<L", res['buffer'])
            raise HardwareError("Could not query streamer", error=error)

        return StreamerStatus(res['buffer'])

    @param("index", "integer", desc="Streamer to acknowledge readings from")
    @param("highest", "integer", desc="Highest received reading to acknowledge")
    @param("force", "bool", desc="Forcibly update the streamer even if highest is lower than what streamer has")
    @return_type("integer")
    def acknowledge_streamer(self, index, highest, force=False):
        """Acknowledge the successful receipt of readings from a streamer

        This acknowledgement allows the streamer to update its internal pointer
        to move beyond the acknowledged readings and stop trying to send them.
        """

        params = struct.pack("<HHL", index, force, highest)
        error, = self.rpc(0x20, 0x0f, params, result_format="L")
        return error

    @return_type("integer")
    def highest_id(self):
        """Fetch the highest id that has been assigned to a reading
        """

        error, reading = self.rpc(0x20, 0x11, result_format="LL")
        if error != 0:
            raise HardwareError("Error fetching highest reading ID", error_code=error)

        return reading

    @return_type("integer")
    @param("stream", "fw_stream", desc="Stream to push reading into")
    @param("value", "integer", desc="Value to push")
    def input(self, stream, value):
        params = struct.pack("<LH", value, stream.id)

        error, = self.rpc(0x20, 0x04, params, result_format="L")
        return error

    def set_online(self, online):
        """
        Change the online status of the sensor graph
        """

        if self.saving_script:
            arg = struct.pack("<H", int(online))
            self.ascii_script.append("set_online {%s}" % (str(online)))
            self.bin_script.append((0x2005, arg))

        if self.no_exec:
            return

        error, = self.rpc(0x20, 0x05, bool(online), result_format="L")
        if error != 0:
            raise HardwareError("Error adding node to sensor graph", code=error)

    @param("index", "integer", desc="Streamer to trigger")
    def trigger_streamer(self, index):
        """Change the online status of the sensor graph."""

        error, = self.rpc(0x20, 0x10, index, result_format="L")
        if error != 0:
            raise HardwareError("Error triggering streamer", code=error)

    @param("stream", "fw_stream", desc="Stream to download")
    @param("reading_id", "integer", desc="Reading id to start with")
    @return_type("integer")
    def count_stream(self, stream, reading_id=0):
        """Count the number of readings available in a stream."""

        err1, err2, count, _ = self.rpc(0x20, 0x08, stream.id, result_format="LLLL")

        if err1:
            raise HardwareError("Could not initialize stream download", error=err1)
        if err2:
            raise HardwareError("Could not initialize stream download", error=err2)

        if reading_id != 0:
            args = struct.pack("<L", reading_id)
            err1, err2, count = self.rpc(0x20, 0x12, args, result_format="LLL")

            if err1:
                raise HardwareError("Could not seek stream to specified id", error=err1, source='seek')
            if err2:
                raise HardwareError("Could not count available readings in seeked stream", error=err2, source='count')

        return count

    @param("tick_index", "integer", desc="The user tick to fetch")
    @return_type("integer")
    def user_tick(self, tick_index):
        """Get the currently configured interval of a user tick.

        The possible tick indices you can pass are 0, 1 or 2 currently.
        Tick 0 is the internal configurable high speed tick that is set
        by the sensor graph compiler to 1 second when in use.  It cannot
        be updated during normal operation.

        Ticks 1 and 2 are user configurable and may be dynamically adjusted
        during operation by calling set_user_tick(1 or 2, <new value>).  The
        value needs to be an integer number of seconds between ticks with 0
        disabling the tick.
        """

        err, value = self.rpc(0x20, 0x14, tick_index, result_format="LL")
        if err:
            raise HardwareError("Error getting user tick value", tick_index=tick_index, error=err)

        return value

    @param("tick_index", "integer", desc="The user tick to set")
    @param("value", "integer", desc="The time interval to set in seconds (0 disables the tick)")
    def set_user_tick(self, tick_index, value):
        """Temporarily update the value of a user tick.

        You should only update the value of user ticks 1 and 2.  Changing the
        value of internal tick 0 is not supported and may result in undefined
        behavior since this tick is used internally by the sensor graph compiler
        and assumed to have a fixed value.

        These changes are not persistent but will take effect immediately without
        needing a reset.  Changing the permanent value of the user tick should be
        done with the appropriate config variable.
        """

        err, = self.rpc(0x20, 0x15, value, tick_index, arg_format="LH", result_format="L")
        if err:
            raise HardwareError("Error setting user tick value", tick_index=tick_index, value=value, error=err)

    @param("stream", "fw_stream", desc="Stream to download")
    @param("reading_id", "integer", desc="Reading id to seek")
    @param("include_all", "bool", desc="Include unique reading ids and actual stream in result")
    @param("require_all", "bool", desc="Raise an exception if we are not able to download reading ids and stream numbers")
    @return_type("list(fw_reading)")
    def download_stream(self, stream, reading_id=0, include_all=True, require_all=False):
        """Download all readings in the sensor graph log matching the given stream."""

        err1, err2, count, device_time = self.rpc(0x20, 0x08, stream.id, result_format="LLLL")
        current_time = datetime.datetime.now()

        if err1:
            raise HardwareError("Could not initialize stream download", error=err1)
        if err2:
            raise HardwareError("Could not initialize stream download", error=err2)

        if reading_id != 0:
            args = struct.pack("<L", reading_id)
            err1, err2, count = self.rpc(0x20, 0x12, args, result_format="LLL")
            if err1:
                raise HardwareError("Could not seek stream to specified id", error=err1, source='seek')
            if err2:
                raise HardwareError("Could not count available readings in seeked stream", error=err2, source='count')

        #Initialize progress bar based on the count
        prog = ProgressBar("Downloading %d readings" % count, count)

        prog.start()

        readings = []
        for i in range(0, count):
            unique_id = IOTileReading.InvalidReadingID
            act_stream = stream.id

            # For backwards compatibility, we need to handle the case where the device does not
            # support giving us a new style output and try to fallback on the old RPC.  The
            # user can decide to force new style output and raise if they will not get unique id
            # and stream information.
            res = self.rpc(0x20, 0x09, int(include_all), arg_format="B", result_type=(0, True))
            if len(res['buffer']) == 12:
                err, timestamp, reading = struct.unpack("<LLL", res['buffer'])
            elif len(res['buffer']) == 20:
                err, timestamp, reading, unique_id, act_stream = struct.unpack("<LLLLH2x", res['buffer'])
            else:
                raise HardwareError("Unknown result format from dump stream RPC 0x2009, did not conform to either v0 or v1 format", result_length=len(res['buffer']))

            if len(res['buffer']) == 12 and include_all is True and require_all is True:
                raise HardwareError("Device firmware did not implement new download_stream format and new format was explicitly required (require_all=True)")

            if err:
                break

            time_base = current_time - datetime.timedelta(seconds=device_time)
            iotile_reading = IOTileReading(timestamp, act_stream, reading, time_base, reading_id=unique_id)

            readings.append(iotile_reading)
            prog.progress(i)

        prog.end()

        return readings

    @param("stream", "fw_stream", desc="Virtual stream to inspect")
    @return_type("integer")
    def inspect_virtualstream(self, stream):
        err, reading = self.rpc(0x20, 0x0b, stream.id, result_format="LL")

        if err != 0:
            raise HardwareError("Error inspecting virtual stream", code=err, stream=stream)

        return reading

    @param("uuid", "integer", desc="new UUID of device")
    def set_uuid(self, uuid):
        """
        Set or update the UUID of this device
        """

        error, = self.rpc(0x20, 0x06, uuid, result_format="L")
        if error != 0:
            raise HardwareError("Error setting UUID", code=error, uuid=uuid)

    @return_type("basic_dict")
    def os_info(self):
        """Return the OS tag and version of this device.

        The OS tag uniquely identifies the hardware and firmware combination
        that is running on this IOTile device.  The version is an X.Y value
        that identifies which particular release of that hardware/firmware
        is running.

        Normal semantic versioning applies so major releases are backwards
        incompatible and minor releases are backwards compatible.

        See the documentation on _parse_version for a description of all of
        the fields that are returned by this function.
        """

        os_data, = self.rpc(0x10, 0x08, result_format="12xL4x")
        return self._parse_version(os_data)

    @return_type("basic_dict")
    def app_info(self):
        """Return the app tag and version of this device.

        The app tag uniquely identifies the sensorgraph and application that
        this device is supposed to be performing.

        Normal semantic versioning applies so major releases are backwards
        incompatible and minor releases are backwards compatible.

        See the documentation on _parse_version for a description of all of
        the fields that are returned by this function.
        """

        app_data, = self.rpc(0x10, 0x08, result_format="16xL")
        return self._parse_version(app_data)

    @classmethod
    def _parse_version(cls, tag_data):
        """Parse a packed version info struct into tag and major.minor version.

        The tag and version are parsed out according to 20 bits for tag and
        6 bits each for major and minor.  The more interesting part is the
        blacklisting performed for tags that are known to be untrustworthy.

        In particular, the following applies to tags.

        - tags < 1024 are reserved for development and have only locally defined
          meaning.  They are not for use in production.
        - tags in [1024, 2048) are production tags but were used inconsistently
          in the early days of Arch and hence cannot be trusted to correspond with
          an actual device model.
        - tags >= 2048 are reserved for supported production device variants.
        - the tag and version 0 (0.0) is reserved for an unknown wildcard that
          does not convey any information except that the tag and version are
          not known.
        """

        tag = tag_data & ((1 << 20) - 1)

        version_data = tag_data >> 20
        major = (version_data >> 6) & ((1 << 6) - 1)
        minor = (version_data >> 0) & ((1 << 6) - 1)

        return {
            'tag': tag,
            'version_string': "%d.%d" % (major, minor),
            'tag_string': "%d (%d.%d)" % (tag, major, minor),
            'major_version': major,
            'minor_version': minor,
            'version_known': major > 0 or minor > 0,
            'prerelease': major == 0,
            'production': tag >= 2048,
            'development': tag < 1024,
            'untrustworthy': (tag >= 1024 and tag < 2048) or tag == 0
        }

    @annotated
    def enable(self):
        """
        Enable the currently programmed sensor graph
        """

        self.set_online(True)

    @annotated
    def disable(self):
        """
        Disable the currently programmed sensor graph
        """

        return self.set_online(False)

    @param("stream", "fw_stream", desc="Stream to push reading into")
    @param("value", "integer", desc="Value to store")
    def push_reading(self, stream, value):
        args = struct.pack("<LH", value, stream.id)

        if self.saving_script:
            self.ascii_script.append("push_reading {%s, %d}" % (str(stream), value))
            self.bin_script.append((0x2000, args))

        if self.no_exec:
            return

        error, = self.rpc(0x20, 0x00, args, result_format="L")

        if error != 0:
            raise HardwareError("Error pushing reading to stream", code=error)

    @param("stream", "fw_stream", desc="Stream to push reading into")
    @param("value", "integer", desc="Value to store")
    @param("count", "integer", desc="The number of readings to push")
    def push_many(self, stream, value, count):
        """ push_many: Pushes many copies of a value into a stream efficiently"""
        args = struct.pack("<LLH", value, count, stream.id)

        timeout = max(5.0, count/100.)
        error, pushed = self.rpc(0x20, 0x13, args, result_format="LL", timeout=timeout)

        if error != 0:
            raise HardwareError("Error pushing reading to stream", code=error)

    @param("stream", "fw_stream", desc="Stream to push reading into")
    @param("valuelist", "list(integer)", desc="List of values to store")
    def push_list(self, stream, valuelist):
        """ push_list: Pushes a list of values into a stream. This is
        useful to upload a dataset into the pod for processing and testing"""
        for v in valuelist:
            self.push_reading(stream, v)


    @param("stream", "fw_stream", desc="Stream on which to perform summary function")
    @param("function", "string", ["list", ["noop","min","max","sum","avg","median","variance","in_window_cnt", "count", "uid_range"]], desc="Summarizing function to run")
    @param("start_param", "string", ["list", ["first", "id","offset"]], desc="Parameter for start condition")
    @param("stop_param" , "string", ["list", ["last", "id","offset"]] , desc="Parameter for stop condition")
    @param("start_val", "integer", desc="Value of start condition for calculation")
    @param("stop_val", "integer", desc="Value of stop condition for calculation")
    @param("arg0", "integer", desc="Argument 0 of summarizing function")
    @param("arg1", "integer", desc="Argument 1 of summarizing function")
    @return_type("basic_dict")
    def summarize_stream(self, stream, function="noop", \
        start_param="first", stop_param="last", start_val=0, stop_val=0, arg0=0, arg1=0):
        """ Performs a summarizing function over data in the Raw Sensor Log
            The function is implemented in firmware and can be executed on the controller over the data
            that is currently stored in the RawSensorLog.

            A start condition is present and the firmware will seek to the start position indicated
            before commencing the summary function. The summary function is then performed sequentially on all data
            in the RSL until the end condition is met. Once the end condition is met the summary function returns
            the value.

            Start/Stop Conditions:
                `start_param`, `stop_param - Identifies the starting/ending parameter as:
                        - The ID of the reading
                        - The Offset of the reading
                        - Or (as default) the first/last entry of the stream

                `start`, `stop` - Identifies the value of the starting parameter to initiate the summary function
                    This is ignored if 'first' is selected as the start_param


            Functions currently supported w/ arguments (arg0, arg1)
                - `noop()`: A null operation. 0 is returned
                - `max()`: Finds the maximum value of a function
                - `min()`: Finds the minimum value of a function
                - `sum()` : Sum all values
                - `avg()` : Average of all values
                - `median()` : Median of all values
                - `variance()` : Variance of data
                - `in_window_cnt(lo_bound, hi_bound)`: Counts the number of items in a given window

            MORE DETAIL TBD
        """
        startflags = {
            "first": 0,
            "id": 1,
            "offset": 2
        }
        stopflags = {
            "last": 0,
            "id": 1,
            "offset": 2
        }

        start_stop_flags = (stopflags.get(stop_param) << 2) | startflags.get(start_param)

        funccodes = {
            "noop"              : 0,
            "max"               : 1,
            "min"               : 2,
            "in_window_cnt"     : 3,
            "sum"               : 4,
            "avg"               : 5,
            "median"            : 6,
            "variance"          : 7,
            "count"             : 8,
            "uid_range"         : 9

        }

        args = struct.pack("<HBBLLLL", stream.id, funccodes.get(function), start_stop_flags, start_val, stop_val, arg0, arg1 )
        err, value0, value1 = self.rpc(0x20, 0x18, args, result_format="LLL")

        result = {}
        result['error'] = err
        result['value0'] = value0
        result['value1'] = value1
        return result


def _parse_ignoreconfigs(ignoreconfigs_bytes):
    """"""

    ignoreconfigs_str = ignoreconfigs_bytes.decode('utf-8')
    configs_ignorelist = []

    if ignoreconfigs_str[0] != '{' and ignoreconfigs_str[-1] != '}':
        ignoreconfigs_str = '{' + ignoreconfigs_str + '}'

    ignoreconfigs_dict = eval(ignoreconfigs_str)

    for target, config_ids in ignoreconfigs_dict.items():
        for config_id in config_ids:
            configs_ignorelist.append((target, config_id))

    return configs_ignorelist


def _is_ignored_config(ignore_configs, slot, config_var):
    """Checks if an entry is in the list of variables to ignore"""

    for ignore_config in ignore_configs:
        if slot == ignore_config[0] and config_var == ignore_config[1]:
            return True

    return False