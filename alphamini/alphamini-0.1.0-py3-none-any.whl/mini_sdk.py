import asyncio
import logging
from asyncio.futures import Future
from typing import Any, Set, Optional

from google.protobuf import message as _message

from .channels.websocket_client import AbstractMsgHandler
from .channels.websocket_client import ubt_websocket as _websocket
from .dns.dns_browser import WiFiDeviceListener, WiFiDevice
from .dns.dns_browser import browser as _browser

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())
if log.level == logging.NOTSET:
    log.setLevel(logging.INFO)

browser = _browser()
websocket = _websocket()


def set_log_level(level: int, save_file: str = None):
    """
    设置sdk日志级别
    :param level: logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR
    :param save_file: 需要保存到文件的, 填写日志文件路径

    """
    log.setLevel(level)

    from .dns.dns_browser import log as log1
    log1.setLevel(log.level)

    from .channels.websocket_client import log as log2
    log2.setLevel(log.level)

    if save_file is not None:
        file_handler = logging.FileHandler(save_file)
        log.addHandler(file_handler)
        log1.addHandler(file_handler)
        log2.addHandler(file_handler)


class GetWiFiDeviceListListener(WiFiDeviceListener):
    """
    批量获取机器人设备监听类
    """
    devices: Set[WiFiDevice]

    def __init__(self, devices):
        """
        初始化
        :param devices: Set[WiFiDevice] or None
        """
        self.devices: Set[WiFiDevice] = devices or set()

    def on_device_updated(self, device: WiFiDevice) -> None:
        """
        机器人设备更新了
        :type device: WiFiDevice
        """
        self.devices.update(device)

    def on_device_removed(self, device: WiFiDevice) -> None:
        """
        机器人设备从局域网中移除了
        :param device: WFiDevice
        """
        self.devices.remove(device)

    def on_device_found(self, device: WiFiDevice) -> None:
        """
        扫描到一个机器人设备
        :param device: WFiDevice
        """
        self.devices.add(device)


async def get_user_input(devices: tuple) -> int:
    """
    获取用户输入
    :param devices: 扫描到的机器人设备
    :return: 用户输入值
    """
    try:
        i: int = 0
        for device in devices:
            print('{0}.{1}'.format(i, device))
            i += 1
        num_text = input(f'请输入选择连接的机器人序号:')
    except Exception as e:
        raise e
    else:
        return int(num_text)


def start_scan(loop: asyncio.AbstractEventLoop, name: str) -> Future:
    """
    开启一个扫描机器人设备的Future
    :param loop: 当前事件loop
    :param name: 指定设备名称
    :return: asyncio.Future
    """
    fut = loop.create_future()

    class _InnerLister(WiFiDeviceListener):

        @staticmethod
        def set_result(future: Future, device: WiFiDevice):
            if future.cancelled() or future.done():
                return
            log.info(f"found device : {device}")
            future.set_result(device)

        def on_device_found(self, device: WiFiDevice) -> None:
            if device.name.endswith(name):
                if fut.cancelled() or fut.done():
                    return
                loop.run_in_executor(None, browser.stop_scan)
                loop.call_soon(_InnerLister.set_result, fut, device)

        def on_device_updated(self, device: WiFiDevice) -> None:
            if device.name.endswith(name):
                if fut.cancelled() or fut.done():
                    return
                loop.run_in_executor(None, browser.stop_scan)
                loop.call_soon(_InnerLister.set_result, fut, device)

        def on_device_removed(self, device: WiFiDevice) -> None:
            if device.name.endswith(name):
                if fut.cancelled() or fut.done():
                    return
                loop.call_soon(_InnerLister.set_result, fut, device)

    log.info("start scanning...")
    browser.add_listener(_InnerLister())
    browser.start_scan(0)

    return fut


async def get_device_by_name(name: str, timeout: int) -> Optional[WiFiDevice]:
    """
    获取当前局域网内，指定名字的机器人设备信息
    :param name: 设备序列号
    :param timeout: 扫描超时时间
    :return: Optional[WiFiDevice]
    """

    async def start_scan_async():
        return await start_scan(asyncio.get_running_loop(), name)

    try:
        device: WiFiDevice = await asyncio.wait_for(start_scan_async(), timeout)
        return device
    except asyncio.TimeoutError:
        log.warning(f'scan device timeout')
        return None
    finally:
        browser.stop_scan()
        log.info("stop scan finished.")


async def get_device_list(timeout: int) -> tuple:
    """
    获取当前局域网内所有机器人设备信息
    :param timeout: 超时时间
    :return: ()
    """
    devices: Set[WiFiDevice] = set()
    browser.add_listener(GetWiFiDeviceListListener(devices))
    browser.start_scan(0)
    await asyncio.sleep(timeout)
    browser.remove_all_listener()
    browser.stop_scan()
    return tuple(devices)


async def connect(device: WiFiDevice) -> bool:
    """
    连接机器人设备
    :param device: WiFiDevice
    :return: bool
    """
    return await websocket.connect(device.address)


def register_msg_handler(cmd: int, handler: AbstractMsgHandler):
    """
    注册命令监听器
    :param cmd: 支持的命令请查看: mini.blockapi.cmdid
    :param handler: 命令处理器
    """
    websocket.register_msg_handler(cmd, handler)


def unregister_msg_handler(cmd: int, handler: AbstractMsgHandler):
    """
    反注册命令监听器
    :param cmd: 支持的命令请查看: mini.blockapi.cmdid
    :param handler:
    """
    websocket.unregister_msg_handler(cmd, handler)


async def send_msg(cmd: int, message: _message.Message, timeout: int) -> Any:
    """
    发送一个消息给机器人
    :param cmd:支持的命令请查看: mini.blockapi.cmdid
    :param message:  消息类在: mini.pb2 包内
    :param timeout: 超时时间
    :return:
    """
    return await websocket.send_msg(cmd, message, timeout)


"""
断开链接，释放资源
"""


async def release():
    await websocket.shutdown()
