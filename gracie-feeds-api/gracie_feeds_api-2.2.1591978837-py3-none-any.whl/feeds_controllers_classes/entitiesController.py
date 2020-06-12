from gracie_feeds_api import GracieBaseAPI


class entitiesController(GracieBaseAPI):
    """Manager for choosing expected entities in search results for alerts."""

    _controller_name = "entitiesController"

    def geoRetrieve(self, entityId):
        """Return the entity with specified ID.

        Args:
            entityId: (string): entityId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'entityId': {'name': 'entityId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/entities/geo/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def getGeoEntities(self, languageId, name, **kwargs):
        """Return JSON array of the objects which represent the entities with the requested name.

        Args:
            languageId: (string): languageId
            maxEntitiesNumber: (integer): maxEntitiesNumber
            name: (string): name
            onlyDirectChildren: (boolean): onlyDirectChildren
            onlyMainNames: (boolean): onlyMainNames
            parentEntityId: (string): parentEntityId
            sortByPopularity: (boolean): sortByPopularity
            wholeSubTree: (boolean): wholeSubTree

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'languageId': {'name': 'languageId', 'required': True, 'in': 'query'}, 'maxEntitiesNumber': {'name': 'maxEntitiesNumber', 'required': False, 'in': 'query'}, 'name': {'name': 'name', 'required': True, 'in': 'query'}, 'onlyDirectChildren': {'name': 'onlyDirectChildren', 'required': False, 'in': 'query'}, 'onlyMainNames': {'name': 'onlyMainNames', 'required': False, 'in': 'query'}, 'parentEntityId': {'name': 'parentEntityId', 'required': False, 'in': 'query'}, 'sortByPopularity': {'name': 'sortByPopularity', 'required': False, 'in': 'query'}, 'wholeSubTree': {'name': 'wholeSubTree', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/entities/getGeoEntities'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def getTopicEntities(self, languageId, name, **kwargs):
        """Return JSON array of the objects which represent the entities with the requested name.

        Args:
            languageId: (string): languageId
            maxEntitiesNumber: (integer): maxEntitiesNumber
            name: (string): name
            onlyMainNames: (boolean): onlyMainNames
            sortByPopularity: (boolean): sortByPopularity
            topicTypeId: (string): topicTypeId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'languageId': {'name': 'languageId', 'required': True, 'in': 'query'}, 'maxEntitiesNumber': {'name': 'maxEntitiesNumber', 'required': False, 'in': 'query'}, 'name': {'name': 'name', 'required': True, 'in': 'query'}, 'onlyMainNames': {'name': 'onlyMainNames', 'required': False, 'in': 'query'}, 'sortByPopularity': {'name': 'sortByPopularity', 'required': False, 'in': 'query'}, 'topicTypeId': {'name': 'topicTypeId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/entities/getTopicEntities'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def topicRetrieve(self, entityId):
        """Return the entity with specified ID.

        Args:
            entityId: (string): entityId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'entityId': {'name': 'entityId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/entities/topic/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
