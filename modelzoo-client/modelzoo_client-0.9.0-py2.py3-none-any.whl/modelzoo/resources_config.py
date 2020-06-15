from typing import Any, Dict


class ResourcesConfig:
    """
    ResourcesConfig specifies optional configuration to use when provisioning a
    model serving container.
    """

    def __init__(self, memory_mb: int = 512, cpu_units: int = 256) -> None:
        """
        memory_mb:
            integer number of megabytes of memory each model container
            should use.

        cpu_units:
            integer number of CPU units each model container should use (1024
            CPU units = 1 vCPU).

        """

        self.memory_mb = memory_mb
        self.cpu_units = cpu_units

    def to_json(self) -> Dict[str, Any]:
        return self.__dict__
