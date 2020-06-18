import abc
from abc import ABC
import json


# Operations

class Operation(ABC):

    @property
    @abc.abstractmethod
    def url_path(self) -> str:
        pass


class PostOperation(Operation, ABC):

    @property
    @abc.abstractmethod
    def post_obj(self):
        pass


class PutOperation(Operation, ABC):

    @property
    @abc.abstractmethod
    def put_obj(self):
        pass


class CreateOperation(Operation, ABC):

    def __init__(self):
        Operation.__init__(self)


class DeleteOperation(Operation, ABC):
    pass


class CreateAreaOfInterestOperation(CreateOperation, PutOperation):

    def __init__(
        self,
        user,
        name,
        description,
        category,
        features
    ):
        CreateOperation.__init__(self)
        PutOperation.__init__(self)
        self._user = user
        self._name = name
        self._description = description
        self._category = category
        self._features = features

    @property
    def url_path(self):
        return "/aoi/user/{0}/{1}".format(self._user, self._name)

    @property
    def put_obj(self):
        return {
            "description": self._description,
            "category": self._category,
            "features": self._features if isinstance(self._features, str) else json.dumps(self._features)
        }


class CreatePeriodicSubscriptionOperation(CreateOperation, PostOperation):

    def __init__(
        self,
        user,
        variable_name,
        variable_source_name,
        spatial_operation_name,
        aoi_name,
    ):
        CreateOperation.__init__(self)
        PostOperation.__init__(self)
        self._user = user
        self._variable_name = variable_name
        self._variable_source_name = variable_source_name
        self._spatial_operation_name = spatial_operation_name
        self._aoi_name = aoi_name

    @property
    def url_path(self):
        return "/subsc/user/{0}".format(self._user)

    @property
    def post_obj(self):
        return {
            "type": "PERIODIC",
            "variable": {
                "name": self._variable_name,
                "source": {
                    "name": self._variable_source_name
                }
            },
            "spatial_operation": {
                "name": self._spatial_operation_name
            },
            "aoi": {
                "name": self._aoi_name
            }
        }


class DeleteAreaOfInterestOperation(DeleteOperation):

    def __init__(self, user, aoi_id):
        DeleteOperation.__init__(self)
        self._user = user
        self._aoi_id = aoi_id

    @property
    def url_path(self) -> str:
        return "/aoi/user/{0}/{1}".format(self._user, self._aoi_id)


class DeleteSubscriptionOperation(DeleteOperation):

    def __init__(self, user, subscription_id):
        DeleteOperation.__init__(self)
        self._user = user
        self._subscription_id = subscription_id

    @property
    def url_path(self) -> str:
        return "/subsc/user/{0}/{1}".format(self._user, self._subscription_id)


class CheckScheduleOperation(PutOperation):

    def __init__(self, user, *subscriptions):
        PutOperation.__init__(self)
        self._user = user
        self._subscriptions = subscriptions

    @property
    def url_path(self) -> str:
        subscriptions_path = ''
        if len(self._subscriptions) > 0:
            subscriptions_path = '/subsc/{0}'.format(','.join(self._subscriptions))

        return '/schedule/user/{0}{1}'.format(self._user, subscriptions_path)

    @property
    def put_obj(self):
        return {}


class ClearScheduleOperation(DeleteOperation):

    def __init__(self, user, *subscriptions):
        DeleteOperation.__init__(self)
        self._user = user
        self._subscriptions = subscriptions

    @property
    def url_path(self) -> str:
        subscriptions_path = ''
        if len(self._subscriptions) > 0:
            subscriptions_path = '/subsc/{0}'.format(','.join(self._subscriptions))

        return '/schedule/user/{0}{1}'.format(self._user, subscriptions_path)


class ReScheduleOperation(PostOperation):

    def __init__(self, user, *subscriptions):
        PostOperation.__init__(self)
        self._user = user
        self._subscriptions = subscriptions

    @property
    def url_path(self) -> str:
        subscriptions_path = ''
        if len(self._subscriptions) > 0:
            subscriptions_path = '/subsc/{0}'.format(','.join(self._subscriptions))

        return '/schedule/user/{0}{1}'.format(self._user, subscriptions_path)

    @property
    def post_obj(self):
        return {}


# Builders

