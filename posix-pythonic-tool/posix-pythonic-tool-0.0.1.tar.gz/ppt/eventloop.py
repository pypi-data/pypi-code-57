"""统一 epoll 、poll 、select 三大事件循环，让 Uloop 可以跨平台
"""

import time
import enum
import select
import logging

__ALL__ = ['UEvent', 'Uloop']


class UEvent(enum.IntFlag):
    """event mask
    """
    poll_none = 0x00
    poll_in = 0x01
    poll_out = 0x04
    poll_err = 0x08
    poll_hup = 0x10
    poll_nval = 0x20


class SelectLoop(object):
    """封装 select 事件循环
    """

    def __init__(self):
        """
        """
        # 可读句柄列表
        self._reads = []
        # 可写句柄列表
        self._writes = []
        # 异常句柄列表
        self._execes = []

    def register(self, fileno: int, mode: UEvent):
        """注册事件
        """
        if mode & UEvent.poll_in:
            self._reads.append(fileno)

        if mode & UEvent.poll_out:
            self._writes.append(fileno)

        if mode & UEvent.poll_err:
            self._execes.append(fileno)

    def unregister(self, fileno: int):
        """取消事件
        """
        if fileno in self._reads:
            self._reads.remove(fileno)

        if fileno in self._writes:
            self._writes.remove(fileno)

        if fileno in self._execes:
            self._execes.remove(fileno)

    def modify(self, fileno: int, mode: UEvent):
        """
        """
        self.unregister(fileno)
        self.register(fileno, mode)

    def close(self):
        """
        """
        pass

    def poll(self):
        """
        """
        r, w, e = select.select(self._reads, self._writes, self._execes)
        for fileno in r:
            yield fileno, UEvent.poll_in

        for fileno in w:
            yield fileno, UEvent.poll_out

        for fileno in e:
            yield fileno, UEvent.poll_err


class Uloop(object):
    """封装 epoll,poll,select 为一个事件循环
    """

    def __init__(self):
        """
        """
        # self._loop 事件循环的低层实现方法
        # self._impl 实现的方法名
        if hasattr(select, 'epoll'):
            self._loop = select.epoll()
            self._impl = 'epoll'
        elif hasattr(select, 'poll'):
            self._loop = select.poll()
            self._impl = 'poll'
        elif hasattr(select, 'select'):
            self._loop = SelectLoop()
            self._impl = 'select'
        else:
            raise Exception(
                "can't find any available functions in select  model .")

        # self._handers 保存句柄与处理器之间的对应关系
        # {fileno:EventHander}
        self._handlers = {}

        # self._last_time
        self._last_time = time.time()

        # self._periodic_callbacks 周期性回调函数列表
        self._periodic_callbacks = []

        # 是否停止
        self._stoping = False

        # poll 的超时时间
        self.timeout = 10

    def add(self, fileno, mode: UEvent, eventhandler):
        """注册文档句柄到事件循环
        """
        if not isinstance(fileno, int):
            # fileno 不是句柄号，就调用 fileno 方法
            fileno = fileno.fileno()

        # 记录句柄与处理器的关系
        self._handlers[fileno] = (fileno, eventhandler)
        # 注册事件
        self._loop.register(fileno, mode)

    def remove(self, fileno):
        """从事件循环中移除句柄
        """
        if not isinstance(fileno, int):
            fileno = fileno.fileno()

        if fileno in self._handlers:
            self._loop.unregister(fileno)
            del self._handlers[fileno]

    def modify(self, fileno, mode: UEvent):
        """修改句柄注册的事件
        """
        if not isinstance(fileno, int):
            fileno = fileno.fileno()

        if fileno in self._handlers:
            # 如果在
            self._loop.modify(fileno, mode)

    def add_periodic(self, callback):
        """添加周期性回调函数
        """
        self._periodic_callbacks.append(callback)

    def remove_periodic(self, callback):
        """移除周期性回调函数
        """
        self._periodic_callbacks.remove(callback)

    def stop(self):
        self._stoping = True

    def close(self):
        self._loop.close()

    def poll(self, timeout=10):
        """
        """
        return [(self._handlers[fileno][1], fileno, event)for fileno, event in self._loop.poll(timeout)]

    def run(self):
        """启动事件循环
        """
        while not self._stoping:
            # 只要没有设置 self._stopping == True 就一直执行下去

            # 接收事件
            has_error = False
            try:
                events = self.poll(self.timeout)
            except (OSError, IOError) as err:
                has_error = True
                logging.error(str(err))

            # 处理事件
            for handler, fileno, event in events:
                try:
                    handler.process_event(fileno, event)
                except Exception as err:
                    logging.error(str(err))
                    logging.exception(str(err))

            # 处理周期性任务和异常
            now = time.time()
            if has_error or (now - self._last_time) > self.timeout:
                for callback in self._periodic_callbacks:
                    callback()
                self._last_time = now
