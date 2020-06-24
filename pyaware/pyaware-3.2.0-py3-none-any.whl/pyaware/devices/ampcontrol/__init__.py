import asyncio
import async_timeout

from pymodbus.exceptions import ConnectionException

from pyaware.data_types import AddressMapUint16
from pyaware.devices import ModbusDevice, log, ModbusBitMask
from pyaware.devices.definitions import EIPCommands, EIPDevice, ModbusRTU, ModbusHolding, DATATYPES, EnumConverter


class IPB(ModbusRTU):

    def __init__(self, *args, unit=0, client=None, **kwargs):
        self.read_timeout = 1
        self.data_info = {
            "pilot-forward-resistance": ModbusHolding(address=4 - 1, words=1, data_type=DATATYPES.UINT16),
            "earth-leakage-current": ModbusHolding(address=3 - 1, words=1, data_type=DATATYPES.UINT16),
            "current-range-setting": ModbusHolding(address=18 - 1, words=1, data_type=DATATYPES.UINT16,
                                                   converter=EnumConverter({
                                                       1: 60,
                                                       2: 64,
                                                       3: 68,
                                                       4: 72,
                                                       5: 76,
                                                       6: 80,
                                                       7: 84,
                                                       8: 88,
                                                       9: 92,
                                                       10: 96,
                                                       11: 100,
                                                       12: 104,
                                                       13: 108,
                                                       14: 112,
                                                       15: 116
                                                   })),
            "current-multiplier-setting": ModbusHolding(address=19 - 1, words=1, data_type=DATATYPES.UINT16,
                                                        converter=EnumConverter({
                                                            1: 0.125,
                                                            2: 0.25,
                                                            3: 0.5,
                                                            4: 1,
                                                            5: 2,
                                                            6: 4
                                                        })),
            "over-current-curve": ModbusHolding(address=20 - 1, words=1, data_type=DATATYPES.UINT16,
                                                converter=EnumConverter({
                                                    1: "Vinv",
                                                    2: "m-OL"
                                                })),
            "overload-time-parameter": ModbusHolding(address=21 - 1, words=1, data_type=DATATYPES.UINT16,
                                                     converter=EnumConverter({
                                                         1: 0.05,
                                                         2: 0.075,
                                                         3: 0.1,
                                                         4: 0.15,
                                                         5: 0.2,
                                                         6: 0.3,
                                                         7: 0.4,
                                                         8: 0.5,
                                                         9: 0.6,
                                                         10: 0.7,
                                                         11: 0.9,
                                                         12: 1.0,
                                                         13: 0.04,
                                                         14: 0.03,
                                                         15: 0.02,
                                                         16: 0.015,
                                                         17: 0.01,
                                                         18: 0.005
                                                     })),
            "short-circuit-trip-parameter": ModbusHolding(address=24 - 1, words=1, data_type=DATATYPES.UINT16,
                                                          converter=EnumConverter({
                                                              1: 3.0,
                                                              2: 3.5,
                                                              3: 4.0,
                                                              4: 4.5,
                                                              5: 5.0,
                                                              6: 5.5,
                                                              7: 6.0,
                                                              8: 6.5,
                                                              9: 7.0,
                                                              10: 7.5,
                                                              11: 8.0,
                                                              12: 8.5,
                                                              13: 9.0,
                                                              14: 9.5,
                                                              15: 10.0
                                                          })),
            "short-circuit-time-parameter": ModbusHolding(address=25 - 1, words=1, data_type=DATATYPES.UINT16,
                                                          converter=EnumConverter({
                                                              1: 20,
                                                              2: 40,
                                                              3: 60,
                                                              4: 80,
                                                              5: 100
                                                          })),
            "status-register": ModbusBitMask(address=2 - 1, words=1, data_type=DATATYPES.UINT16, bitmask={
                "earth-leakage-trip": 0,
                "earth-continuity-trip": 1,
                "earth-fault-lockout": 2,
                "overload": 3,
                "short-circuit": 4,
                "mcf": 5,
                "reserved": 6,
                "running": 7,
                "relay-type": 8,
                "ipsi-ipb-comms-ok": 9,
                "fan-interlock-read": 10,
                "ipb-stop": 11,
                "ipb-reset": 12,
                "ipb-lock": 13,
                "ipb-mci": 14,
                "ipb-start": 15
            }),
            "earth-leakage-sensitivity": ModbusHolding(address=27 - 1, words=1, data_type=DATATYPES.UINT16,
                                                       converter=EnumConverter({
                                                           1: 100,
                                                           2: 150,
                                                           3: 200,
                                                           4: 250,
                                                           5: 300,
                                                           6: 350,
                                                           7: 400,
                                                           8: 450,
                                                           9: 500
                                                       })),
            "earth-leakage-time": ModbusHolding(address=28 - 1, words=1, data_type=DATATYPES.UINT16,
                                                converter=EnumConverter({
                                                    1: 0,
                                                    2: 150,
                                                    3: 190,
                                                    4: 230,
                                                    5: 270,
                                                    6: 310,
                                                    7: 350,
                                                    8: 390,
                                                    9: 430,
                                                    10: 470
                                                })),
        }
        super().__init__(*args, unit=unit, client=client, **kwargs)


