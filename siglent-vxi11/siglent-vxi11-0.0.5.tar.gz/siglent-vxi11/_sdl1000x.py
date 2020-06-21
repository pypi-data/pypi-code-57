import vxi11
from enum import IntEnum


# https://www.siglenteu.com/wp-content/uploads/dlm_uploads/2019/05/SDL1000X-Programming_Guide-V1.0.pdf

class Function(IntEnum):
    CURRENT = 1,
    VOLTAGE = 2,
    POWER = 3,
    RESISTANCE = 4,
    LED = 5


class Measure():

    def __init__(self, dev):
        self.__dev = dev

    # Gets the real time voltage measurement value
    # MEASure:VOLTage[:DC]?
    def __get_voltage(self) -> float:
        return float(self.__dev.ask("MEAS:VOLT?"))

    voltage = property(__get_voltage)

    # Gets the real time current measurement value
    # MEASure:CURRent[:DC]?
    def __get_current(self) -> float:
        return float(self.__dev.ask("MEAS:CURR?"))

    current = property(__get_current)

    # Gets the real time power measurement value
    # MEASure:POWer[:DC]?
    def __get_power(self) -> float:
        return float(self.__dev.ask("MEAS:POW?"))

    power = property(__get_power)

    # Gets the real time resistor measurement value
    # MEASure:RESistance[:DC]?
    def __get_resistance(self) -> float:
        return float(self.__dev.ask("MEAS:RES?"))

    resistance = property(__get_resistance)

    # Gets the real time external measurement value in external sink mode
    # MEASure:EXT?
    def __get_ext(self) -> float:
        return float(self.__dev.ask("MEAS:EXT?"))

    ext = property(__get_ext)

    # Gets the waveform data of the waveform display interface in CC/CV/CP/CR mode. Totally include 200 float data
    # MEASure:WAVEdata? {CURRent | VOLTage | POWer | RESistance}


