import getgpu.gpuinfo as gpuinfo
import time
import pynvml

def get_idle(device_ids=None, n_gpus=1, memory_used_less_than=100):
    if device_ids is None:
        pynvml.nvmlInit()
        device_ids = list(range(pynvml.nvmlDeviceGetCount()))

    idle_devices = []
    for device_id in device_ids:
        gpu_status = gpuinfo.get(device_id=device_id)
        if gpu_status['memory_used'] < memory_used_less_than:
            idle_devices.append(device_id)

        if len(idle_devices) == n_gpus:
            break

    if len(idle_devices) == 0:
        return None
    elif len(idle_devices) == 1:
        return idle_devices[0]
    elif len(idle_devices) == n_gpus:
        return str(idle_devices).replace('[', ''). replace(']', '').replace(' ', '')
    elif len(idle_devices) < n_gpus:
        return None
    else:
        raise ValueError("Error in `idle_devices`.")


def wait_until_available(device_ids=None, n_gpus=1, memory_used_less_than=100, timeout=1000000):
    base_time = time.time()
    while True:
        idle_device = get_idle(device_ids, n_gpus, memory_used_less_than)
        if idle_device is not None:
            print(idle_device)
            return idle_device

        time.sleep(3)
        if time.time() - base_time > timeout:
            return None
