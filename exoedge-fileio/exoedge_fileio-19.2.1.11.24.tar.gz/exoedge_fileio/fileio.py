#pylint: disable=C0103,W1202

from __future__ import print_function
import time as _time
from exoedge.sources import ExoEdgeSource
from exoedge import logger
from threading import Thread

SUCCESSFUL_READ = 0
ERR_FILE_NOT_FOUND = 1
ERR_EMPTY_FILE = 2

APPLICATION_NAME = "FileIO"

LOG = logger.getLogger(__name__)

try:
    from sys_info import *
except ImportError:
    LOG.warning("Unable to import psutil. Please install in order to use the sys_info ExoEdge source.")


class FileioExoEdgeSource(ExoEdgeSource):
    def run(self):
        while not self.is_stopped():
            while not self._Q_DATA_OUT.empty():
                obj = self._Q_DATA_OUT.safe_get(timeout=0.1)
                if obj:
                    LOG.critical(
                         "ARJ: Processing data_out on channel {} with value {}"
                        .format(obj.channel, obj.data_out_value)
                    )

                    thread = Thread(target = self.handle_data_out, args=(obj,))
                    thread.start()

            for channel in self.get_channels_by_application(APPLICATION_NAME):
                if channel.is_sample_time():
                    LOG.warning("ARJ: sample_time for: {}" .format(channel.name))
                    input_file = channel.protocol_config.app_specific_config['input_file']
                    last_line, return_code = self.read_last_line_of_file(input_file)

                    if return_code == SUCCESSFUL_READ:
                        try:
                            channel.put_sample(last_line)
                        except Exception as exc: #pylint: disable=W0703
                            LOG.exception("Exception" .format(format_exc=exc))
                            channel.put_channel_error(traceback.format_exc(exc))

                    elif return_code == ERR_FILE_NOT_FOUND:
                        channel.put_channel_error("File not found: {}" .format(input_file))

                    elif return_code == ERR_EMPTY_FILE:
                        channel.put_channel_error("File was empty: {}" .format(input_file))



            _time.sleep(0.1)

        LOG.critical("ExoFileIO EXITING!")

    # Return Codes:
    #   0 - Successfully Read File
    #   1 - File not found
    #   2 - Empty File
    def read_last_line_of_file(self, file_name):
        try:
            file_h = open(file_name, 'r')

            for line in file_h:
                pass

            last_line = line
            last_line = last_line.rstrip("\r\n") #Strips trailing whitespace/newline
            file_h.close()
            return_code = SUCCESSFUL_READ
            return last_line, return_code

        except IOError: # Name error if last_line is not assigned
            return_code = ERR_FILE_NOT_FOUND
            last_line = ""
            return last_line, return_code

        except UnboundLocalError: # Name error if last_line is not assigned
            return_code = ERR_EMPTY_FILE
            last_line = ""
            return last_line, return_code

    def handle_data_out(self, data_out_obj):
        #TODO: do I need to check application??
        #TODO: do I need to check validity of output_file?
        filename = data_out_obj.channel.protocol_config.app_specific_config['output_file']

        LOG.info("Writing data_out {} to file {}" .format(data_out_obj.data_out_value, filename))

        file_h = open(filename, 'w')
        file_h.write(str(data_out_obj.data_out_value))
        file_h.close()


