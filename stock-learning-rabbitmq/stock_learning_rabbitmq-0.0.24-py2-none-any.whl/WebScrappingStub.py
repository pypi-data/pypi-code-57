from stock_learning_rabbitmq.Stub import Stub


class WebScrappingStub(Stub):
    
    def __init__(self, server):
        super().__init__(server, 'stock-learning-web-scrapping')

    def infomoney_ibovespa_company_data(self):
        self._send('infomoney-ibovespa-company-data', {})

    def infomoney_ibovespa_historic_data(self, content):
        self._send('infomoney-ibovespa-historic-data', {})

    def infomoney_ibovespa_live_update(self, content):
        self._send('infomoney-ibovespa-live-update', {})
