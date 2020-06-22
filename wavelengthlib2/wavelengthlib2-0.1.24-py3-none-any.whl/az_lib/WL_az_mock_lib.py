''' 
    Mock versions of Azure Function HttpRequest and HttpContext
    Intended to be used to test the WL_Az_http_func_handler Class
    Instances of these Classes can be created, populated and then passed 
    to the WL_Az_http_func_handler constructor
'''      
class MockHttpRequest():
    def __init__(self, req_params, req_file, req_json):
        if req_params:
            self.params = req_params
        else:
            self.params = {}

        if req_json:
            self.json = req_json
        else:
            self.json = {}
 
        self.bin_file = req_file
        return

    def get_json(self):
        return self.json
    
    def get_body(self):
        return self.bin_file

class MockHttpContext():
    def __init__(self, fname):
        self.function_name = fname