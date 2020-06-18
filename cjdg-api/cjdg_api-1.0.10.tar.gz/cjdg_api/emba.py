from .base import base


class emba(base):
    def __init__(self, token):
        super().__init__(token)

    def getBook(self):
        api_name = "emba/getBookList"
        return self.request(api_name)

    def getBookDir(self, book_id):
        api_name = "emba/getBookDir"
        data = {}
        data["book_id"] = book_id
        return self.request(api_name)

    def getCourseList(self, interface_type=3):
        # 书的目录结构
        api_name = "emba/getCourseList"
        data = {}
        data["interface_type"] = interface_type
        return self.request(url, data)

    def addTopic(self, data):
        api_name = "activity/addTopic"
        return self.request(api_name, data)