class IPC(ModbusRTU):

    def __init__(self, *args, unit=0, client=None, **kwargs):
        self.read_timeout = 1
        self.data_info = {
            "pilot-forward-resistance": ModbusHolding(address=4 - 1, words=1, data_type=DATATYPES.UINT16),
            "megger-result": ModbusHolding(address=51 - 1, words=1, data_type=DATATYPES.UINT16),
            "earth-leakage-current": ModbusHolding(address=3 - 1, words=1, data_type=DATATYPES.UINT16),
            "current-range-setting": ModbusHolding(address=18 - 1, words=1, data_type=DATATYPES.UINT16),
            "current-multiplier-setting": ModbusHolding(address=19 - 1, words=1, data_type=DATATYPES.UINT16),
            "over-current-curve": ModbusHolding(address=20 - 1, words=1, data_type=DATATYPES.UINT16),
            "ol-time-parameter": ModbusHolding(address=21 - 1, words=1, data_type=DATATYPES.UINT16),
            "sc-trip-parameter": ModbusHolding(address=24 - 1, words=1, data_type=DATATYPES.UINT16),
            "sc-time-parameter": ModbusHolding(address=25 - 1, words=1, data_type=DATATYPES.UINT16),
            "status": ModbusHolding(address=2 - 1, words=1, data_type=DATATYPES.UINT16),
            "el-sensitivity": ModbusHolding(address=27 - 1, words=1, data_type=DATATYPES.UINT16),
            "el-time": ModbusHolding(address=28 - 1, words=1, data_type=DATATYPES.UINT16),
        }
        super().__init__(*args, unit=unit, client=client, **kwargs)


