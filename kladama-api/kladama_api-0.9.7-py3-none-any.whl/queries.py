import abc
from abc import ABC

import kladama.entities as kle


class QueryBase:

    @property
    @abc.abstractmethod
    def entity_meta(self) -> kle.EntityMetadata:
        pass

    @property
    @abc.abstractmethod
    def url_path(self) -> str:
        pass


class MultipleResultsQuery(QueryBase, ABC):

    def __init__(self):
        QueryBase.__init__(self)


class SimpleResultsQuery(QueryBase, ABC):

    def __init__(self, query_base: MultipleResultsQuery):
        QueryBase.__init__(self)
        self._query_base = query_base

    @property
    def entity_meta(self):
        return self._query_base.entity_meta


# binary data queries


class BinaryDataQuery(QueryBase, ABC):

    def __init__(self, query_base: SimpleResultsQuery):
        QueryBase.__init__(self)
        self._query_base = query_base

    @property
    def entity_meta(self):
        return None


class AroundQuery(BinaryDataQuery):

    def __init__(self, query_base: SimpleResultsQuery, days: int, *dates):
        BinaryDataQuery.__init__(self, query_base)
        self._days = days
        self._dates = dates

    @property
    def url_path(self) -> str:
        return '{0}/{1}around/{2}'.format(self._query_base.url_path, self._days, ','.join(*self._dates))


class DatesQuery(BinaryDataQuery):

    def __init__(self, query_base: SimpleResultsQuery, *dates):
        BinaryDataQuery.__init__(self, query_base)
        self._dates = dates

    @property
    def url_path(self) -> str:
        return '{0}/dates/{1}'.format(self._query_base.url_path, ','.join(*self._dates))


class LastQuery(BinaryDataQuery):

    def __init__(self, query_base: SimpleResultsQuery):
        BinaryDataQuery.__init__(self, query_base)

    @property
    def url_path(self) -> str:
        return '{0}/last'.format(self._query_base.url_path)


class LastNQuery(BinaryDataQuery):

    def __init__(self, query_base: SimpleResultsQuery, amount: int):
        BinaryDataQuery.__init__(self, query_base)
        self._amount = amount

    @property
    def url_path(self) -> str:
        return '{0}/last{1}'.format(self._query_base.url_path, self._amount)


class LastYearsQuery(BinaryDataQuery):

    def __init__(self, query_base: SimpleResultsQuery, years: int, *dates):
        BinaryDataQuery.__init__(self, query_base)
        self._years = years
        self._dates = dates

    @property
    def url_path(self) -> str:
        return '{0}/{1}years/{2}'.format(self._query_base.url_path, self._years, ','.join(*self._dates))


class PeriodQuery(BinaryDataQuery):

    def __init__(self, query_base: SimpleResultsQuery, from_, to):
        BinaryDataQuery.__init__(self, query_base)
        self._from = from_
        self._to = to

    @property
    def url_path(self) -> str:
        return '{0}/period/{1}TO{2}'.format(self._query_base.url_path, self._from, self._to)


class BinaryAccessibleQuery(QueryBase, ABC):

    def __init__(self, query_base: SimpleResultsQuery):
        QueryBase.__init__(self)
        self._query_base = query_base

    @property
    def query_base(self) -> SimpleResultsQuery:
        return self._query_base

    @property
    def url_path(self):
        return self._query_base.url_path

    def around(self, days: int, *dates):
        return AroundQuery(self.query_base, days, dates)

    def dates(self, *dates):
        return DatesQuery(self.query_base, dates)

    @property
    def last(self):
        return LastQuery(self.query_base)

    def last_n(self, amount: int):
        return LastNQuery(self.query_base, amount)

    def last_years(self, years: int, *dates):
        return LastYearsQuery(self.query_base, years, dates)

    def period(self, from_, to):
        return PeriodQuery(self._query_base, from_, to)


# categorized queries


class EntityQuery(MultipleResultsQuery):

    def __init__(self, entity_meta):
        MultipleResultsQuery.__init__(self)
        self._entity_meta = entity_meta
        self._url_path = '/' + entity_meta.url_base_path

    @property
    def entity_meta(self):
        return self._entity_meta

    @property
    def url_path(self):
        return self._url_path


