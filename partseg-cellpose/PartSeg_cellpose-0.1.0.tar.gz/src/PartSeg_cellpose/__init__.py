from .cellpose_plugin import CellposeCytoSegmentation


def register():
    print("buka")
    from PartSegCore.register import register, RegisterEnum

    register(CellposeCytoSegmentation, RegisterEnum.mask_algorithm)
