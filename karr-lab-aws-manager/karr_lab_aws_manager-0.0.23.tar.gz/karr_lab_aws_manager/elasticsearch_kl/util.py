from elasticsearch import Elasticsearch, RequestsHttpConnection
from karr_lab_aws_manager.config import config
from karr_lab_aws_manager.elasticsearch_kl import index_setting_file
import requests
import json
from bson import ObjectId
import math
from pathlib import Path
from requests_aws4auth import AWS4Auth
import re
import datetime


class ComplexEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        elif isinstance(o, datetime.datetime):
            return o.__str__()
        return json.JSONEncoder.default(self, o)


class EsUtil(config.establishES):

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
        '''
        super().__init__(config_path=config_path, profile_name=profile_name, credential_path=credential_path,
                        elastic_path=elastic_path, service_name=service_name)
        self.verbose = verbose
        self.max_entries = max_entries
        self.cache_dir = cache_dir
        self.index_setting_manager = index_setting_file.IndexUtil()

    def unassigned_reason(self):
        """sends http request to get why a shard is unassigned

        Returns:
            (HTTPResponse): http response    
        """
        uri = self.es_endpoint + '/' + '_cat/shards?h=index,shard,prirep,state,unassigned.reason'
        r = requests.get(uri, auth=self.awsauth)
        return r

    def allocation_explain(self):
        """chooses the first unassigned shard that it finds and explains why it cannot be allocated to a node

        Returns:
            (HTTPResponse): http response    
        """
        uri = self.es_endpoint + '/_cluster/allocation/explain'
        r = requests.get(uri, auth=self.awsauth)
        return r

    def index_health_status(self):
        """shows the health status, number of documents, and disk usage for each index

        Returns:
            (HTTPResponse): http response    
        """
        uri = self.es_endpoint + '/_cat/indices?v'
        r = requests.get(uri, auth=self.awsauth)
        return r

    def get_index_mapping(self, index='.kibana_1'):
        """Get 
        
        Args:
            index (:obj:`str`, optional): Comma-separated list or wildcard expression of index names. Defaults to '.kibana_1'.

        Returns:
            (:obj:`requests.Response`)
        """
        uri = self.es_endpoint + '/' + index + '/_mapping'
        r = requests.get(uri, auth=self.awsauth)
        return r
    
    def index_settings(self, index, number_of_replicas, number_of_shards=1,
                      other_settings = {}, 
                      headers={ "Content-Type": "application/json" }):
        """Setting index's shard and replica number in es cluster
        
        Args:
            index (str): name of index to be set
            number_of_replicas (int): number of replica shards to be used for the index
            number_of_shards (int): number of primary shards contained in the es cluster
            other_settings (:obj:`dict`): other index settings.
            headers (dict): http request content header description

        Returns:
            (HTTPResponse): http response
        """
        url = self.es_endpoint + '/' + index + '/_settings'
        if number_of_shards == 1:
            body = {"index": {"number_of_replicas": number_of_replicas}}
        else:
            body = {"index": {"number_of_replicas": number_of_replicas,
                            "number_of_shards": number_of_shards}}
        
        if other_settings == {}:
            tmp = body['index']
        else:
            tmp = {**body['index'], **other_settings.get('index')}
        settings = {'index': tmp}
        r = requests.put(url, auth=self.awsauth, data=json.dumps(settings), headers=headers)
        return r

    def create_index(self, index, mappings=None, setting={"settings": {"number_of_shards": 1,
                    "number_of_replicas": 0}}, additional_settings=None):
        """Create index
            (https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-create-index.html)

        Args:
            index (:obj:`str`): name of index
            setting (:obj:`dict`, optional): index settings. Defaults to {"settings": {"number_of_shards": 1}}.
            mappings (:obj:`dict`, optional): index mappings. Deafults to None.
            additional_settings (:obj:`dict`): additional settings. Defaults to None.
        """
        url = self.es_endpoint + '/' + index
        if mappings is not None:
            setting['mappings'] = mappings
        if additional_settings is not None:
            tot_setting = {**setting['settings'], **additional_settings}
            setting['settings'] = tot_setting
        r = requests.put(url, auth=self.awsauth, json=setting)
        return r

    def create_index_with_file(self, index, _file, num_shard=1, num_replica=0):
        """Create index with an index description file
            (https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-create-index.html)

        Args:
            index (:obj:`str`): name of index
            _file (:obj:`dict`): index setting description.
            num_shard (:obj:`int`, optional): number of shards. Defaults to 1.
            num_replica (:obj:`int`, optional): number of replicas. Defaults to 0.

        Return:
            (:obj:`requests.Response`)
        """
        url = self.es_endpoint + '/' + index
        _file['settings']['number_of_shards'] = num_shard
        _file['settings']['number_of_replicas'] = num_replica
        print(_file)
        r = requests.put(url, auth=self.awsauth, json=_file)
        return r

    def migrate_index(self, old_index, new_index, headers={ "Content-Type": "application/json" },
                    number_of_shards=1, number_of_replicas=0):
        """Migrate old index to new index whilst changing shard and replica setting
        
        Args:
            old_index (:obj:`str`): name of the old index.
            new_index (:obj:`str`): name of the new index
            headers (:obj:`HTTP.header`, optional): header. Defaults to { "Content-Type": "application/json" }.
            number_of_shards (:obj:`int`, optional): number of shards for the index. Defaults to 1.
            number_of_replicas (:obj:`int`, optional): number of replicas for the index. Defaults to 1.

        Return:
            (:obj:`list` of :obj:`requests.Response`)
        """
        template = {"index_patterns": [new_index], "settings": {"number_of_shards": number_of_shards,
                                                                "number_of_replicas": number_of_replicas}}
        template_url = self.es_endpoint + '/_template/template_1'
        reindex = {"source": {"index": old_index}, "dest": {"index": new_index}}
        reindex_url = self.es_endpoint + '/_reindex'
        count_url = self.es_endpoint + '/_cat/count/'
        old_index_url = self.es_endpoint + '/' + old_index
        r_template = requests.put(template_url, auth=self.awsauth, json=template)
        r_reindex = requests.post(reindex_url, auth=self.awsauth, json=reindex)
        count_old = requests.get(count_url+old_index, auth=self.awsauth).content.decode('utf-8')
        count_new = requests.get(count_url+new_index, auth=self.awsauth).content.decode('utf-8')
        if count_old.split(' ')[:-1] == count_new.split(' ')[:-1]:
            r = requests.delete(old_index_url, auth=self.awsauth)
        else:
            r = [count_old, count_new]
        return [r_template, r_reindex, r]     

    def put_mapping(self, index, body):
        """Put index mapping to exisiting index.
        (https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-put-mapping.html)
        
        Args:
            index (:obj:`str`): mapping for the index.
            body (:obj:`dict`): mapping description.

        Return:
            (:obj:`requests.Response`)
        """
        url = self.es_endpoint + '/' + index + '/' + '_mapping'
        r = requests.put(url, auth=self.awsauth, json=body)
        return r

    def enable_fielddata(self, index, _type, field):
        """Enable fielddata for type fields
        
        Args:
            index (:obj:`str`): Index in which the operation will be done
            _type (:obj:`str`): Existing mapping for field.
            field (:obj:`str`): name of the field.
        """
        url = self.es_endpoint + '/' + index + '/_mapping'
        body = {
                "properties": {
                    field: { 
                    "type": _type,
                    "fielddata": True
                    }
                }}
        r = requests.put(url, auth=self.awsauth, json=body)
        return r

    def build_es(self, suffix=None):
        ''' build es query object

            Args:
                suffix (:obj:`str`): string trailing es endpoint

            Returns:
                (:obj:`Elasticsearch`): Elasticsearch object
        '''
        if suffix is None:
            uri = self.es_endpoint.split('https://')[1]
        else:
            uri = self.es_endpoint.split('https://')[1] + suffix 
        
        es = Elasticsearch(
            hosts = [{'host': uri, 'port': 443}],
            http_auth = self.awsauth,
            use_ssl = True,
            verify_certs = True,
            connection_class = RequestsHttpConnection
        )
        return es

    def add_field_to_index(self, index, field=None, value=None,
                          query={"match_all": {}},
                          script_type="inline",
                          script_complete=None):
        """Add a field of value to all documents in index
        
        Args:
            index (:obj:`str`): name of index.
            field (:obj:`str`): name of field.
            value (:obj:`Obj`): value of field.
            query(:obj:`Obj`): query of index.
            script_type(:obj:`str`): type of script, inline or store.
            script_complete(:obj:`str`): content of script.

        Return:
            (:obj:`HTTPResponse`): elasticsearch update status description.
        """
        url = self.es_endpoint + '/' + index + '/' + '_update_by_query'
        if value is None:
            script = script_complete
        elif isinstance(value, (int, float, complex)) and not isinstance(value, bool):
            val = str(value)
            script = {script_type: "ctx._source.{} = {}".format(field, val)}
        else:
            val = "\""+value+"\""
            script = {script_type: "ctx._source.{} = {}".format(field, val)}

        body = {
                    "query": query,
                    "script": script
                }
        r = requests.post(url, auth=self.awsauth, json=body)
        return r 

    def make_action_and_metadata(self, index, _id):
        ''' Make action_and_metadata obj for bulk loading
            e.g. { "index": { "_index" : "index", "_id" : "id" } }

            Args:
                index (:obj:`str`): name of index on ES
                _id (:obj:`str`):  unique id for document

            Returns:
                (:obj:`dict`): metadata that conforms to ES bulk load requirement
        '''
        action_and_metadata = {'index': { "_index" : index, "_id" : _id }}
        return action_and_metadata

    def delete_index(self, index, _id=None):
        ''' Delete elasticsearch index

            Args:
                index (:obj:`str`): name of index in es
                _id (:obj:`int`): id of the doc in index (optional)
        '''
        if _id is None:
            url = self.es_endpoint + '/' + index
        else:
            url = self.es_endpoint + '/' + index + '/_doc/' + _id
        r = requests.delete(url, auth=self.awsauth)
        return r.status_code

    def data_to_es_bulk(self, cursor, index='test', count=None, bulk_size=100, _id='uniprot_id',
                        headers={ "Content-Type": "application/json" }):
        ''' Load data into elasticsearch service

            Args:
                count (:obj:`int`): cursor size
                cursor (:obj:`pymongo.Cursor` or :obj:`iter`): documents to be PUT/POST to es
                index (:obj:`str`): name of unique key to be used as index for es
                bulk_size (:obj:`int`): number of documents in one PUT
                headers (:obj:`dict`): http header
                _id (:obj:`str`): key in mogno collection for identification

            Returns:
                (:obj:`set`): set of status codes
        '''
        def gen_bulk_file(_iid, bulk_file):
            action_and_metadata = self.make_action_and_metadata(index, _iid)
            bulk_file += json.dumps(action_and_metadata, cls=ComplexEncoder) + '\n'
            if doc.get('_id') is not None:
                doc['id'] = doc.pop('_id')
            bulk_file += json.dumps(doc, cls=ComplexEncoder) + '\n'  
            return bulk_file

        def mod_cursor(cursor):
            pathlist = Path(cursor).expanduser().glob('**/*.json')
            for path in pathlist:
                with path.open() as f:
                    yield json.load(f)     

        if isinstance(cursor, str):
            count = len(list(Path(cursor).expanduser().glob('**/*.json'))) 
            cursor = mod_cursor(cursor)            
        elif isinstance(cursor, list):
            count = len(cursor) 
        else:
            cursor = cursor       

        url = self.es_endpoint + '/_bulk'
        status_code = {201}
        bulk_file = ''
        tot_rounds = math.ceil(count/bulk_size)        

        for i, doc in enumerate(cursor):
            if i == self.max_entries:
                break
            if self.verbose and i % bulk_size == 0:
                print("Processing bulk {} out of {} ...".format(math.floor(i/bulk_size)+1, tot_rounds))
               
            if i == count - 1:  # last entry
                bulk_file = gen_bulk_file(doc[_id], bulk_file)
                r = requests.post(url, auth=self.awsauth, data=bulk_file, headers=headers)
                status_code.add(r.status_code)
                return r
            elif i % bulk_size != 0 or i == 0: #  bulk_size*(n-1) + 1 --> bulk_size*n - 1
                bulk_file = gen_bulk_file(doc[_id], bulk_file)
            else:               # bulk_size * n
                r = requests.post(url, auth=self.awsauth, data=bulk_file, headers=headers)
                status_code.add(r.status_code)
                bulk_file = gen_bulk_file(doc[_id], '') # reset bulk_file
                
    def data_to_es_single(self, count, cursor, index, _id='uniprot_id',
                          headers={ "Content-Type": "application/json" }):
        ''' Load data into elasticsearch service

            Args:
                count (:obj:`int`): cursor size
                cursor (:obj:`pymongo.Cursor` or :obj:`iter`): documents to be PUT to es
                index (:obj:`str`): name of unique key to be used as index for es
                es_endpoint (:obj:`str`): elasticsearch endpoint
                headers (:obj:`dict`): http header information
                _id (:obj:`str`): key in mongo collection for identification
                
            Returns:
                (:obj:`set`): set of status codes
        '''
        url_root = self.es_endpoint + '/' + index + '/_doc/'
        status_code = {201}
        for i, doc in enumerate(cursor):
            if i == self.max_entries:
                break
            if i % 20 == 0 and self.verbose:
                print("Processing doc {} out of {}...".format(i, min(count, self.max_entries)))
            doc = json.loads(json.dumps(doc, cls=ComplexEncoder))
            url = url_root + doc[_id]
            r = requests.post(url, auth=self.awsauth, json=doc, headers=headers)
            status_code.add(r.status_code)
        return status_code

    def change_field_name(self, pipeline_name, pipeline_description,
                         src_field, target_field, src_idx, dest_idx):
        """Change field name.
        (https://www.elastic.co/guide/en/elasticsearch/reference/current/rename-processor.html)

        Args:
            pipeline_name(:obj:`str`): Name of pipeline.
            pipeline_description(:obj:`str`): Description of pipeline.
            src_field(:obj:`str`): Name of the field before change.
            target_field(:obj:`str`): Name of the field after change.
            src_idx(:obj:`str`): Name of index before change.
            dest_idx(:obj:`str`): Name of index after changes.
        """
        pipeline_url = self.es_endpoint + '/_ingest/pipeline/{}'.format(pipeline_name)
        reindex_url = self.es_endpoint + '/_reindex'
        pipeline = {
                    "description": pipeline_description,
                    "processors":[
                                    {
                                     "rename": 
                                            {
                                            "field": src_field,
                                            "target_field": target_field
                                            }
                                    }
                                 ]
                    }
        r_pipeline = requests.put(pipeline_url, auth=self.awsauth, json=pipeline)
        reindex = {
                    "source": {
                        "index": src_idx
                        },
                    "dest": {
                        "index": dest_idx,
                        "pipeline": pipeline_name
                        }
                   }
        r_reindex = requests.post(reindex_url, auth=self.awsauth, json=reindex)
        return r_pipeline, r_reindex

    def update_alias_to_idx(self, idx, alias, action="add"):
        """Add aliases to an index.
        (https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-aliases.html)

        Args:
            idx(:obj:`str` or :obj:`list` of :obj:`str`): indices official name / names.
            alias(:obj:`str`): index alias.
            action(:obj:`str`): add or remove
        """
        if isinstance(idx, list):
            _key = "indices"
        else:
            _key = "index"
        _input = {
                    "actions" : [
                        {action: {_key : idx, "alias" : alias}}
                    ]
                 }
        alias_url = self.es_endpoint + '/_aliases'
        r = requests.post(alias_url, auth=self.awsauth, json=_input)
        return r.text


def main():
    manager = EsUtil(profile_name='es-poweruser', credential_path='~/.wc/third_party/aws_credentials',
                config_path='~/.wc/third_party/aws_config', elastic_path='~/.wc/third_party/elasticsearch.ini',
                service_name='es', max_entries=float('inf'), verbose=True)

    # r = manager.enable_fielddata('protein', 'text', 'frontend_gene_aggregate')
    # print(r.text)

    # r_pipeline, r_reindex = manager.change_field_name('modify_rna_modification', 'Change kegg_orthology_id in rna_mod to ko_number',
    # 'kegg_orthology_id', 'ko_number', 'rna_modification', 'rna_modification_new')
    # print(r_pipeline.text, r_reindex.text)

    r = manager.update_alias_to_idx(['rna_modification_new'], 'genes', action="remove")
    print(r)

    # script = {
    #             "source": "ctx._source.frontend_gene_aggregate= ctx._source.kegg_orthology_id",
    #             "lang": "painless"
    #          }
    # query = {"bool": {
    #             "must_not": {
    #                 "exists": {
    #                     "field": "kegg_orthology_id"
    #                 }
    #             }
    #         }}
    # r = manager.add_field_to_index("rna_modification", query=query,
    #                                script_complete=script)
    # print(r.text)

if __name__ == "__main__":
    main()