class SubClassedFilterQuery(MultipleResultsQuery):

    def __init__(self, sub_query, sub_class_path):
        MultipleResultsQuery.__init__(self)
        self._sub_query = sub_query
        self._sub_class_path = sub_class_path

    @property
    def entity_meta(self):
        return self._sub_query.entity_meta

    @property
    def url_path(self):
        return '{0}/{1}'.format(self._sub_query.url_path, self._sub_class_path)


class ForecastQuery(SubClassedFilterQuery):

    def __init__(self, sub_query):
        SubClassedFilterQuery.__init__(self, sub_query, 'forecast')


class ObservedQuery(SubClassedFilterQuery):

    def __init__(self, sub_query):
        SubClassedFilterQuery.__init__(self, sub_query, 'observed')


class PredictableEntityQuery(MultipleResultsQuery, ABC):

    def __init__(self):
        MultipleResultsQuery.__init__(self)

    @property
    def forecast(self):
        return ForecastQuery(self)


class ObservableEntityQuery(MultipleResultsQuery, ABC):

    def __init__(self):
        MultipleResultsQuery.__init__(self)

    @property
    def observed(self):
        return ObservedQuery(self)


class ByNameQueryable(MultipleResultsQuery, ABC):

    def __init__(self):
        MultipleResultsQuery.__init__(self)

    def by_name(self, name_value):
        return ByNameQuery(self, name_value)


class ByPhenomenaQueryable(MultipleResultsQuery, ABC):

    def __init__(self):
        MultipleResultsQuery.__init__(self)

    def by_phenomena(self, phenomena):
        return ByPhenomenaQuery(self, phenomena)


class BySourceQueryable(MultipleResultsQuery, ABC):

    def __init__(self):
        MultipleResultsQuery.__init__(self)

    def by_sources(self, *sources):
        return BySourceQuery(self, sources)


class BySubscriptionQueryable(MultipleResultsQuery, ABC):

    def __init__(self):
        MultipleResultsQuery.__init__(self)

    def by_subsc(self, *subscriptions):
        return BySubscriptionQuery(self, *subscriptions)


class ByUserQueryable(MultipleResultsQuery, ABC):

    def __init__(self):
        MultipleResultsQuery.__init__(self)

    def by_user(self, user):
        return ByUserQuery(self, user)


class ByNameAndUserQueryable(MultipleResultsQuery, ABC):

    def __init__(self):
        MultipleResultsQuery.__init__(self)

    def by_user(self, user):
        return ByNameAndUserQuery(self, user)


class ByUserAndSubscriptionQueryable(MultipleResultsQuery, ABC):

    def __init__(self):
        MultipleResultsQuery.__init__(self)

    def by_user(self, user):
        return ByUserAndSubscriptionQuery(self, user)

# filters


class FilterQuery(QueryBase, ABC):

    def __init__(self, query_base, filter_value):
        QueryBase.__init__(self)
        self._entity_query = query_base
        self._filter_value = filter_value

    @property
    def entity_meta(self):
        return self._entity_query.entity_meta

    @property
    def entity_query(self):
        return self._entity_query

    @property
    def filter_value(self):
        return self._filter_value


class ByNameQuery(FilterQuery, SimpleResultsQuery):

    def __init__(self, query_base: ByNameQueryable, name_value):
        FilterQuery.__init__(self, query_base, name_value)
        SimpleResultsQuery.__init__(self, query_base)

    @property
    def url_path(self):
        return '{0}/{1}'.format(self.entity_query.url_path, self.filter_value)


class ByPhenomenaQuery(FilterQuery, ObservableEntityQuery, PredictableEntityQuery):

    def __init__(self, query_base, phenomena):
        assert isinstance(query_base, ByNameQueryable)
        FilterQuery.__init__(self, query_base, phenomena)
        ObservableEntityQuery.__init__(self)
        PredictableEntityQuery.__init__(self)

    @property
    def url_path(self):
        return '{0}/phenom/{1}'.format(self.entity_query.url_path, self.filter_value)


