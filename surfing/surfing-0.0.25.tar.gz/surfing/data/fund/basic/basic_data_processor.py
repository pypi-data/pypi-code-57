from .basic_data_part1 import BasicDataPart1
from .basic_data_part2_fund_ret import BasicFundRet
from .style_analysis_data import StockFactor
from .basic_data_helper import BasicDataHelper


class BasicDataProcessor(object):
    def __init__(self):
        self._data_helper = BasicDataHelper()
        self.basic_data_part1 = BasicDataPart1(self._data_helper)
        self.basic_fund_ret = BasicFundRet(self._data_helper)
        self._style_analysis = StockFactor(self._data_helper)

    def process_all(self, start_date, end_date):
        failed_tasks = []

        failed_tasks.extend(self.basic_data_part1.process_all(start_date, end_date))
        failed_tasks.extend(self.basic_fund_ret.process_all(end_date))
        failed_tasks.extend(self._style_analysis.process_all(start_date, end_date))

        return failed_tasks

    def get_updated_count(self):
        return self._data_helper._updated_count
