from .n1ql import *
from couchbase_core.n1ql import N1QLRequest
from couchbase.options import OptionBlockTimeOut
from enum import Enum
from couchbase_core.analytics import AnalyticsQuery, AnalyticsRequest
from couchbase_core import iterable_wrapper
from typing import *


class AnalyticsIndex(dict):
    def __init__(self, **kwargs):
        print("creating index from {}".format(kwargs))
        super(AnalyticsIndex, self).__init__(**kwargs['Index'])

    @property
    def name(self):
        return self.get("IndexName", None)

    @property
    def dataset_name(self):
        return self.get("DatasetName", None)

    @property
    def dataverse_name(self):
        return self.get("DataverseName", None)

    @property
    def is_primary(self):
        return self.get("IsPrimary", None)


class AnalyticsDataType(Enum):
    STRING='string'
    INT64='int64'
    DOUBLE='double'


class AnalyticsDataset(dict):
    def __init__(self, **kwargs):
        super(AnalyticsDataset, self).__init__(**kwargs)

    @property
    def dataset_name(self):
        return self.get("DatasetName", None)

    @property
    def dataverse_name(self):
        return self.get('DataverseName', None)

    @property
    def link_name(self):
        return self.get('LinkName', None)

    @property
    def bucket_name(self):
        return self.get('BucketName', None)


class AnalyticsResult(iterable_wrapper(AnalyticsRequest)):
    def client_context_id(self):
        return super(AnalyticsResult, self).client_context_id()

    def signature(self):
        return super(AnalyticsResult, self).signature()

    def warnings(self):
        return super(AnalyticsResult, self).warnings()

    def request_id(self):
        return super(AnalyticsResult, self).request_id()

    def __init__(self,
                 *args, **kwargs  # type: N1QLRequest
                 ):
        super(AnalyticsResult, self).__init__(*args, **kwargs)


class AnalyticsOptions(OptionBlockTimeOut):
    VALID_OPTS = {'timeout', 'read_only', 'scan_consistency', 'client_context_id', 'positional_parameters',
                  'named_parameters', 'raw'}

    @overload
    def __init__(self,
                 timeout=None,  # type: timedelta
                 read_only=None,  # type: bool
                 scan_consistency=None,  # type: QueryScanConsistency
                 client_context_id=None,  # type: str
                 priority=None,  # type: bool
                 positional_parameters=None,  # type: Iterable[str]
                 named_parameters=None,  # type: Dict[str, str]
                 raw=None,  # type: Dict[str,Any]
                 ):
        """

        :param timeout:
        :param read_only:
        :param scan_consistency:
        :param client_context_id:
        :param priority:
        :param positional_parameters:
        :param named_parameters:
        :param raw:
        """
        pass

    def __init__(self,
                 **kwargs
                 ):
        super(AnalyticsOptions, self).__init__(**kwargs)

    def to_analytics_query(self, statement, *options, **kwargs):
        # lets make a copy of the options, and update with kwargs...
        args = self.copy()
        args.update(kwargs)

        # now lets get positional parameters.  Actual positional
        # params OVERRIDE positional_parameters
        positional_parameters = args.pop('positional_parameters', [])
        if options and len(options) > 0:
            positional_parameters = options

        # now the named parameters.  NOTE: all the kwargs that are
        # not VALID_OPTS must be named parameters, and the kwargs
        # OVERRIDE the list of named_parameters
        new_keys = list(filter(lambda x: x not in self.VALID_OPTS, args.keys()))
        named_parameters = args.pop('named_parameters', {})
        for k in new_keys:
            named_parameters[k] = args[k]

        query = AnalyticsQuery(statement, *positional_parameters, **named_parameters)

        # TODO: there is surely a cleaner way...
        for k in self.VALID_OPTS:
            v = args.get(k, None)
            if v:
                if k == 'scan_consistency':
                    query.consistency = v.as_string()
                if k == 'timeout':
                    query.timeout = v
                if k == 'read_only':
                    query.readonly = v
                if k == 'profile':
                    query.profile = v.as_string()
        return query



