import json
from pathlib import Path, PurePath


class IndexUtil:
    """Make index setting json file.
    """

    def __init__(self, filter_dir=None, analyzer_dir=None, mapping_properties_dir=None):
        """Initialize
        
        Args:
            filter_dir (:obj:`str`, optional): filter file directory. Defaults to None.
            analyzer_dir (:obj:`str`, optional): analyzer file directory. Defaults to None.
            mapping_properties_dir (:obj:`str`, optional): mapping properties file directory. Defaults to None.
        """
        self.filter_dir = filter_dir
        self.analyzer_dir = analyzer_dir
        self.mapping_properties_dir = mapping_properties_dir

    def read_file(self, _dir):
        """Read in json file.
        
        Args:
            _dir (:obj:`str`): directory of the json file.

        Return:
            (:obj:`dict`)
        """
        full_dir = str(Path(_dir).expanduser())
        with open(full_dir, 'r') as f:
            return json.load(f)

    def combine_files(self, **kwargs):
        """Combine various settings for index to form a coherent description.
        (https://www.elastic.co/guide/en/elasticsearch/reference/current/search-analyzer.html)

        Args:
            _filter (:obj:`bool`): whether to include filter info.
            analyzer (:obj:`bool`): whether to include analyzer info.
            mappings (:obj:`bool`): whether to include mappings info.

        Return:
            (:obj:`dict`)
        """
        _filter = kwargs.get('_filter')
        analyzer = kwargs.get('analyzer')
        mappings = kwargs.get('mappings')

        result = {}

        if _filter:
            _filter_data = self.read_file(self.filter_dir)
        if analyzer:
            analyzer_data = self.read_file(self.analyzer_dir)
        if mappings:
            mappings_data = self.read_file(self.mapping_properties_dir)
            result['mappings'] = mappings_data

        result['settings'] = {'analysis': {**_filter_data, **analyzer_data}}
        

        return result
        