class LogMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        print(request)

        response = self.get_response(request)
        print(response)

        return response