class ConstantCurrent():

    def __init__(self, dev):
        self.__dev = dev

    # Sets the sink current value of CC mode in static operation
    # [:SOURce]:CURRent[:LEVel][:IMMediate] {<value> | MINimum | MAXimum | DEFault}
    def __set_current(self, value: float):
        self.__dev.ask(":CURR " + str(value))

    # Query the preset current value of CC mode in static operation
    # [:SOURce]:CURRent[:LEVel][:IMMediate]?
    def __get_current(self):
        return float(self.__dev.ask(":CURR?"))

    current = property(__get_current, __set_current)

    # Sets the current range of CC mode in static operation
    # [:SOURce]:CURRent:IRANGe <value>
    def __set_i_range(self, value):
        self.__dev.ask(":CURR:IRANG " + str(value))

    # Query the current range of CC mode in static operation
    # [:SOURce]:CURRent:IRANGe?
    def __get_i_range(self):
        return self.__dev.ask(":CURR:IRANG?")

    i_range = property(__get_i_range, __set_i_range)

    # Sets the voltage range of CC mode in static operation
    # [:SOURce]:CURRent:VRANGe <value>
    def __set_v_range(self, value):
        self.__dev.ask(":CURR:VRANG " + str(value))

    # Query the voltage range of CC mode in static operation
    # [:SOURce]:CURRent:VRANGe?
    def __get_v_range(self):
        return self.__dev.ask(":CURR:VRANG?")

    v_range = property(__get_v_range, __set_v_range)

    # Sets the slope of CC mode in static operation. The rise slope and descending slope will be set synchronously
    # [:SOURce]:CURRent:SLEW[:BOTH] {<value> | MINimum | MAXimum | DEFault}
    def __set_slew(self, value):
        self.__dev.ask(":CURR:SLEW " + str(value))

    slew = property(__set_slew)

    # Sets the rise slope of CC mode in static operation.
    # [:SOURce]:CURRent:SLEW:POSitive {<value> | MINimum | MAXimum | DEFault}
    def __set_slew_ris(self, value):
        self.__dev.ask(":CURR:SLEW:POS " + str(value))

    # Query the rise slope of CC mode in static operation
    # [:SOURce]:CURRent:SLEW:POSitive?
    def __get_slew_ris(self) -> float:
        return float(self.__dev.ask(":CURR:SLEW:POS?"))

    slew_ris = property(__get_slew_ris, __set_slew_ris)

    # Sets the descending slope of CC mode in static operation
    # [:SOURce]:CURRent:SLEW:NEGative {<value> | MINimum | MAXimum | DEFault}
    def __set_slew_fal(self, value):
        self.__dev.ask(":CURR:SLEW:NEG " + str(value))

    # Query the descending slope of CC mode in static operation.
    # [:SOURce]:CURRent:SLEW:NEGative?
    def __get_slew_fal(self) -> float:
        return float(self.__dev.ask(":CURR:SLEW:NEG?"))

    slew_fal = property(__get_slew_fal, __set_slew_fal)

    # Sets the waveform mode of CC mode in transient operation
    # [:SOURce]:CURRent:TRANsient:MODE {CONTinuous | PULSe | TOGGle}

    # Query the waveform mode of CC mode in static operation
    # [:SOURce]:CURRent:TRANsient:MODE?

    # Sets the current range of CC mode in transient operation
    # [:SOURce]:CURRent:TRANsient:IRANGe <value>

    # Query the current range of CC mode in transient operation
    # [:SOURce]:CURRent:TRANsient:IRANGe?

    # Sets the voltage range of CC mode in transient operation
    # [:SOURce]:CURRent:TRANsient:VRANGe <value>

    # Query the voltage range of CC mode in transient operation
    # [:SOURce]:CURRent:TRANsient:VRANGe?

    # Sets the A Level of CC mode in transient operation
    # [:SOURce]:CURRent:TRANsient:ALEVel {<value> | MINimum | MAXimum | DEFault}

    # Query the A Level of CC mode in transient operation
    # [:SOURce]:CURRent:TRANsient:ALEVel?

    # Sets the B Level of CC mode in transient operation
    # [:SOURce]:CURRent:TRANsient:BLEVel {<value> | MINimum | MAXimum | DEFault}

    # Query the B Level of CC mode in transient operation
    # [:SOURce]:CURRent:TRANsient:BLEVel?

    # Sets the A Level pulse width time value of CC mode in transient operation. Its unit is "s"
    # [:SOURce]:CURRent:TRANsient:AWIDth {<value> | MINimum | MAXimum | DEFault}

    # Query the A Level pulse width time value of CC mode in transient operation. Its unit is "s"
    # [:SOURce]:CURRent:TRANsient:AWIDth?

    # Sets the B Level pulse width time value of CC mode in transient operation. Its unit is "s"
    # [:SOURce]:CURRent:TRANsient:BWIDth {<value> | MINimum | MAXimum | DEFault}

    # Query the B Level pulse width time value of CC mode in transient operation. Its unit is "s"
    # [:SOURce]:CURRent:TRANsient:BWIDth?

    # Sets the rise slope of CC mode in transient operation
    # [:SOURce]:CURRent:TRANsient:SLEW:POSitive {<value> | MINimum | MAXimum | DEFault}

    # Query the rise slope of CC mode in transient operation
    # [:SOURce]:CURRent:TRANsient:SLEW:POSitive?

    # Sets the descending slope of CC mode in transient operation
    # [:SOURce]:CURRent:TRANsient:SLEW:NEGative {<value> | MINimum | MAXimum | DEFault}

    # Query the descending slope of CC mode in transient operation
    # [:SOURce]:CURRent:TRANsient:SLEW:NEGative?