class IPD(ModbusRTU):
    def __init__(self, *args, unit=0, client=None, **kwargs):
        self.read_timeout = 1
        self.data_info = {
            "pilot-forward-resistance": ModbusHolding(address=4 - 1, words=1, data_type=DATATYPES.UINT16),
            "megger-result": ModbusHolding(address=51 - 1, words=1, data_type=DATATYPES.UINT16, scale=100000),
            "earth-leakage-current": ModbusHolding(address=3 - 1, words=1, data_type=DATATYPES.UINT16),
            "current-range-setting": ModbusHolding(address=18 - 1, words=1, data_type=DATATYPES.UINT16,
                                                   converter=EnumConverter({
                                                       1: 60,
                                                       2: 64,
                                                       3: 68,
                                                       4: 72,
                                                       5: 76,
                                                       6: 80,
                                                       7: 84,
                                                       8: 88,
                                                       9: 92,
                                                       10: 96,
                                                       11: 100,
                                                       12: 104,
                                                       13: 108,
                                                       14: 112,
                                                       15: 116
                                                   })),
            "current-multiplier-setting": ModbusHolding(address=19 - 1, words=1, data_type=DATATYPES.UINT16,
                                                        converter=EnumConverter({
                                                            1: 0.125,
                                                            2: 0.25,
                                                            3: 0.5,
                                                            4: 1,
                                                            5: 2,
                                                            6: 4
                                                        })),
            "over-current-curve": ModbusHolding(address=20 - 1, words=1, data_type=DATATYPES.UINT16,
                                                converter=EnumConverter({
                                                    1: "Vinv",
                                                    2: "m-OL"
                                                })),
            "overload-time-parameter": ModbusHolding(address=21 - 1, words=1, data_type=DATATYPES.UINT16,
                                                     converter=EnumConverter({
                                                         1: 0.05,
                                                         2: 0.075,
                                                         3: 0.1,
                                                         4: 0.15,
                                                         5: 0.2,
                                                         6: 0.3,
                                                         7: 0.4,
                                                         8: 0.5,
                                                         9: 0.6,
                                                         10: 0.7,
                                                         11: 0.9,
                                                         12: 1.0,
                                                         13: 0.04,
                                                         14: 0.03,
                                                         15: 0.02,
                                                         16: 0.015,
                                                         17: 0.01,
                                                         18: 0.005
                                                     })),
            "short-circuit-trip-parameter": ModbusHolding(address=24 - 1, words=1, data_type=DATATYPES.UINT16,
                                                          converter=EnumConverter({
                                                              1: 3.0,
                                                              2: 3.5,
                                                              3: 4.0,
                                                              4: 4.5,
                                                              5: 5.0,
                                                              6: 5.5,
                                                              7: 6.0,
                                                              8: 6.5,
                                                              9: 7.0,
                                                              10: 7.5,
                                                              11: 8.0,
                                                              12: 8.5,
                                                              13: 9.0,
                                                              14: 9.5,
                                                              15: 10.0
                                                          })),
            "short-circuit-time-parameter": ModbusHolding(address=25 - 1, words=1, data_type=DATATYPES.UINT16,
                                                          converter=EnumConverter({
                                                              1: 20,
                                                              2: 40,
                                                              3: 60,
                                                              4: 80,
                                                              5: 100,
                                                              6: 120,
                                                              7: 160
                                                          })),
            "status-register": ModbusBitMask(address=2 - 1, words=1, data_type=DATATYPES.UINT16, bitmask={
                "earth-leakage-trip": 0,
                "earth-continuity-trip": 1,
                "earth-fault-lockout": 2,
                "overload": 3,
                "short-circuit": 4,
                "mcf": 5,
                "insulation-fail-trip": 6,
                "running": 7,
                "reserved": 8,
                "ipsi-ipd-comms-ok": 9,
                "fan-interlock-read": 10,
                "ipd-stop": 11,
                "ipd-reset": 12,
                "ipd-lock": 13,
                "ipd-mci": 14,
                "ipd-start": 15
            }),
            "earth-leakage-sensitivity": ModbusHolding(address=27 - 1, words=1, data_type=DATATYPES.UINT16,
                                                       converter=EnumConverter({
                                                           1: 100,
                                                           2: 150,
                                                           3: 200,
                                                           4: 250,
                                                           5: 300,
                                                           6: 350,
                                                           7: 400,
                                                           8: 450,
                                                           9: 500
                                                       })),
            "earth-leakage-time": ModbusHolding(address=28 - 1, words=1, data_type=DATATYPES.UINT16,
                                                converter=EnumConverter({
                                                    1: 0,
                                                    2: 100,
                                                    3: 150,
                                                    4: 190,
                                                    5: 230,
                                                    6: 270,
                                                    7: 310,
                                                    8: 350,
                                                    9: 390,
                                                    10: 430,
                                                    11: 470
                                                })),
        }
        super().__init__(*args, unit=unit, client=client, **kwargs)


