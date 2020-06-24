from log.views import Log

class LogMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        response = self.get_response(request)
        Log().salvar(request=request, response=response)
        return response