from pyaware.devices.definitions import DATATYPES, ModbusHolding, ModbusInput, ModbusRTU, ModbusBitMask_Input


class M2M(ModbusRTU):
    read_timeout = 1
    data_info = {
        "current-i1": ModbusHolding(address=4112, words=2, data_type=DATATYPES.UINT32, scale=0.001),
        "current-i2": ModbusHolding(address=4114, words=2, data_type=DATATYPES.UINT32, scale=0.001),
        "current-i3": ModbusHolding(address=4116, words=2, data_type=DATATYPES.UINT32, scale=0.001),
        "voltage-a-n": ModbusHolding(address=4098, words=2, data_type=DATATYPES.UINT32),
        "voltage-b-n": ModbusHolding(address=4100, words=2, data_type=DATATYPES.UINT32),
        "voltage-c-n": ModbusHolding(address=4102, words=2, data_type=DATATYPES.UINT32),
        "total-active-power": ModbusHolding(address=4142, words=2, data_type=DATATYPES.SINT32),
        "total-apparent-power": ModbusHolding(address=4134, words=2, data_type=DATATYPES.UINT32),
        "total-power-factor": ModbusHolding(address=4118, words=2, data_type=DATATYPES.SINT32, scale=0.001),
        "total-positive-energy": ModbusHolding(address=4158, words=2, data_type=DATATYPES.UINT32, scale=0.01),
        "frequency": ModbusHolding(address=4166, words=2, data_type=DATATYPES.UINT32, scale=0.001)
    }


# Backward compatibility
ABB_M2M = M2M


class EkipELsig(ModbusRTU):
    read_timeout = 1
    data_info = {
        "status-trips": ModbusBitMask_Input(address=50, words=1, data_type=DATATYPES.UINT16, bitmask={
            "l-tripped": 0,
            "s-tripped": 1,
            "i-tripped": 2,
            "g-tripped": 3,
            "instant-tripped": 4
        }),
        "current-i1": ModbusInput(address=100, words=2, data_type=DATATYPES.UINT32, scale=0.00001),
        "current-i2": ModbusInput(address=102, words=2, data_type=DATATYPES.UINT32, scale=0.00001),
        "current-i3": ModbusInput(address=104, words=2, data_type=DATATYPES.UINT32, scale=0.00001),
        "voltage-a-n": ModbusInput(address=150, words=1, data_type=DATATYPES.UINT16),
        "voltage-b-n": ModbusInput(address=151, words=1, data_type=DATATYPES.UINT16),
        "voltage-c-n": ModbusInput(address=152, words=1, data_type=DATATYPES.UINT16),
        "total-active-power": ModbusInput(address=206, words=2, data_type=DATATYPES.SINT32, scale=0.001),
        "total-apparent-power": ModbusInput(address=222, words=2, data_type=DATATYPES.SINT32, scale=0.001),
        "total-power-factor": ModbusInput(address=253, words=1, data_type=DATATYPES.SINT16, scale=0.01),
        "total-positive-energy": ModbusInput(address=304, words=2, data_type=DATATYPES.SINT32, scale=0.001)
    }


# Backward compatibility
ABB_EKIPELSIG = EkipELsig


class Emax2(ModbusRTU):
    read_timeout = 1
    data_info = {
        "status-trips": ModbusBitMask_Input(address=50, words=1, data_type=DATATYPES.UINT16, bitmask={
            "l-tripped": 0,
            "s-tripped": 1,
            "i-tripped": 2,
            "g-tripped": 3,
            "instant-tripped": 4
        }),
        "current-i1": ModbusInput(address=100, words=2, data_type=DATATYPES.UINT32, scale=0.00001),
        "current-i2": ModbusInput(address=102, words=2, data_type=DATATYPES.UINT32, scale=0.00001),
        "current-i3": ModbusInput(address=104, words=2, data_type=DATATYPES.UINT32, scale=0.00001),
        "voltage-a-n": ModbusInput(address=150, words=1, data_type=DATATYPES.UINT16, scale=0.1),
        "voltage-b-n": ModbusInput(address=151, words=1, data_type=DATATYPES.UINT16, scale=0.1),
        "voltage-c-n": ModbusInput(address=152, words=1, data_type=DATATYPES.UINT16, scale=0.1),
        "total-active-power": ModbusInput(address=206, words=2, data_type=DATATYPES.SINT32, scale=0.01),
        "total-apparent-power": ModbusInput(address=222, words=2, data_type=DATATYPES.SINT32, scale=0.01),
        "total-power-factor": ModbusInput(address=253, words=1, data_type=DATATYPES.SINT16, scale=0.001),
        "total-positive-energy": ModbusInput(address=304, words=2, data_type=DATATYPES.SINT32, scale=0.001)
    }


# Backward compatibility
ABB_EMAX2 = Emax2
