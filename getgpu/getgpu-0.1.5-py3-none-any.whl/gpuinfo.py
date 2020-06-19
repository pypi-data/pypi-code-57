import pynvml

def get(device_id):
    pynvml.nvmlInit()
    handle = pynvml.nvmlDeviceGetHandleByIndex(device_id)

    return {
        'memory_used': pynvml.nvmlDeviceGetMemoryInfo(handle).used / (1024 * 1024),
        'utilization': pynvml.nvmlDeviceGetUtilizationRates(handle).gpu
    }
