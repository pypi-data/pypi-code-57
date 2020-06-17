"""
WebSwitch(Plus) from https://www.controlbyweb.com/
Refer to the manual page 73-80
"""
import pymodbus as mb
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from time import sleep


class WebSwitch:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def __enter__(self):
        self.webctrl = mb.client.sync.ModbusTcpClient(self.host, self.port)
        self.webctrl.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.webctrl.close()

    def send_write_coil(self, address, value):
        return self.webctrl.write_coil(address, value)

    def send_read_coils(self, address, count=4):
        return self.webctrl.read_coils(address, count)  # Fixed count for 2 outlets and 2 inputs

    def switch_on_outlet1(self):
        self.send_write_coil(0, 1)

    def switch_off_outlet1(self):
        self.send_write_coil(0, 0)

    def switch_on_outlet2(self):
        self.send_write_coil(1, 1)

    def switch_off_outlet2(self):
        self.send_write_coil(1, 0)


if __name__ == '__main__':
    with WebSwitch('192.168.1.2', '502') as wc:  # default address at 192.168.1.2
        print(wc.send_read_coils(0).bits)
        # for _ in range(10):
        #     print(wc.send_write_coil(0, 1 if _ % 2 == 0 else 0))
        #     print(wc.send_write_coil(1, 1 if _ % 2 == 0 else 0))
        #     sleep(5)
        wc.switch_on_outlet1()
        sleep(5)
        wc.switch_off_outlet1()
        sleep(5)
        wc.switch_on_outlet2()
        sleep(5)
        wc.switch_off_outlet2()
