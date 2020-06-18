from .utils import amp_mode_active


def amp(request):
    return {
        'amp': amp_mode_active(),
    }