class BySourceQuery(FilterQuery, ObservableEntityQuery, PredictableEntityQuery):

    def __init__(self, query_base, *sources):
        assert isinstance(query_base, ByNameQueryable)
        FilterQuery.__init__(self, query_base, sources)
        ObservableEntityQuery.__init__(self)
        PredictableEntityQuery.__init__(self)

    @property
    def url_path(self):
        return '{0}/src/{1}'.format(self.entity_query.url_path, ','.join(*self.filter_value))


class BySubscriptionQuery(FilterQuery, MultipleResultsQuery):

    def __init__(self, query_base, *subscriptions):
        FilterQuery.__init__(self, query_base, subscriptions)
        MultipleResultsQuery.__init__(self)

    @property
    def url_path(self) -> str:
        return '{0}/subsc/{1}'.format(self.entity_query.url_path, ','.join(self.filter_value))


class ByUserQuery(FilterQuery, MultipleResultsQuery):

    def __init__(self, query_base, user):
        FilterQuery.__init__(self, query_base, user)
        MultipleResultsQuery.__init__(self)

    @property
    def url_path(self) -> str:
        return '{0}/user/{1}'.format(self.entity_query.url_path, self.filter_value)


class ByNameAndUserQuery(ByUserQuery, ByNameQueryable):

    def __init__(self, query_base, user):
        assert isinstance(query_base, ByNameQueryable)
        ByUserQuery.__init__(self, query_base, user)
        ByNameQueryable.__init__(self)

    def filter_by(self, name):
        return BinaryAccessibleQuery(ByNameQuery(self, name))


class ByUserAndSubscriptionQuery(ByUserQuery, BySubscriptionQueryable):

    def __init__(self, query_base, user):
        ByUserQuery.__init__(self, query_base, user)
        BySubscriptionQueryable.__init__(self)


# entity queries

class AreaOfInterestQuery(EntityQuery, ByNameQueryable, ByNameAndUserQueryable):

    def __init__(self):
        EntityQuery.__init__(self, kle.get_aoi_meta())
        ByNameQueryable.__init__(self)
        ByNameAndUserQueryable.__init__(self)


class PhenomenaQuery(
    EntityQuery,
    ByNameQueryable,
    BySourceQueryable,
    ObservableEntityQuery,
    PredictableEntityQuery
):
    def __init__(self):
        EntityQuery.__init__(self, kle.get_phenom_meta())
        ByNameQueryable.__init__(self)
        BySourceQueryable.__init__(self)
        ObservableEntityQuery.__init__(self)
        PredictableEntityQuery.__init__(self)


class OrganizationQuery(EntityQuery, ByNameQueryable):

    def __init__(self):
        EntityQuery.__init__(self, kle.get_org_meta())
        ByNameQueryable.__init__(self)


class SourceQuery(
    EntityQuery,
    ByNameQueryable,
    ByPhenomenaQueryable,
    ObservableEntityQuery,
    PredictableEntityQuery
):
    def __init__(self):
        EntityQuery.__init__(self, kle.get_src_meta())
        ByNameQueryable.__init__(self)
        ByPhenomenaQueryable.__init__(self)
        ObservableEntityQuery.__init__(self)
        PredictableEntityQuery.__init__(self)


class ScheduleQuery(EntityQuery, ByUserAndSubscriptionQueryable):

    def __init__(self):
        EntityQuery.__init__(self, kle.get_schedule_meta())
        ByUserAndSubscriptionQueryable.__init__(self)


class SubscriptionQuery(EntityQuery, ByNameQueryable, ByNameAndUserQueryable):

    def __init__(self):
        EntityQuery.__init__(self, kle.get_subsc_meta())
        ByNameQueryable.__init__(self)
        ByNameAndUserQueryable.__init__(self)


class UserQuery(EntityQuery, ByNameQueryable):

    def __init__(self):
        EntityQuery.__init__(self, kle.get_user_meta())
        ByNameQueryable.__init__(self)


class VariableQuery(
    EntityQuery,
    ByNameQueryable,
    ByPhenomenaQueryable,
    BySourceQueryable,
    ObservableEntityQuery,
    PredictableEntityQuery
):
    def __init__(self):
        EntityQuery.__init__(self, kle.get_var_meta())
        ByNameQueryable.__init__(self)
        ByPhenomenaQueryable.__init__(self)
        BySourceQueryable.__init__(self)
        ObservableEntityQuery.__init__(self)
        PredictableEntityQuery.__init__(self)
