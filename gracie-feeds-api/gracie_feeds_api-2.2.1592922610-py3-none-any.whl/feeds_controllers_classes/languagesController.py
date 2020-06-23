from gracie_feeds_api import GracieBaseAPI


class languagesController(GracieBaseAPI):
    """Supported languages."""

    _controller_name = "languagesController"

    def languages(self):
        """Return the list of supported languages."""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/languages'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def retrieve(self, languageId):
        """Return the language with specified ID.

        Args:
            languageId: (string): languageId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'languageId': {'name': 'languageId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/languages/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
