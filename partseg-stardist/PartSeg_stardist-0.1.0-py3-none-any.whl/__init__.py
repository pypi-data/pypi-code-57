from .stardist_plugin import StardistSegmentation, StardistSegmentation3D

def register():
    print("buka")
    from PartSegCore.register import register, RegisterEnum

    register(StardistSegmentation, RegisterEnum.mask_algorithm)
    register(StardistSegmentation3D, RegisterEnum.mask_algorithm)