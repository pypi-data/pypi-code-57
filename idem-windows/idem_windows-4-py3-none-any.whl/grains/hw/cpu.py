import os


async def load_cpu_model(hub):
    hub.grains.GRAINS.cpu_model = hub.exec.reg.read_value(
        hive="HKEY_LOCAL_MACHINE",
        key="HARDWARE\\DESCRIPTION\\System\\CentralProcessor\\0",
        vname="ProcessorNameString",
    ).get("vdata")


async def load_num_cpus(hub):
    hub.grains.GRAINS.num_cpus = 1
    if "NUMBER_OF_PROCESSORS" in os.environ:
        # Cast to int so that the logic isn't broken when used as a
        # conditional in templating.
        try:
            hub.grains.GRAINS.num_cpus = int(os.environ["NUMBER_OF_PROCESSORS"])
        except ValueError:
            pass