class IPM(ModbusRTU):
    def __init__(self, *args, unit=0, client=None, **kwargs):
        self.read_timeout = 1
        self.data_info = {
            "trip-word": ModbusBitMask(address=4, words=1, data_type=DATATYPES.UINT16, bitmask={
                # Trip Status 1
                "earth-leakage": 0,
                "earth-continuity-trip": 1,
                "insulat-test-trip": 2,
                "overload-trip": 3,
                "short-circuit-trip": 4,
                "current-balance-trip": 5,
                "residual-current-trip": 6,
                "main-contactor-fail": 7,
                # Trip Status 2
                "external-stop": 8,
                "rtm-offline-trip": 9,
                "ipm-memory-error": 10,
                "rtm-memory-error": 11,
                "stopped-ipm": 12,
                "modbus-timeout": 13,
                "modbus-stop": 14,
                "rtm-ct-ratio-error": 15
            }),
            "pilot-forward-resistance": ModbusHolding(address=9, words=1, data_type=DATATYPES.UINT16),
            "megger-result": ModbusHolding(address=11, words=1, data_type=DATATYPES.UINT16, scale=1000000),
            "earth-leakage-current": ModbusHolding(address=13, words=1, data_type=DATATYPES.UINT16),
            "current-range-parameter": ModbusHolding(address=47, words=1, data_type=DATATYPES.UINT16,
                                                     converter=EnumConverter(self.build_current_range())),
            "short-circuit-trip-parameter": ModbusHolding(address=48, words=1, data_type=DATATYPES.SINT16,
                                                          converter=EnumConverter({
                                                              1: 3.0,
                                                              2: 3.5,
                                                              3: 4.0,
                                                              4: 4.5,
                                                              5: 5.0,
                                                              6: 5.5,
                                                              7: 6.0,
                                                              8: 6.5,
                                                              9: 7.0,
                                                              10: 7.5,
                                                              11: 8.0,
                                                              12: 8.5,
                                                              13: 9.0,
                                                              14: 9.5,
                                                              15: 10.0
                                                          })),
            "short-circuit-time-parameter": ModbusHolding(address=49, words=1, data_type=DATATYPES.UINT16,
                                                          converter=EnumConverter({
                                                              1: 20,
                                                              2: 40,
                                                              3: 60,
                                                              4: 80,
                                                              5: 100,
                                                              6: 120,
                                                              7: 160
                                                          })),
            "overload-time-parameter": ModbusHolding(address=50, words=1, data_type=DATATYPES.UINT16,
                                                     converter=EnumConverter({
                                                         1: 3,
                                                         2: 4,
                                                         3: 5,
                                                         4: 6,
                                                         5: 7,
                                                         6: 8,
                                                         7: 10,
                                                         8: 12,
                                                         9: 14,
                                                         10: 16,
                                                         11: 20,
                                                         12: 24,
                                                         13: 28,
                                                         14: 32,
                                                         15: 40
                                                     })),
            "earth-leakage-sensitivity": ModbusHolding(address=57, words=1, data_type=DATATYPES.UINT16,
                                                       converter=EnumConverter({
                                                           1: 25,
                                                           2: 50,
                                                           3: 100,
                                                           4: 200,
                                                           5: 500,
                                                           6: 0
                                                       })),
            "earth-leakage-time": ModbusHolding(address=58, words=1, data_type=DATATYPES.UINT16,
                                                converter=EnumConverter({
                                                    1: 0,
                                                    2: 50,
                                                    3: 100,
                                                    4: 150
                                                }))
        }
        super().__init__(*args, unit=unit, client=client, **kwargs)

    def build_current_range(self):
        output = {}
        l = [
            [5.125, 10],
            [10.25, 20],
            [20.5, 40],
            [41, 80],
            [82, 160],
            [164, 320],
            [328, 640]
        ]
        for i in range(0, len(l)):
            x = {j: self.step_calc(j, i * 32 + 1, (i + 1) * 32 + 1, l[i][0], l[i][1]) for j in
                 range(i * 32 + 1, (i + 1) * 32 + 1)}
            output = {**output, **x}
        return output

    def step_calc(self, i, x1, x2, y1, y2):
        '''
        Returns the step calculated between two separate ranges for the second range.
        :param i: Index of current step required
        :param x1: starting number of first range
        :param x2: ending number of first range
        :param y1: starting number of second range
        :param y2: ending number of second range
        '''
        step = (y2 - y1) / (x2 - (x1 + 1))
        return (i - x1) * step + y1


