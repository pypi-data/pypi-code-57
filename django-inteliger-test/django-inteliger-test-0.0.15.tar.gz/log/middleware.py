from core.views import Inteliger

class LogMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        response = self.get_response(request)
        Inteliger().log(request=request, response=response)
        return response