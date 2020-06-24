import logging
import threading
from functools import wraps
from pymodbus.client.sync import ModbusSerialClient, ModbusTcpClient
from pyaware.resources import Resource

log = logging.getLogger(__name__)


def get(protocol):
    protocols = {
        "modbus-rtu": ModbusRTU
    }
    return protocols[protocol]


class ModbusBase(Resource):
    def read_coils(self, address, count=1, priority=10, unit=0):
        """

        :param address: The starting address to read from
        :param count: The number of coils to read
        :param unit: The slave unit this request is targeting
        :param priority: The priority of this command. 1 is highest, higher is lower
        :returns: A future promising a deferred response handle
        """
        return self.executor.submit(priority,
                                    self.resource.read_coils,
                                    fn_args=(address, count),
                                    fn_kwargs={"unit": unit})

    def read_discrete_inputs(self, address, count=1, priority=10, unit=0):
        """

        :param address: The starting address to read from
        :param count: The number of discretes to read
        :param unit: The slave unit this request is targeting
        :param priority: The priority of this command. 1 is highest, higher is lower
        :returns: A future promising a deferred response handle
        """
        return self.executor.submit(priority,
                                    self.resource.read_discrete_inputs,
                                    fn_args=(address, count),
                                    fn_kwargs={"unit": unit})

    def write_coil(self, address, value, priority=10, unit=0):
        """

        :param address: The starting address to write to
        :param value: The value to write to the specified address
        :param unit: The slave unit this request is targeting
        :param priority: The priority of this command. 1 is highest, higher is lower
        :returns: A future promising a deferred response handle
        """
        return self.executor.submit(priority,
                                    self.resource.write_coil,
                                    fn_args=(address, value),
                                    fn_kwargs={"unit": unit})

    def write_coils(self, address, values, priority=10, unit=0):
        """

        :param address: The starting address to write to
        :param values: The values to write to the specified address
        :param unit: The slave unit this request is targeting
        :param priority: The priority of this command. 1 is highest, higher is lower
        :returns: A future promising a deferred response handle
        """
        return self.executor.submit(priority,
                                    self.resource.write_coils,
                                    fn_args=(address, values),
                                    fn_kwargs={"unit": unit})

    def write_register(self, address, value, priority=10, unit=0):
        """

        :param address: The starting address to write to
        :param value: The value to write to the specified address
        :param unit: The slave unit this request is targeting
        :param priority: The priority of this command. 1 is highest, higher is lower
        :returns: A future promising a deferred response handle
        """
        return self.executor.submit(priority,
                                    self.resource.write_register,
                                    fn_args=(address, value),
                                    fn_kwargs={"unit": unit})

    def write_registers(self, address, values, priority=10, unit=0):
        """

        :param address: The starting address to write to
        :param values: The values to write to the specified address
        :param unit: The slave unit this request is targeting
        :param priority: The priority of this command. 1 is highest, higher is lower
        :returns: A future promising a deferred response handle
        """
        return self.executor.submit(priority,
                                    self.resource.write_registers,
                                    fn_args=(address, values),
                                    fn_kwargs={"unit": unit})

    def read_holding_registers(self, address, count=1, priority=10, unit=0):
        """

        :param address: The starting address to read from
        :param count: The number of registers to read
        :param unit: The slave unit this request is targeting
        :param priority: The priority of this command. 1 is highest, higher is lower
        :returns: A future promising a deferred response handle
        """
        return self.executor.submit(priority,
                                    self.resource.read_holding_registers,
                                    fn_args=(address, count),
                                    fn_kwargs={"unit": unit})

    def read_input_registers(self, address, count=1, priority=10, unit=0):
        """

        :param address: The starting address to read from
        :param count: The number of registers to read
        :param unit: The slave unit this request is targeting
        :param priority: The priority of this command. 1 is highest, higher is lower
        :returns: A future promising a deferred response handle
        """
        return self.executor.submit(priority,
                                    self.resource.read_input_registers,
                                    fn_args=(address, count),
                                    fn_kwargs={"unit": unit})

    def readwrite_registers(self, *args, priority=10, unit=0):
        """

        :param read_address: The address to start reading from
        :param read_count: The number of registers to read from address
        :param write_address: The address to start writing to
        :param write_registers: The registers to write to the specified address
        :param unit: The slave unit this request is targeting
        :param priority: The priority of this command. 1 is highest, higher is lower
        :returns: A future promising a deferred response handle
        """
        return self.executor.submit(priority,
                                    self.resource.readwrite_registers,
                                    fn_args=args,
                                    fn_kwargs={"unit": unit})

    def mask_write_register(self, *args, priority=10, unit=0):
        """

        :param address: The address of the register to write
        :param and_mask: The and bitmask to apply to the register address
        :param or_mask: The or bitmask to apply to the register address
        :param unit: The slave unit this request is targeting
        :param priority: The priority of this command. 1 is highest, higher is lower
        :returns: A future promising a deferred response handle
        """
        return self.executor.submit(priority,
                                    self.resource.mask_write_register,
                                    fn_args=args,
                                    fn_kwargs={"unit": unit})


