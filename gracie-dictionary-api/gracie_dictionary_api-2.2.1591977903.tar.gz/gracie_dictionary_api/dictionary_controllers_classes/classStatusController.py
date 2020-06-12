from gracie_dictionary_api import GracieBaseAPI


class classStatusController(GracieBaseAPI):
    """clssStatus"""

    _controller_name = "classStatusController"

    def list(self, **kwargs):
        """

        Args:
            languageId: (string): languageId
            scope: (string): scope

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'scope': {'name': 'scope', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/classStatus/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def retrieve(self, classId, **kwargs):
        """

        Args:
            classId: (string): classId
            languageId: (string): languageId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'classId': {'name': 'classId', 'required': True, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/classStatus/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
