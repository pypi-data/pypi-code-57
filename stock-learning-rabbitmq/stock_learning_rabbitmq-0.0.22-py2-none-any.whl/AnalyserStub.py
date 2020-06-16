from stock_learning_rabbitmq.Stub import Stub


class AnalyserStub(Stub):
    
    def __init__(self, server):
        super().__init__(server, 'stock-learning-analyser')

    def daily_prediction_startup_handler(self):
        self._send('daily-prediction-startup-handler', {})

    def daily_prediction_closing_handler(self):
        self._send('daily-prediction-closing-handler', {})

    def real_time_value_addition_handler(self, content):
        self._send('real-time-value-addition-handler', content)