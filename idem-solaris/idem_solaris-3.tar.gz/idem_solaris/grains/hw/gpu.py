async def load_num_gpus(hub):
    # TODO figure out how to get gpu info
    # get the model and vendor for each GPU
    hub.grains.GRAINS.gpus = {}
    hub.grains.GRAINS.num_gpus = len(hub.grains.GRAINS.gpus)
