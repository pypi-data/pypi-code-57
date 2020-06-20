class WatchmanLog:
    message = None
    payload = None
    is_valid = True
    log_code = None

    def __init__(self, log_code, message, payload):
        self.message = message
        self.payload = payload
        self.log_code = log_code
        self.validate()


    def validate(self):
        if self.message is None or type(self.message) is not str:
            print("Invalid log data. Message is required.")
            self.is_valid = False
            return

        if self.log_code is None or type(self.log_code) is not str:
            print("Invalid log data. log_code is required and it has to be a string")
            self.is_valid = False
            return

        if self.payload != None and type(self.payload) is not dict:
            print("Invalid log data. Payload has to be a python dictionary.")
            self.is_valid = False
            return

        self.is_valid = True

