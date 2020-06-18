import os
import signal
import time
from concurrent import futures

import grpc

from . import registry
from . import options


class Flag:
    def __init__(self, name: str, env_var, default):
        """
        定义初始化参数
        :param name: 保存的名字
        :param env_var: 环境变量的名字
        :param default: 默认值
        """
        self.default = default
        self.env_var = env_var
        self.name = name


def extract_entity_and_method(k: str):
    """
    提取protobuf定义的service名字，以及方法名字
    例如：
        /user.srv.User/login -> User,login
        /User/Login -> User-> Login
    :param k:/user.srv.User/login类似这种格式
    :return:
    """
    itmes = k.split("/")
    entity_name = itmes[1]
    s = entity_name.split(".")
    if len(s) >= 2:
        entity_name = s[len(s) - 1]

    return entity_name, itmes[2]


class Service:
    def __init__(self, ops: dict = None,
                 *args: Flag
                 ):
        mate = ops
        if mate is None:
            mate = {}
            # 记录数据，并保留环境变量的值
        # 初始化程序只带解析的环境变量参数
        for (k, v) in options.OPS.items():
            ev = os.getenv(v[0], v[1])
            # 判定是否等于默认值
            if ev == v[1]:
                # 判断是否设置有值，如果有，则不使用默认值
                if mate.get(k) is None:
                    mate[k] = ev
            else:
                mate[k] = ev

        # 初始化自定义的环境变量参数
        for f in args:
            mate[f.name] = os.getenv(f.name, f.default)

        self.registry = registry.Registry()
        if mate["registry"] == "consul":
            self.registry = registry.NewConsul(
                mate["server_name"],
                mate["server_address"],
                mate["server_port"],
                mate["registry_address"],
                mate["register_interval"],
            )

        ser = grpc.server(futures.ThreadPoolExecutor(max_workers=mate["server_pool_size"]))
        self.service = ser
        self.mate = mate

    def get_mate(self, name: str):
        """
        获取init 绑定的环境变量
        :param name: 环境变量的名字
        :return:
        """
        return self.mate[name]

    def addWrapHandler(self, generic_rpc_handlers: [grpc.GenericRpcHandler]):
        self.service.add_generic_rpc_handlers(generic_rpc_handlers)

    def add_generic_rpc_handlers(self, generic_handler):
        """
        添加实现后的gRPC作为服务提供外部访问
        :param servicer:实现gRPC接口的对象实例
        :return:
        """
        service_name = self.get_mate("server_name")
        n_hander = []

        for handler in generic_handler:
            method_handlers = getattr(generic_handler[0], '_method_handlers')
            rpc_method_handlers = {}

            entity_name = ""
            for (k, v) in method_handlers.items():
                entity_name, name = extract_entity_and_method(k)

                rpc_method_handlers[name] = v

            n_hander.append(handler)

            n_hander.append(
                grpc.method_handlers_generic_handler(
                    "{}.{}".format(service_name, entity_name),
                    rpc_method_handlers)
            )

        self.service.add_generic_rpc_handlers(n_hander)

    def run(self):
        port = self.get_mate("server_port")
        host = "{}:{}".format(self.get_mate("server_address"), port)
        self.service.add_insecure_port(host)

        print("Server Listening on {}".format(host))
        print("Registering node: {}:{}".format(self.get_mate("server_name"), self.get_mate("server_id")))
        self.service.start()

        def un(signalnum, handler):
            self.registry.deregister()
            exit(0)

        for sig in [signal.SIGINT, signal.SIGTERM]:
            signal.signal(sig, un)
        self.registry.register()
        self.service.wait_for_termination()