class ConstantVoltage():

    def __init__(self, dev):
        self.__dev = dev

    # Sets the preset voltage value of CV mode in static operation
    # [:SOURce]:VOLTage[:LEVel][:IMMediate] {<value> | MINimum | MAXimum | DEFault}

    # Query the preset voltage value of CV mode in static operation
    # [:SOURce]:VOLTage[:LEVel][:IMMediate]?

    # Sets the current range of CV mode in static operation
    # [:SOURce]:VOLTage:IRANGe <value>

    # Query the current range of CV mode in static operation
    # [:SOURce]:VOLTage:IRANGe?

    # Sets the voltage range of CV mode in static operation
    # [:SOURce]:VOLTage:VRANGe <value>

    # Query the voltage range of CV mode in static operation
    # [:SOURce]:VOLTage:VRANGe?

    # Sets the waveform mode of CV mode in transient operation
    # [:SOURce]:VOLTage:TRANsient:MODE {CONTinuous | PULSe | TOGGle}

    # Query the waveform mode of CV mode in static operation
    # [:SOURce]:VOLTage:TRANsient:MODE?

    # Sets the current range of CV mode in transient operation
    # [:SOURce]:VOLTage:TRANsient:IRANGe <value>

    # Query the current range of CV mode in transient operation
    # [:SOURce]:VOLTage:TRANsient:IRANGe?

    # Sets the voltage range of CV mode in transient operation
    # [:SOURce]:VOLTage:TRANsient:VRANGe <value>

    # Query the voltage range of CV mode in transient operation
    # [:SOURce]:VOLTage:TRANsient:VRANGe?

    # Sets the A Level of CV mode in transient operation
    # [:SOURce]: VOLTage:TRANsient:ALEVel {<value> | MINimum | MAXimum | DEFault}

    # Query the A Level of CV mode in transient operation
    # [:SOURce]: VOLTage:TRANsient:ALEVel?

    # Sets the B Level of CV mode in transient operation
    # [:SOURce]:VOLTage:TRANsient:BLEVel {<value> | MINimum | DEFault}

    # Query the B Level of CV mode in transient operation
    # [:SOURce]: VOLTage:TRANsient:BLEVel?

    # Sets the A Level pulse width time value of CV mode in transient operation. Its unit is "s"
    # [:SOURce]:VOLTage:TRANsient:AWIDth {<value> | MINimum | MAXimum | DEFault}

    # Query the A Level pulse width time value of CV mode in transient operation. Its unit is "s"
    # [:SOURce]:VOLTage:TRANsient:AWIDth?

    # Sets the B Level pulse width time value of CV mode in transient operation. Its unit is "s"
    # [:SOURce]:VOLTage:TRANsient:BWIDth {<value> | MINimum | MAXimum | DEFault}

    # Query the B Level pulse width time value of CV mode in transient operation. Its unit is "s"
    # [:SOURce]:VOLTage:TRANsient:BWIDth?


# 3.3.4 Source Power Subsystem Command
class ConstantPower():

    def __init__(self, dev):
        self.__dev = dev

 # Sets the preset power value of CP mode in static operation
 # [:SOURce]:POWer[:LEVel][:IMMediate] {<value> | MINimum |  MAXimum | DEFault}

 # Query the preset power value of CP mode in static operation
 # [:SOURce]:POWer[:LEVel][:IMMediate]?

# Sets the current range of CP mode in static operation
# [:SOURce]:POWer:IRANGe <value>

# Query the current range of CP mode in static operation
# [:SOURce]:POWer:IRANGe?

# Sets the voltage range of CP mode in static operation
# [:SOURce]:POWer:VRANGe <value>

# Query the voltage range of CP mode in static operation
# [:SOURce]:POWer:VRANGe?

# Sets the waveform mode of CP mode in transient operation
# [:SOURce]:POWer:TRANsient:MODE {CONTinuous | PULSe | TOGGle}

# Query the waveform mode of CP mode in static operation
# [:SOURce]:POWer:TRANsient:MODE?

# Sets the current range of CP mode in transient operation
# [:SOURce]:POWer:TRANsient:IRANGe <value>

# Query the current range of CP mode in transient operation
# [:SOURce]:POWer:TRANsient:IRANGe?

# Sets the voltage range of CP mode in transient operation
# [:SOURce]:POWer:TRANsient:VRANGe <value>


class ConstantResitance():

    def __init__(self, dev):
        self.__dev = dev


