from FaspaySendme import _request, _http

class Services():
    _environment = "development"
    _request = None

    def enableProd(self):
        self._environment = "production"

    def register(self, data={}):
        _http.setEnvironment(_http, self._environment)
        _http.setSection(_http, "register")
        _http.setRequestParam(_http, data)
        _request.generateHeadersRequest(_request)
        _http.generateUrl(_http)
        _http.curl(_http)
        return _http.getResponseParam(_http)

    def confirm(self, data={}):
        _http.setEnvironment(_http, self._environment)
        _http.setSection(_http, "register_confirm")
        _http.setRequestParam(_http, data)
        _request.generateHeadersRequest(_request)
        _http.generateUrl(_http)
        _http.curl(_http)
        return _http.getResponseParam(_http)

    def transfer(self, data={}):
        _http.setEnvironment(_http, self._environment)
        _http.setSection(_http, "transfer")
        _http.setRequestParam(_http, data)
        _request.generateHeadersRequest(_request)
        _http.generateUrl(_http)
        _http.curl(_http)
        return _http.getResponseParam(_http)

    def balance_inquiry(self):
        _http.setEnvironment(_http, self._environment)
        _http.setSection(_http, "balance_inquiry")
        _http.setRequestParam(_http)
        _request.generateHeadersRequest(_request)
        _http.generateUrl(_http)
        _http.curl(_http)
        return _http.getResponseParam(_http)

    def inquiry_name(self, data={}):
        _http.setEnvironment(_http, self._environment)
        _http.setSection(_http, "inquiry_name")
        _http.setRequestParam(_http, data)
        _request.generateHeadersRequest(_request)
        _http.generateUrl(_http)
        _http.curl(_http)
        return _http.getResponseParam(_http)

    def mutasi(self, data={}):
        _http.setEnvironment(_http, self._environment)
        _http.setSection(_http, "mutasi")
        _http.setRequestParam(_http, data)
        _request.generateHeadersRequest(_request)
        _http.generateUrl(_http)
        _http.curl(_http)
        return _http.getResponseParam(_http)

    def inquiry_status(self, data={}):
        _http.setEnvironment(_http, self._environment)
        _http.setSection(_http, "inquiry_status")
        _http.setRequestParam(_http, data)
        _request.generateHeadersRequest(_request)
        _http.generateUrl(_http)
        _http.curl(_http)
        return _http.getResponseParam(_http)
