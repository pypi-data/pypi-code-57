from pyaware.devices.definitions import ModbusRTU, ModbusHolding, DATATYPES


class I33(ModbusRTU):
    read_timeout = 0.5
    data_info = {
        "ph-n-voltage-v1": ModbusHolding(address=18444, words=2, data_type=DATATYPES.UINT32, scale=0.01),
        "ph-n-voltage-v2": ModbusHolding(address=18446, words=2, data_type=DATATYPES.UINT32, scale=0.01),
        "ph-n-voltage-v3": ModbusHolding(address=18448, words=2, data_type=DATATYPES.UINT32, scale=0.01),
        "current-i1": ModbusHolding(address=18458, words=2, data_type=DATATYPES.UINT32, scale=0.001),
        "current-i2": ModbusHolding(address=18460, words=2, data_type=DATATYPES.UINT32, scale=0.001),
        "current-i3": ModbusHolding(address=18462, words=2, data_type=DATATYPES.UINT32, scale=0.001),
        "total-active-power": ModbusHolding(address=18476, words=2, data_type=DATATYPES.SINT32),
        "total-apparent-power": ModbusHolding(address=18484, words=2, data_type=DATATYPES.UINT32),
        "total-power-factor": ModbusHolding(address=18486, words=1, data_type=DATATYPES.SINT16, scale=0.001),
        "current-i1-thd": ModbusHolding(address=18757, words=1, data_type=DATATYPES.UINT16, scale=0.01),
        "current-i2-thd": ModbusHolding(address=18758, words=1, data_type=DATATYPES.UINT16, scale=0.01),
        "current-i3-thd": ModbusHolding(address=18759, words=1, data_type=DATATYPES.UINT16, scale=0.01),
        "current-in-thd": ModbusHolding(address=18760, words=1, data_type=DATATYPES.UINT16, scale=0.01),
        "total-positive-energy": ModbusHolding(address=19841, words=2, data_type=DATATYPES.UINT32, scale=1000)
    }


class U30(ModbusRTU):
    read_timeout = 0.5
    data_info = {
        "frequency": ModbusHolding(address=36871, words=2, data_type=DATATYPES.UINT32, scale=0.001),
        "ph-n-voltage-v1": ModbusHolding(address=36873, words=2, data_type=DATATYPES.UINT32, scale=0.01),
        "ph-n-voltage-v2": ModbusHolding(address=36875, words=2, data_type=DATATYPES.UINT32, scale=0.01),
        "ph-n-voltage-v3": ModbusHolding(address=36877, words=2, data_type=DATATYPES.UINT32, scale=0.01),
        "pn-n-voltage-thd-v1": ModbusHolding(address=37144, words=1, data_type=DATATYPES.UINT16, scale=0.01),
        "pn-n-voltage-thd-v2": ModbusHolding(address=37145, words=1, data_type=DATATYPES.UINT16, scale=0.01),
        "pn-n-voltage-thd-v3": ModbusHolding(address=37146, words=1, data_type=DATATYPES.UINT16, scale=0.01),
    }


class I35(ModbusRTU):
    read_timeout = 0.5
    data_info = {
        "ph-n-voltage-v1": ModbusHolding(address=18444, words=2, data_type=DATATYPES.UINT32, scale=0.01),
        "ph-n-voltage-v2": ModbusHolding(address=18446, words=2, data_type=DATATYPES.UINT32, scale=0.01),
        "ph-n-voltage-v3": ModbusHolding(address=18448, words=2, data_type=DATATYPES.UINT32, scale=0.01),
        "current-i1": ModbusHolding(address=18458, words=2, data_type=DATATYPES.UINT32, scale=0.001),
        "current-i2": ModbusHolding(address=18460, words=2, data_type=DATATYPES.UINT32, scale=0.001),
        "current-i3": ModbusHolding(address=18462, words=2, data_type=DATATYPES.UINT32, scale=0.001),
        "total-active-power": ModbusHolding(address=18476, words=2, data_type=DATATYPES.SINT32),
        "total-apparent-power": ModbusHolding(address=18484, words=2, data_type=DATATYPES.UINT32),
        "total-power-factor": ModbusHolding(address=18486, words=1, data_type=DATATYPES.SINT16, scale=0.001),
        "current-thd-i1": ModbusHolding(address=18757, words=1, data_type=DATATYPES.UINT16, scale=0.01),
        "current-thd-i2": ModbusHolding(address=18758, words=1, data_type=DATATYPES.UINT16, scale=0.01),
        "current-thd-i3": ModbusHolding(address=18759, words=1, data_type=DATATYPES.UINT16, scale=0.01),
        "total-positive-energy": ModbusHolding(address=19843, words=2, data_type=DATATYPES.UINT32, scale=1000)
    }