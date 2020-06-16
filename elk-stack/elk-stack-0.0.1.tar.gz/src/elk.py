import json
# from urllib import request
import requests


def check_elastic_connection(elastic_url):
    try:
        response = requests.get(elastic_url)
        return True
    except requests.exceptions.RequestException as e:
        return False

def search(uri, term):
    """Simple Elasticsearch Query"""
    query = json.dumps({
        "query": {
            "match": {
                "content": term
            }
        }
    })

    # response = request.urlopen(url=uri, data=query)
    response = requests.get(uri, data=query)
    results = json.loads(response.text)
    return results


def format_results(results):
    """Print results nicely:
    doc_id) content
    """
    data = [doc for doc in results['hits']['hits']]
    for doc in data:
        print("%s) %s" % (doc['_id'], doc['_source']['content']))


def create_doc(uri, doc_data=dict):
    """Create new document."""
    query = json.dumps(doc_data)
    # response = request.urlopen(uri, data=query)
    response = requests.post(uri, data=query)
    print(response)


check_elastic_connection('http://elastic:13771998g@localhost:9200/')