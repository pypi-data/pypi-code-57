class Registry:
    """
    用于 微服务注册工具
    """

    def register(self):
        pass

    def deregister(self):
        pass

    def get_service(self, name: str):
        pass

    def list_services(self):
        pass

    def watch(self):
        pass


def NewConsul(*args, **kwargs) -> Registry:
    from . import consul
    return consul.Consul(*args, **kwargs)