class OperationBuilder(ABC):

    @abc.abstractmethod
    def build(self) -> Operation:
        pass

    @property
    def url_path(self) -> str:
        return self.build().url_path


class CreateAreaOfInterestBuilder(OperationBuilder):

    def __init__(self):
        OperationBuilder.__init__(self)
        self._user = ""
        self._name = ""
        self._description = ""
        self._category = ""
        self._features = {}

    def build(self) -> CreateAreaOfInterestOperation:
        return CreateAreaOfInterestOperation(
            self._user,
            self._name,
            self._description,
            self._category,
            self._features
        )

    def for_user(self, user: str):
        self._user = user
        return self

    def with_name(self, name: str):
        self._name = name
        return self

    def with_description(self, description: str):
        self._description = description
        return self

    def with_category(self, category: str):
        self._category = category
        return self

    def with_features(self, features):
        self._features = features
        return self

    def from_file(self, file_path: str):
        with open(file_path, 'r') as file:
            data = file.read()
            features = json.loads(data)
            self.with_features(features)
            return self


class CreatePeriodicSubscriptionBuilder(OperationBuilder):

    def __init__(self):
        OperationBuilder.__init__(self)
        self._user = ""
        self._subscription_type = ""
        self._variable_name = ""
        self._variable_source_name = ""
        self._spatial_operation_name = ""
        self._aoi_name = ""

    def build(self) -> CreatePeriodicSubscriptionOperation:
        return CreatePeriodicSubscriptionOperation(
            self._user,
            self._variable_name,
            self._variable_source_name,
            self._spatial_operation_name,
            self._aoi_name,
        )

    def for_user(self, user: str):
        self._user = user
        return self

    def with_variable(self, variable_name: str):
        self._variable_name = variable_name
        return self

    def with_source(self, variable_source_name: str):
        self._variable_source_name = variable_source_name
        return self

    def with_operation(self, spatial_operation_name: str):
        self._spatial_operation_name = spatial_operation_name
        return self

    def with_aoi(self, aoi_name: str):
        self._aoi_name = aoi_name
        return self


class DeleteAreaOfInterestBuilder(OperationBuilder):

    def __init__(self):
        OperationBuilder.__init__(self)
        self._user = ""
        self._aoi_id = ""

    def build(self) -> DeleteAreaOfInterestOperation:
        return DeleteAreaOfInterestOperation(self._user, self._aoi_id)

    def from_user(self, user: str):
        self._user = user
        return self

    def with_aoi(self, aoi_id: str):
        self._aoi_id = aoi_id
        return self


class DeleteSubscriptionBuilder(OperationBuilder):

    def __init__(self):
        OperationBuilder.__init__(self)
        self._user = ""
        self._subscription_id = ""

    def build(self) -> DeleteSubscriptionOperation:
        return DeleteSubscriptionOperation(self._user, self._subscription_id)

    def from_user(self, user: str):
        self._user = user
        return self

    def with_subsc(self, subscription_id: str):
        self._subscription_id = subscription_id
        return self


class CheckScheduleBuilder(OperationBuilder):

    def build(self) -> Operation:
        return CheckScheduleOperation(self._user, *self._subscriptions)

    def __init__(self):
        OperationBuilder.__init__(self)
        self._user = ''
        self._subscriptions = []

    def for_user(self, user):
        self._user = user
        return self

    def for_subsc(self, *subscriptions):
        self._subscriptions = subscriptions
        return self


class ClearScheduleBuilder(OperationBuilder):

    def build(self) -> Operation:
        return ClearScheduleOperation(self._user, *self._subscriptions)

    def __init__(self):
        OperationBuilder.__init__(self)
        self._user = ''
        self._subscriptions = []

    def for_user(self, user):
        self._user = user
        return self

    def for_subsc(self, *subscriptions):
        self._subscriptions = subscriptions
        return self


class ReScheduleBuilder(OperationBuilder):

    def build(self) -> Operation:
        return ReScheduleOperation(self._user, *self._subscriptions)

    def __init__(self):
        OperationBuilder.__init__(self)
        self._user = ''
        self._subscriptions = []

    def for_user(self, user):
        self._user = user
        return self

    def for_subsc(self, *subscriptions):
        self._subscriptions = subscriptions
        return self