class SDL1000X():

    def __init__(self, host='192.168.20.12'):
        self.__dev = vxi11.Instrument(host)
        self.__measure = Measure(self.__dev)
        self.__constant_current = ConstantCurrent(self.__dev)
        self.__constant_voltage = ConstantVoltage(self.__dev)

    # 3. System Commands
    # 3.1 IEEE Common Subsystem Commands

    # Returns an instrument identification information string. The string will contain the manufacturer , model number, serial number and software number
    # *IDN?
    def __get_idn(self):
        return self.__dev.ask("*IDN?")

    idn = property(__get_idn)

    # Rstore the equipment state to be initial state
    # *RST
    def rstore(self):
        self.__dev.ask("*RST")

    # Clears all bits in all of the event registers and the error list
    # *CLS
    def clear(self):
        self.__dev.ask("*CLS")

    # Set the bits in the standard event status enable register
    # *ESE <number>
    def __set_ese(self, value):
        self.__dev.ask("*ESE " + str(value))

    # Query the standard event status enable register. The value returned reflects the current state of all the bits in the register
    # *ESE?
    def __get_ese(self) -> int:
        return int(self.__dev.ask("*ESE?"))

    ese = property(__get_ese, __set_ese)

    # Query and clears the standard event status register. The value returned reflects the current state of all the bits in the register
    # *ESR?


    # 3.2 Measure Subsystem command

    def __get_measure(self) -> Measure:
        return self.__measure

    measure = property(__get_measure)

    # 3.3   Source Subsystem Command
    # 3.3.1 Source Common Subsystem Command

    # Sets the input status of the load (ON or OFF)
    # [:SOURce]:INPut[:STATe] {ON | OFF 0 | 1}
    def __set_input(self, value):
        self.__dev.ask(":INP " + str(value))

    # Query the input status of the load. Return "1" if input status is ON. Otherwise, return "0"
    # [:SOURce]:INPut[:STATe]?
    def __get_input(self) -> int:
        return int(self.__dev.ask(":INP?"))

    input = property(__get_input, __set_input)

    # Sets the short circuit status of the load (ON or OFF)
    # [:SOURce]:SHORt[:STATe] {ON | OFF 0 | 1}

    # Query the short circuit status in current mode of the load. Return "1" if short circuit status is ON. Otherwise, return "0"
    # [:SOURce]:SHORt[:STATe]?

    # Sets mode in transient operation (CC/CV/CP/CR)
    # [:SOURce]:FUNCtion:TRANsient {CURRent | VOLTage | POWer | RESistance }

    # Query current mode in transient operation
    # [:SOURce]:FUNCtion:TRANsient?

    # [:SOURce]:FUNCtion {CURRent | VOLTage | POWer | RESistance | LED}
    # Sets mode in static operation (CC/CV/CP/CR/LED)
    def __set_function(self, value: Function):
        self.__dev.ask(":FUNC " + value.name)

    # [:SOURce]:FUNCtion?
    # Query current mode in static operation
    def __get_function(self) -> Function:
        return Function[self.__dev.ask(":FUNC?")]

    function = property(__get_function, __set_function)

    # Query the number of running step in the LIST/PROGRAM test sequence
    # [:SOURce]:TEST:STEP?

    # Query whether the running steps of the test sequence stop or not. Resturns "1" if test stop or return "0" if test stop
    # [:SOURce]:TEST:STOP?

    # 3.3.2 Source Current Subsystem Command
    def __get_constant_current(self) -> ConstantCurrent:
        return self.__constant_current

    constant_current = property(__get_constant_current)

    # 3.3.3 Source Voltage Subsystem Command
    def __get_constant_voltage(self) -> ConstantVoltage:
        return self.__constant_voltage

    constant_voltage = property(__get_constant_voltage)

    # 3.3.4 Source Power Subsystem Command

    # 3.3.5 Source Resistance Subsystem Command

    # 3.3.6 Source LED Subsystem Command

    # 3.3.7 Source Battery Subsystem Command

    # 3.3.8 Source List Subsystem Command

    # 3.3.9 Source OCPT Subsystem Command

    # 3.3.10 Source OPPT Subsystem Command

    # 3.3.11 Source Program Subsystem Command

    # 3.3.12 Source Wave Subsystem Command

    # 3.3.13 Source Utility Subsystem Command

    # 3.4 Subsystem Command

    # 3.5 LAN Interface Subsystem Command

class SDL1020XE(SDL1000X):
    pass