import json

class MSIxReply(object):

    def __init__(self, success, res):
        self.success = success
        self.res = res

    def json(self):
        res = {"success": self.success, "result": self.res}
        return json.dumps(res)
