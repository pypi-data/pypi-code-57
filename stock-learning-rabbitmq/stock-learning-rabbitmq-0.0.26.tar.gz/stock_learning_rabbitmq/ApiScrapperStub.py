from stock_learning_rabbitmq.Stub import Stub


class ApiScrapperStub(Stub):
    
    def __init__(self, server):
        super().__init__(server, 'stock-learning-api-scrapper')

    def fetch_company_news(self, content):
        self._send('fetch-company-news',  content)
