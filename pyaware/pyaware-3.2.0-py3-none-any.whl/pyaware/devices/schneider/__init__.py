from pyaware.devices.definitions import ModbusRTU, ModbusHolding, DATATYPES


class PM5110(ModbusRTU):
    read_timeout = 0.5
    data_info = {
        "current-i1": ModbusHolding(address=3000 - 1, words=2, data_type=DATATYPES.FLOAT32),
        "current-i2": ModbusHolding(address=3002 - 1, words=2, data_type=DATATYPES.FLOAT32),
        "current-i3": ModbusHolding(address=3004 - 1, words=2, data_type=DATATYPES.FLOAT32),
        "ph-n-voltage-va": ModbusHolding(address=3028 - 1, words=2, data_type=DATATYPES.FLOAT32),
        "ph-n-voltage-vb": ModbusHolding(address=3030 - 1, words=2, data_type=DATATYPES.FLOAT32),
        "ph-n-voltage-vc": ModbusHolding(address=3032 - 1, words=2, data_type=DATATYPES.FLOAT32),
        "total-active-power": ModbusHolding(address=3060 - 1, words=2, data_type=DATATYPES.FLOAT32, scale=1000),
        "total-apparent-power": ModbusHolding(address=3076 - 1, words=2, data_type=DATATYPES.FLOAT32, scale=1000),
        "total-power-factor": ModbusHolding(address=3084 - 1, words=2, data_type=DATATYPES.FLOAT32, nan_convert=0),
        "total-positive-energy": ModbusHolding(address=3204 - 1, words=4, data_type=DATATYPES.UINT64),
        "frequency": ModbusHolding(address=3110 - 1, words=2, data_type=DATATYPES.FLOAT32)
    }


class PM710(ModbusRTU):
    read_timeout = 0.5
    data_info = {
        "current-i1": ModbusHolding(address=1034 - 1, words=2, data_type=DATATYPES.FLOAT32),
        "current-i2": ModbusHolding(address=1036 - 1, words=2, data_type=DATATYPES.FLOAT32),
        "current-i3": ModbusHolding(address=1038 - 1, words=2, data_type=DATATYPES.FLOAT32),
        "ph-n-voltage-va": ModbusHolding(address=1060 - 1, words=2, data_type=DATATYPES.FLOAT32),
        "ph-n-voltage-vb": ModbusHolding(address=1062 - 1, words=2, data_type=DATATYPES.FLOAT32),
        "ph-n-voltage-vc": ModbusHolding(address=1064 - 1, words=2, data_type=DATATYPES.FLOAT32),
        "total-active-power": ModbusHolding(address=1006 - 1, words=2, data_type=DATATYPES.FLOAT32, scale=1000),
        "total-apparent-power": ModbusHolding(address=1008 - 1, words=2, data_type=DATATYPES.FLOAT32, scale=1000),
        "total-power-factor": ModbusHolding(address=4048 - 1, words=1, data_type=DATATYPES.SINT16, scale=0.001, nan_convert=0),
        "total-positive-energy": ModbusHolding(address=1000 - 1, words=2, data_type=DATATYPES.FLOAT32, scale=1000),
        "frequency": ModbusHolding(address=1020 - 1, words=2, data_type=DATATYPES.FLOAT32),
        "current-a-thd": ModbusHolding(address=4045 - 1, words=1, data_type=DATATYPES.UINT16, scale=0.1),
        "current-b-thd": ModbusHolding(address=4046 - 1, words=1, data_type=DATATYPES.UINT16, scale=0.1),
        "current-c-thd": ModbusHolding(address=4047 - 1, words=1, data_type=DATATYPES.UINT16, scale=0.1),
        "voltage-a-n-thd": ModbusHolding(address=4049 - 1, words=1, data_type=DATATYPES.UINT16, scale=0.1),
        "voltage-b-n-thd": ModbusHolding(address=4050 - 1, words=1, data_type=DATATYPES.UINT16, scale=0.1),
        "voltage-c-n-thd": ModbusHolding(address=4051 - 1, words=1, data_type=DATATYPES.UINT16, scale=0.1)
    }
