from karr_lab_aws_manager.elasticsearch_kl import util
import requests


class QueryBuilder(util.EsUtil):

    def __init__(self, profile_name=None, credential_path=None,
                config_path=None, elastic_path=None,
                cache_dir=None, service_name='es', max_entries=float('inf'), verbose=False):
        ''' 
            Args:
                profile_name (:obj:`str`): AWS profile to use for authentication
                credential_path (:obj:`str`): directory for aws credentials file
                config_path (:obj:`str`): directory for aws config file
                elastic_path (:obj:`str`): directory for file containing aws elasticsearch service variables
                cache_dir (:obj:`str`): temp directory to store json for bulk upload
                service_name (:obj:`str`): aws service to be used
                max_entries (:obj:`int`): maximum number of operations
                verbose (:obj:`bool`): verbose messages
        '''
        super().__init__(profile_name=profile_name, credential_path=credential_path,
                config_path=config_path, elastic_path=elastic_path,
                cache_dir=cache_dir, service_name=service_name, max_entries=max_entries, verbose=verbose)


    def _set_options(self, query, option_key, option_value, _source={}):
        ''' Builds query options for elasticsearch
            (https://opendistro.github.io/for-elasticsearch-docs/docs/elasticsearch/full-text/#options,
            https://www.elastic.co/guide/en/elasticsearch/reference/7.0/search-request-source-filtering.html)

            Args:
                query_operation(:obj:`dict`): query body
                option_key(:obj:`str`): option name
                option_value(:obj:`str`): option value
                _source(:obj:`Obj`): Source filtering, equivalent of projection in MongoDB

            Returns:
                (:obj:`dict`): new query body
        '''
        if _source != {}:
            query['_source'] = _source
        query_operation = list(query['query'].keys())[0]
        query['query'][query_operation][option_key] = option_value
        return query
    
    def build_simple_query_string_body(self, query_message, **kwargs):
        ''' Builds query portion of the body in request body search
            (https://opendistro.github.io/for-elasticsearch-docs/docs/elasticsearch/full-text/#simple-query-string)

            Args:
                query_message (:obj:`str`): string to be queried for.
                
            Returns:
                (:obj:`dict`): query request body
        '''
        query_operation = 'simple_query_string'
        query = {'query': {query_operation: {'query': query_message}}}

        _source = kwargs.get('_source', {})

        fields = kwargs.get('fields', ['*'])
        query = self._set_options(query, 'fields', fields, _source=_source)

        flags = kwargs.get('flags', 'ALL')
        query = self._set_options(query, 'flags', flags)

        fuzzy_transpositions = kwargs.get('fuzzy_transpositions', True)
        query = self._set_options(query, 'fuzzy_transpositions', fuzzy_transpositions)

        fuzzy_max_expansions = kwargs.get('fuzzy_max_expansions', 50)
        query = self._set_options(query, 'fuzzy_max_expansions', fuzzy_max_expansions)

        fuzzy_prefix_length = kwargs.get('fuzzy_prefix_length', 0)
        query = self._set_options(query, 'fuzzy_prefix_length', fuzzy_prefix_length)

        minimum_should_match = kwargs.get('minimum_should_match', 1)
        query = self._set_options(query, 'minimum_should_match', minimum_should_match)

        analyze_wildcard = kwargs.get('analyze_wildcard', True)
        query = self._set_options(query, 'analyze_wildcard', analyze_wildcard)

        lenient = kwargs.get('lenient', True)
        query = self._set_options(query, 'lenient', lenient)

        quote_field_suffix = kwargs.get('quote_field_suffix', "")
        query = self._set_options(query, 'quote_field_suffix', quote_field_suffix)

        auto_generate_synonyms_phrase_query = kwargs.get('auto_generate_synonyms_phrase_query', True)
        query = self._set_options(query, 'auto_generate_synonyms_phrase_query', auto_generate_synonyms_phrase_query)

        default_operator = kwargs.get('default_operator', 'OR')
        query = self._set_options(query, 'default_operator', default_operator)

        analyzer = kwargs.get('analyzer', 'standard')
        query = self._set_options(query, 'analyzer', analyzer)

        return query

    def build_bool_query_body(self, must=None, _filter=None, should=None, must_not=None,
                              minimum_should_match=0):
        """Building boolean query body
        (https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-bool-query.html)
        
        Args:
            must (:obj:`list` or :obj:`dict`, optional): Body for must. Defaults to None.
            _filter (:obj:`list` or :obj:`dict`, optional): Body for filter. Defaults to None.
            should (:obj:`list` or :obj:`dict`, optional): Body for should. Defaults to None.
            must_not (:obj:`list` or :obj:`dict`, optional): Body for must_not. Defaults to None.
            minimum_should_match (:obj:`int`): The number or percentage of should clauses returned documents must match. Defaults to 0.

        Return:
            (:obj:`dict`): boolean query body
        """
        query = {'query': {'bool': {"minimum_should_match": minimum_should_match}}}

        if must is not None:
            query['query']['bool']['must'] = must
        if _filter is not None:
            query['query']['bool']['filter'] = _filter
        if should is not None:
            query['query']['bool']['should'] = should
        if must_not is not None:
            query['query']['bool']['must_not'] = must_not

        return query