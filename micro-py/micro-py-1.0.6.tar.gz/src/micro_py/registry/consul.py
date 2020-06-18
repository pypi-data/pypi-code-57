import consul

from . import Registry


class Consul(Registry):
    """
    consul 的微服务注册实现
    """

    def __init__(self, server_name: str = "", addr: str = "", port: int = 0, host: str = "",
                 register_interval: int = 0):
        self.register_interval = register_interval
        self.host = host
        self.port = port
        self.addr = addr
        self.server_name = server_name
        (host, port) = host.split(":")
        self.c = consul.Consul(host, port)
        print("consul addr {}".format(host))

    def register(self):
        check = consul.Check.tcp(host=self.addr, port=self.port, interval=self.register_interval,
                                 deregister=self.register_interval + 5)  # 健康检查的ip，端口，检查时间
        self.c.agent.service.register(name=self.server_name, service_id=f"{self.server_name}-{self.addr}-{self.port}",
                                      address=self.addr, port=self.port, check=check)  # 注册服务部分
        print(f"注册服务{self.server_name}成功")

    def deregister(self):
        print(f"开始退出服务{self.server_name}")
        self.c.agent.service.deregister(f'{self.server_name}-{self.addr}-{self.port}')

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
