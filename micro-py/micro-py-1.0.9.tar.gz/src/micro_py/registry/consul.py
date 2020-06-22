import os

from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

import threading
import time

import consul

from . import Registry


class Consul(Registry):
    """
    consul 的微服务注册实现
    """

    def __init__(self, server_name: str = "", addr: str = "", port: int = 0, host: str = "",
                 register_interval: int = 30, register_ttl: int = 60):

        # register_ttl
        splay = 5
        deregTTL = register_ttl + splay

        # consul has a minimum timeout on deregistration of 1 minute.
        if register_ttl < 60:
            deregTTL = 60 + splay

        # 如果 轮训间隔 小于 超时时间的话，那就将超时时间修改成 轮训间隔加一分钟，避免导致服务检测异常
        if register_interval > deregTTL:
            deregTTL += register_interval + 60

        self.register_interval = register_interval
        self.register_ttl = deregTTL
        self.host = host
        self.port = port
        self.addr = addr
        self.server_name = server_name
        (host, port) = host.split(":")
        self.c = consul.Consul(host, port)
        # 服务ID
        self.service_id = f"{self.server_name}-{self.addr}-{self.port}"
        self.sched = BlockingScheduler()

        print("consul addr {}".format(host))

    def job(self):
        check_id = f"service:{self.service_id}"
        print(check_id)
        self.c.agent.check.ttl_pass(check_id=check_id)

    def register(self):
        check = consul.Check.ttl(f"{self.register_ttl}s")
        # 注册服务部分
        self.c.agent.service.register(
            name=self.server_name,
            service_id=self.service_id,
            address=self.addr,
            port=self.port,
            check=check
        )

        # 定义BlockingScheduler
        self.sched.add_job(self.job, 'interval', seconds=self.register_interval)
        self.job()
        print(f"注册服务{self.server_name}成功")
        self.sched.start()

    def deregister(self):
        print(f"开始退出服务{self.server_name}")
        self.c.agent.service.deregister(self.service_id)

    def get_service(self, name: str):
        services = []
        for (k, v) in self.list_services().items():
            if k.startswith(name):
                services.append(v)
        return services

    def list_services(self):
        return self.c.agent.services()

    def watch(self):
        pass
