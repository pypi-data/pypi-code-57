import os
from ctypes import *


class Record:
    def __init__(self, size, data_ptr, pc_ptr):
        self.pc = [0] * size
        self.data = [0.0] * size
        for i in range(size):
            self.data[i] = data_ptr[i]
            self.pc[i] = pc_ptr[i]

    def size(self) -> int:
        return len(self.data)


class Net:
    def __init__(self, ptr: c_char_p):
        self.ptr = ptr

    def __del__(self):
        self.delete()

    def delete(self):
        return SnnAPI.delete_net(self)

    def add_part(self, data: str):
        return SnnAPI.add_part(self, data)

    def get_params(self, pid: int) -> str:
        return SnnAPI.get_params(self, pid)

    def set_params(self, pid: int, data: str):
        return SnnAPI.set_params(self, pid, data)

    def set_recorder(self, pid: int, data: str):
        return SnnAPI.set_recorder(self, pid, data)

    def reset(self):
        return SnnAPI.reset_net(self)

    def run(self, steps: int, dt: float):
        return SnnAPI.run_net(self, steps, dt)

    def get_record(self, rid: int) -> Record:
        data_ptr = POINTER(c_double)()
        pc_ptr = POINTER(c_uint32)()
        size = SnnAPI.get_recorder_ptr(self, rid, data_ptr, pc_ptr)
        return Record(size, data_ptr, pc_ptr)


class SnnAPI:
    path = os.path.join(os.path.dirname(__file__), "lib\\snn.dll")
    api = cdll.LoadLibrary(path)
    api.SnnAPI_deleteNet.argtypes = [c_void_p]
    api.SnnAPI_newNet.restype = c_void_p
    api.SnnAPI_getLog.restype = c_char_p
    api.SnnAPI_addPart.argtypes = [c_void_p, c_char_p]
    api.SnnAPI_getParams.argtypes = [c_void_p, c_uint32]
    api.SnnAPI_getParams.restype = c_char_p
    api.SnnAPI_setParams.argtypes = [c_void_p, c_uint32, c_char_p]
    api.SnnAPI_setRecorder.argtypes = [c_void_p, c_uint32, c_char_p]
    api.SnnAPI_setRecorder.restype = c_uint32
    api.SnnAPI_resetNet.argtypes = [c_void_p]
    api.SnnAPI_runNet.argtypes = [c_void_p, c_uint32, c_double]
    api.SnnAPI_getRecorderPtr.argtypes = [c_void_p, c_uint32, POINTER(POINTER(c_double)),
                                          POINTER(POINTER(c_uint32))]
    api.SnnAPI_getRecorderPtr.restype = c_uint32

    @staticmethod
    def new_net() -> Net:
        return Net(SnnAPI.api.SnnAPI_newNet())

    @staticmethod
    def clear_log():
        SnnAPI.api.SnnAPI_clearLog()

    @staticmethod
    def get_log() -> str:
        return SnnAPI.api.SnnAPI_getLog().decode("utf-8")

    @staticmethod
    def delete_net(net: Net):
        SnnAPI.api.SnnAPI_deleteNet(net.ptr)
        net.ptr = None

    @staticmethod
    def add_part(net: Net, data: str):
        SnnAPI.api.SnnAPI_addPart(net.ptr, data.encode())

    @staticmethod
    def get_params(net: Net, pid: int) -> str:
        return SnnAPI.api.SnnAPI_getParams(net.ptr, pid).decode("utf-8")

    @staticmethod
    def set_params(net: Net, pid: int, data: str) -> None:
        return SnnAPI.api.SnnAPI_setParams(net.ptr, pid, data.encode())

    @staticmethod
    def set_recorder(net: Net, pid: int, data: str) -> int:
        return SnnAPI.api.SnnAPI_setRecorder(net.ptr, pid, data.encode())

    @staticmethod
    def reset_net(net: Net):
        return SnnAPI.api.SnnAPI_resetNet(net.ptr)

    @staticmethod
    def run_net(net: Net, steps: int, dt: float):
        return SnnAPI.api.SnnAPI_runNet(net.ptr, steps, dt)

    @staticmethod
    def get_recorder_ptr(net: Net, rid: int, data_ptr, pc_ptr) -> int:
        return SnnAPI.api.SnnAPI_getRecorderPtr(net.ptr, rid, byref(data_ptr), byref(pc_ptr))
