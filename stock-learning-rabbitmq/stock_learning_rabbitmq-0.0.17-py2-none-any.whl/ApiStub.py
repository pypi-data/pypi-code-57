from stock_learning_rabbitmq.Stub import Stub


class ApiStub(Stub):
    
    def __init__(self, server):
        super().__init__(server, 'stock-learning-api')

    def infomoney_ibovespa_company_data(self, content):
        self._send('infomoney-ibovespa-company-data',  content)

    def infomoney_ibovespa_historic_data(self, content):
        self._send('infomoney-ibovespa-historic-data', content)

    def infomoney_ibovespa_live_update(self, content):
        self._send('infomoney-ibovespa-live-update', content)

    def get_daily_companies(self):
        self._send('get-daily-companies', {})

    def get_all_companies(self):
        self._send('get-all-companies', {})

    def live_prediction(self, content):
        self._send('live-prediction', {})