class ModbusRTU(ModbusBase):
    def __init__(self, port: str, stopbits: int, bytesize: int, parity: str, baudrate: int, timeout=3,
                 strict: bool = False):
        """
        :param port: The serial port to attach to
        :param stopbits: The number of stop bits to use
        :param bytesize: The bytesize of the serial messages
        :param parity: Which kind of parity to use
        :param baudrate: The baud rate to use for the serial device
        :param timeout: The timeout between serial requests
        :param strict:  Use Inter char timeout for baudrates <= 19200 (adhere
        """
        resource = ModbusSerialClient(
            method="rtu",
            port=port,
            stopbits=stopbits,
            bytesize=bytesize,
            parity=parity,
            baudrate=baudrate,
            timeout=timeout,
            strict=strict
        )
        super().__init__(resource=resource, max_threads=1)


class ModbusTCP(ModbusBase):
    def __init__(self, host, port, max_threads=1):
        self.lock = threading.Lock()

        def locked(func):
            @wraps(func)
            def f(*args, **kwargs):
                with self.lock:
                    return func(*args, **kwargs)

            return f

        class WhyNot:
            def __init__(self, host, port):
                self.client = ModbusTcpClient(host, port)

            def __getattr__(self, item):
                return locked(getattr(self.client, item))

        resource = ModbusTcpClient(host, port)
        super().__init__(resource, max_threads=max_threads)


if __name__ == "__main__":
    import logging
    import time


    logging.basicConfig(level=logging.DEBUG)

    def fut_thing(fut):
        print(fut.result().registers)


    res = ModbusRTU(port="COM14", stopbits=1, bytesize=8, parity="N", baudrate=19200)
    # res = ModbusTCP(port=502, host="127.0.0.1", max_threads=5)
    # print(res.read_holding_registers(0, unit=2).result().registers)
    # print(res.read_holding_registers(1, unit=1).result().registers)
    # print(res.read_holding_registers(2, unit=0).result().registers)
    # print(res.read_holding_registers(3).result().registers)
    # print(res.read_holding_registers(4).result().registers)
    # print(res.read_holding_registers(5).result().registers)
    # print(res.read_holding_registers(6).result().registers)
    # print(res.read_holding_registers(7).result().registers)
    # print(res.read_holding_registers(8).result().registers)
    # print(res.read_holding_registers(9).result().registers)
    # print(res.read_holding_registers(0).result().registers)
    resp = []
    for x in range(3):
        resp.extend([res.read_holding_registers(address=addr, unit=x, priority=10 - x) for addr in
                     range(10)])
    # import time
    import concurrent.futures

    # print([res.result().registers for res in resp])
    #
    # # resp[10].cancel()
    for itm in concurrent.futures.as_completed(resp):
        try:
            print("Future responses: {}".format(itm.result().registers))
        except concurrent.futures._base.CancelledError:
            print("Cancelled")
        except BaseException as e:
            log.exception(e)
            pass
    # while True:
    #     time.sleep(1)