class HpbSubPlc(EIPDevice):
    def __init__(self, *args, index=0, **kwargs):
        self.data_info = {
            "communications_to_hpb": EIPCommands("HpbData[{index}].HpbComsHly".format(index=index)),
            "running": EIPCommands("HpbData[{index}].OtlRun".format(index=index)),
            "cbr-relay": EIPCommands("HpbData[{index}].CbrClsd".format(index=index)),
            "mcr-relay": EIPCommands("HpbData[{index}].McrClsd".format(index=index)),
            "earth-leakage-trip": EIPCommands("HpbData[{index}].ElTrp".format(index=index)),
            "earth-continuity-trip": EIPCommands("HpbData[{index}].EcTrp".format(index=index)),
            "ef-lockout-trip": EIPCommands("HpbData[{index}].EfloTrp".format(index=index)),
            "over-current-trip": EIPCommands("HpbData[{index}].OcTrp".format(index=index)),
            "short-circuit-trip": EIPCommands("HpbData[{index}].ScTrp".format(index=index)),
            "main-contactor-fail": EIPCommands("HpbData[{index}].McfTrp".format(index=index)),
            "hpb-memory-error": EIPCommands("HpbData[{index}].HpbMemErr".format(index=index)),
            "rtu-memory-error": EIPCommands("HpbData[{index}].HpbMemErr".format(index=index)),
            "mcf-trip-flag": EIPCommands("HpbData[{index}].MCFTrpFlg".format(index=index)),
            "a-phase-current": EIPCommands("HpbData[{index}].CurAVar".format(index=index)),
            "b-phase-current": EIPCommands("HpbData[{index}].CurBVar".format(index=index)),
            "c-phase-current": EIPCommands("HpbData[{index}].CurCVar".format(index=index)),
            "a-phase-volts": EIPCommands("HpbData[{index}].VloA".format(index=index)),
            "b-phase-volts": EIPCommands("HpbData[{index}].VloB".format(index=index)),
            "c-phase-volts": EIPCommands("HpbData[{index}].VloC".format(index=index)),
            "earth-leakage-current": EIPCommands("HpbData[{index}].ElCurVar".format(index=index)),
            "pilot-series-resistance": EIPCommands("HpbData[{index}].PltSerRes".format(index=index)),
            "over-current-trip-level": EIPCommands("HpbData[{index}].OCurLvlTrp".format(index=index)),
            "current-balance": EIPCommands("HpbData[{index}].CurBal".format(index=index)),
            "back-emf-timer-selection": EIPCommands("HpbData[{index}].BemfTimeSet".format(index=index)),
            "current-balance-setting": EIPCommands("HpbData[{index}].CurBalPar".format(index=index)),
            "current-multiplier-setting": EIPCommands("HpbData[{index}].CurMulPar".format(index=index)),
            "current-range-setting": EIPCommands("HpbData[{index}].CurRanPar".format(index=index)),
            "earth-fault-lockout-time-setting": EIPCommands("HpbData[{index}].EfloTimeSet".format(index=index)),
            "earth-leakage-level": EIPCommands("HpbData[{index}].ElCLvl".format(index=index)),
            "earth-leakage-sensitivity-setting": EIPCommands("HpbData[{index}].ElcSensPar".format(index=index)),
            "earth-leakage-trip-time-setting": EIPCommands("HpbData[{index}].ElTimePar".format(index=index)),
            "ec-time": EIPCommands("HpbData[{index}].EfloTimeSet".format(index=index)),
            "eflo-select": EIPCommands("HpbData[{index}].EFloSel".format(index=index)),
            "machine-number-setting": EIPCommands("HpbData[{index}].MacNum".format(index=index)),
            "machine-type-setting": EIPCommands("HpbData[{index}].MacType".format(index=index)),
            "over-current-curve-setting": EIPCommands("HpbData[{index}].CurCurvePar".format(index=index)),
            "over-current-time-multiplier": EIPCommands("HpbData[{index}].CurTimeMul".format(index=index)),
            "pilot-latch-setting": EIPCommands("HpbData[{index}].PltLatPar".format(index=index)),
            "pilot-mode-selection": EIPCommands("HpbData[{index}].PltModeSelPar".format(index=index)),
            "short-circuit-output-relay-selection": EIPCommands("HpbData[{index}].ScrSelPar".format(index=index)),
            "short-circuit-setting": EIPCommands("HpbData[{index}].ScMulPar".format(index=index)),
            "short-circuit-trip-time-setting": EIPCommands("HpbData[{index}].ScTimePar".format(index=index)),
            "under-voltage-trip-setting": EIPCommands("HpbData[{index}].UvPar".format(index=index)),
        }
        super().__init__(*args, **kwargs)


