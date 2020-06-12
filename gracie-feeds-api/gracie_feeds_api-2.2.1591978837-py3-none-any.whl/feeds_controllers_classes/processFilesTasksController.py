from gracie_feeds_api import GracieBaseAPI


class processFilesTasksController(GracieBaseAPI):
    """Process files using tasks services and chunking and save results into index."""

    _controller_name = "processFilesTasksController"

    def submit(self, file, privacyMode, projectId, **kwargs):
        """Process the text from file. Supported file formats:  - https://tika.apache.org/1.13/formats.html - .tif, .bmp, .jpg, .png

        Args:
            date: (type, format): The number of seconds since January 1, 1970, 00:00:00 GMT.
            file: (file): file
            languageId: (type): empty - AutoDetect.
            logging: (type): logging
            minRelevancy: (type, format): minRelevancy
            office365EmailType: (type): office365EmailType
            office365EmailsIncludeMode: (type): office365EmailsIncludeMode
            office365Groups: (type, items): office365Groups
            office365MailFolder: (type): office365MailFolder
            privacyMode: (type): In this mode the processed text not saved.
            projectId: (type): projectId
            stopAfterChunkNum: (type, format): Only process the first N number of text chunks when the document requires chunking.

        Consumes:
            multipart/form-data

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'date': {'name': 'date', 'required': False, 'in': 'formData'}, 'file': {'name': 'file', 'required': True, 'in': 'formData'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'formData'}, 'logging': {'name': 'logging', 'required': False, 'in': 'formData'}, 'minRelevancy': {'name': 'minRelevancy', 'required': False, 'in': 'formData'}, 'office365EmailType': {'name': 'office365EmailType', 'required': False, 'in': 'formData'}, 'office365EmailsIncludeMode': {'name': 'office365EmailsIncludeMode', 'required': False, 'in': 'formData'}, 'office365Groups': {'name': 'office365Groups', 'required': False, 'in': 'formData'}, 'office365MailFolder': {'name': 'office365MailFolder', 'required': False, 'in': 'formData'}, 'privacyMode': {'name': 'privacyMode', 'required': True, 'in': 'formData'}, 'projectId': {'name': 'projectId', 'required': True, 'in': 'formData'}, 'stopAfterChunkNum': {'name': 'stopAfterChunkNum', 'required': False, 'in': 'formData'}}
        parameters_names_map = {}
        api = '/process-file-tasks/submit'
        actions = ['post']
        consumes = ['multipart/form-data']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
