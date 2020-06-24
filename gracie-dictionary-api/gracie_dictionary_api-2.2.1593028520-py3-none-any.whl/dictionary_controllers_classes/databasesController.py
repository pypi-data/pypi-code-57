from gracie_dictionary_api import GracieBaseAPI


class databasesController(GracieBaseAPI):
    """Databases Controller"""

    _controller_name = "databasesController"

    def archive(self, classifierId, **kwargs):
        """

        Args:
            classifierId: (string): classifierId
            languageId: (string): languageId

        Consumes:
            application/json

        Returns:
            application/json
        """

        all_api_parameters = {'classifierId': {'name': 'classifierId', 'required': True, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/databases/archive'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def backup(self, **kwargs):
        """

        Args:
            incremental: (boolean): incremental
            removeFolder: (boolean): removeFolder
            zip: (boolean): zip

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'incremental': {'name': 'incremental', 'required': False, 'in': 'query'}, 'removeFolder': {'name': 'removeFolder', 'required': False, 'in': 'query'}, 'zip': {'name': 'zip', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/databases/backup'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def exportDatabases(self, **kwargs):
        """

        Args:
            databaseId: (string): Id is some of { country, topic, skillSet, skill, clusterSet, clusterGroup, cluster, profile }. If empty then export all databases.
            password: (string): password

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'databaseId': {'name': 'databaseId', 'required': False, 'in': 'query'}, 'password': {'name': 'password', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/databases/exportDatabases'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def importDatabases(self, file, **kwargs):
        """

        Args:
            conflictsResolving: (string): conflictsResolving
            file: (file): file
            password: (string): password

        Consumes:
            multipart/form-data

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'conflictsResolving': {'name': 'conflictsResolving', 'required': False, 'in': 'query'}, 'file': {'name': 'file', 'required': True, 'in': 'formData'}, 'password': {'name': 'password', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/databases/importDatabases'
        actions = ['post']
        consumes = ['multipart/form-data']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def updateBinaries(self, **kwargs):
        """

        Args:
            forceUpdateUnchanged: (boolean): forceUpdateUnchanged

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'forceUpdateUnchanged': {'name': 'forceUpdateUnchanged', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/databases/updateBinaries'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def updateDictionaries(self, **kwargs):
        """

        Args:
            dictionaryId: (string): dictionaryId
            recalculateDocumentsVectors: (boolean): recalculateDocumentsVectors

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'dictionaryId': {'name': 'dictionaryId', 'required': False, 'in': 'query'}, 'recalculateDocumentsVectors': {'name': 'recalculateDocumentsVectors', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/databases/updateDictionaries'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def updateDoc2vec(self):
        """"""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/databases/updateDoc2vec'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def updateIdfModel(self):
        """"""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/databases/updateIdfModel'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def updateProfiles(self, **kwargs):
        """

        Args:
            id: (string): id
            updateDocuments: (boolean): updateDocuments

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': False, 'in': 'query'}, 'updateDocuments': {'name': 'updateDocuments', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/databases/updateProfiles'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def updateSkillsets(self, **kwargs):
        """

        Args:
            recalculateDocumentsVectors: (boolean): recalculateDocumentsVectors
            skillId: (string): skillId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'recalculateDocumentsVectors': {'name': 'recalculateDocumentsVectors', 'required': False, 'in': 'query'}, 'skillId': {'name': 'skillId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/databases/updateSkillsets'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
