"""
    CONFIG UTILITIES
        - classes that parse your config file, build a query iterable and yield queries
"""
import yaml
import pandas as pd
import numpy as np

class GAConfigManager:
    """
        Class that parses config .yaml for queries, reader, writer 
        Uses these configs to build required query objects.
    """

    def __init__(self, file_name):
        # load config
        self.config = self._parser(file_name=file_name)
        if self.config.pop('chunk_date_range', False):
            self.config = self._restructure_dateRanges(self.config)
        # get query generator
        self.query_gen, self.additional_args = self._builder(self.config)

    def _prepare_chunked_dates(self, startDate: str, endDate: str, dayFreq: int):
        """
            Split up dates in to multiple startDate, endDate pairs which are dayFreq apart
            args:
                startDate (str) : startDate of date range
                endDate (str) : endDate of date range
                dayFreq (int)  : gap between startDate, endDate within each pairs
            return:
                dateRanges (list of dict)
        """
        dates = pd.Series(pd.date_range(start=startDate, end=endDate))
        df = dates.groupby(np.arange(len(dates))//dayFreq).agg(['first', 'last'])
        return df.rename(
            columns={
                'first':'startDate',
                'last':'endDate'}).astype(str).to_dict('records')

    def _restructure_dateRanges(self, config):
        """
            Restructure dateRanges in to multiple pairs gapped by dayFreq
            args:
                config (dict): config file containing dayFreq, dateRanges keys
            return:
                config (dict)
        """
        # dynamic get kwargs or else set to default
        dayFreq = config.pop('dayFreq', '1d')
        startDate = config.get('dateRanges', [])[0].get('startDate', None)
        endDate = config.get('dateRanges', [])[0].get('endDate', None)
        # restructure dateRanges
        dateRanges = self._prepare_chunked_dates(startDate, endDate, dayFreq)
        # update dateRanges in config
        config.update({'dateRanges':dateRanges})
        return config

    def _generate_queries(self, viewIDs: list, queryConfig: list, dateRanges: list,
                            pageSize: int = 10000, samplingLevel: str = 'LARGE', **kwargs):
        """
        Use the Analytics Service Object to query the
        Google Analytics Reporting API V4.
        args:
            viewIDs (list): list of google analytics view ids
            queryConfig (list): Google query config containing metrics, dimensions, etc.
            dateRanges (list): set of start & end dates.
            pageSize (int): (default: 10000) number of samples per pagination step
            samplingLevel (str): (default:LARGE) sampling level of the query
        yields:
            query generator of queries to run
        """
        # static variables
        for vid in viewIDs:
            for _, single_query in enumerate(queryConfig):
                for dateRange in dateRanges:
                    print("creating a [fields] query")
                    fields = {
                        'viewId': vid,
                        'dateRanges': dateRange,
                        **single_query,
                        "samplingLevel":samplingLevel,
                        "pageSize": pageSize}
                    # building similar queries per vid
                    yield [fields]

    def _parser(self, file_name):
        """Parse config in to dictionary"""
        # load config
        with open(file_name, 'r') as file_:
            return yaml.safe_load(file_)

    def _builder(self, config):
        """Config builder method to generate query configs"""
        additional_args = {}
        # get metadata
        metadata = {
            'dateRanges':self.config.get('dateRanges', None),
            'samplingLevel':self.config.get('samplingLevel', None),
            'pageSize':self.config.get('pageSize', None)
        }
        additional_args.update({'metadata':metadata})
        return self._generate_queries(**config), additional_args

    def get_query(self):
        """Get a Generator for the queries to be executed"""
        return self.query_gen

    def get_additional_args(self):
        """Getter method to get additional arguments"""
        return self.additional_args
