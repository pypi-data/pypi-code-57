
from typing import List

from .fund_score_processor import FundScoreProcessor
from .fund_indicator_processor import FundIndicatorProcessor
from .derived_index_val import IndexValProcess
from .style_analysis_processor import StyleAnalysisProcessor
from .derived_data_helper import DerivedDataHelper


class DerivedDataProcessor(object):
    def __init__(self):
        self._data_helper = DerivedDataHelper()
        self.fund_indicator_processor = FundIndicatorProcessor(self._data_helper)
        self.fund_score_processor = FundScoreProcessor(self._data_helper)
        self.index_val_processor = IndexValProcess(self._data_helper)
        self.style_analysis_processors: List[StyleAnalysisProcessor] = []
        # 暂时只算这三个universe
        for universe in ('hs300', 'csi800', 'all'):
            sap = StyleAnalysisProcessor(self._data_helper, universe)
            self.style_analysis_processors.append(sap)

    def process_all(self, start_date, end_date):
        failed_tasks = []

        failed_tasks.extend(self.fund_indicator_processor.process(start_date, end_date))
        failed_tasks.extend(self.fund_score_processor.process(start_date, end_date))
        failed_tasks.extend(self.index_val_processor.process(start_date, end_date))
        for sap in self.style_analysis_processors:
            failed_tasks.extend(sap.process(start_date, end_date))

        return failed_tasks

    def get_updated_count(self):
        return self._data_helper._updated_count

if __name__ == '__main__':
    ddp = DerivedDataProcessor()
    # start_date = '20200430'
    start_date = '20200605'
    end_date = '20200605'
    ddp.fund_indicator_processor.process(start_date, end_date)
    ddp.fund_score_processor.process(start_date, end_date)