class IpsiConverter:
    def __init__(self, offset, device):
        """
        :param offset: modbus address offset in hex
        :param device: device object containing modbus data information
        """
        self.offset = offset
        self.device: ModbusDevice = device

    def set_client(self, client):
        """
        :param client: The modbus client to use
        :return:
        """
        self.device.client = client

    def sync_read_data(self, lock=None):
        """
        Reads the modbus addresses and buffers them until the next report_data call
        :return:
        """
        rr = self.device.client.read_holding_registers(self.offset, count=64, unit=self.device.unit)
        if rr.isError():
            raise rr
        addr_map = AddressMapUint16()
        addr_map[:64] = rr.registers
        for ident, info in self.device.data_info.items():
            resp = info.decode(addr_map[info.address: info.address + info.words])
            if resp is not None:
                if isinstance(resp, dict):
                    self.device.data[ident].append(resp.pop("_raw"))
                    for k, v in resp.items():
                        try:
                            self.device.data[k].append(v)
                        except KeyError:
                            self.device.data[k] = [v]
                else:
                    self.device.data[ident].append(resp)

    async def async_read_data(self, lock=None, timeout=1):
        """
        Reads the modbus addresses and buffers them until the next report_data call
        :return:
        """
        cm = None
        try:
            log.debug("About to await")
            with async_timeout.timeout(timeout) as cm:
                rr = await self.device.client.protocol.read_holding_registers(self.offset, count=64,
                                                                              unit=self.device.unit)
        except asyncio.TimeoutError:
            if cm is not None and cm.expired:
                log.debug("Async read expired")
            raise
        except AttributeError as e:
            if "NoneType" in e.args[0] and "read_holding_registers" in e.args[0]:
                log.debug("No connection present")
                return None
            else:
                raise
        except ConnectionException as e:
            log.exception(e)
            return None
        if rr.isError():
            log.warning("Invalid reads for unit {}\nMessage:{}".format(self.device.unit, rr))
        else:
            log.debug("Read holding registers complete")
            addr_map = AddressMapUint16()
            addr_map[0:64] = rr.registers
            for ident, info in self.device.data_info.items():
                resp = info.decode(addr_map[info.address: info.address + info.words])
                if resp is not None:
                    if isinstance(resp, dict):
                        self.device.data[ident].append(resp.pop("_raw"))
                        for k, v in resp.items():
                            try:
                                self.device.data[k].append(v)
                            except KeyError:
                                self.device.data[k] = [v]
                    else:
                        log.debug("read {} from slave {} address {}".format(resp, self.device.unit, info.address))
                        self.device.data[ident].append(resp)

    def sync_update(self, register_id, value):
        reg = self.get_modbus_id(register_id)
        return reg.sync_update(self.device.client, self.device.unit, register_id, value)

    async def async_update(self, register_id, value):
        reg = self.get_modbus_id(register_id)
        return await reg.async_update(self.device.client, self.device.unit, register_id, value)

    def get_modbus_id(self, item):
        try:
            return self.device.data_info[item]
        except KeyError:
            for itm in self.device.data_info.values():
                if isinstance(itm, ModbusBitMask):
                    if item in itm.bitmask:
                        return itm
            raise

    def iter_data(self):
        for k, v in self.device.data.items():
            yield self.device.dev_id, self.device.dev_type, k, v

    def __getitem__(self, item):
        self.get_modbus_id(item)
