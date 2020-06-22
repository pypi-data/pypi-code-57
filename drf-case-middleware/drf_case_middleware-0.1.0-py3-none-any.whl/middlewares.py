from humps import camelize, decamelize


class CaseMiddleware:
    def __init__(self, get_response):
         self.get_response = get_response

    def __call__(self, request):
        request.GET = decamelize(request.GET)
        response = self.get_response(request)

        return response
