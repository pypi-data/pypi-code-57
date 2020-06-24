"""
Monitors the read data to determine when to publish cloud events
"""


class DeviceMonitor:
    """
    Class that monitors all connected devices and publishes data based on
    """

    def __init__(self, scheduler):
        self._devices = []
        self._data_retention = None
        self.scheduler = scheduler

    def store_data_for(self, samples=3600):
        """
        Sets the limit of how many samples to locally store data read from devices before it is purged from the buffers.
        :param samples:
        :return:
        """
        self._data_retention = samples

    def purge_data(self):
        """
        Purges data samples exceeding the amount set with store_data_for
        This needs to be scheduled or explicitly called in order to free up readings
        :return:
        """
        for device in self._devices:
            for dev_id, field, data in device.iter_data():
                data[:] = data[-self._data_retention:]

    def add_devices(self, *devices):
        self._devices.extend(devices)

    def iter_data(self):
        for device in self._devices:
            yield from device.iter_data()


class CloudMonitor:
    """
    Class that monitors the cloud events to trigger device communication
    """
