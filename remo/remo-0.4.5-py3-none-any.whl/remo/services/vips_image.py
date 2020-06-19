import pyvips
import logging

logger = logging.getLogger('remo_app')


class VipsImage:
    @staticmethod
    def from_file(path):
        try:
            return pyvips.Image.new_from_file(path, access='sequential')
        except Exception as err:
            logger.error(f'failed to open image with vips library, try to re-install vips: {err}')

    @staticmethod
    def from_buffer(data):
        try:
            return pyvips.Image.new_from_buffer(data, "access=sequential")
        except Exception as err:
            logger.error(f'failed to open image with vips library, try to re-install vips: {err}')
