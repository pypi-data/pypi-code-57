from rdfframes.knowledge_graph import KnowledgeGraph
from rdfframes.dataset.rdfpredicate import RDFPredicate
from rdfframes.client.http_client import HttpClientDataFormat, HttpClient
import time
__author__ = "Ghadeer"


def classes_and_freq():
    endpoint = 'http://10.161.202.101:8890/sparql/'
    port = 8890
    output_format = HttpClientDataFormat.PANDAS_DF
    max_rows = 1000000
    timeout = 12000
    client = HttpClient(endpoint_url=endpoint,
                        port=port,
                        return_format=output_format,
                        timeout=timeout,
                        max_rows=max_rows
                        )

    graph = KnowledgeGraph(graph_uri='http://dbpedia.org')
    triples = graph.classes_and_freq(classes_col_name='class', frequency_col_name='frequency')
    #print(triples.to_sparql())
    df = triples.execute(client, return_format=output_format)
    print(df)


"""
optimized
SPARQL SELECT DISTINCT ?class  (COUNT( ?instance) AS ?frequency)  
FROM <http://dbpedia.org>  WHERE {?instance rdf:type ?class .    } GROUP BY ?class 
 ORDER BY DESC(?frequency);

DISTINCT ?class (COUNT(DISTINCT ?instance) AS ?frequency) FROM <http://dbpedia.org> WHERE {?instance rdf:type ?class . } GROUP BY ?class
 ORDER BY DESC(?frequency);
 
naive:

SPARQL SELECT DISTINCT ?class (COUNT( DISTINCT ?e) AS ?frequency)
where
{
  {select DISTINCT ?e ?class where { ?e rdf:type ?class .}}
}
GROUP BY ?class ORDER BY DESC(?frequency);

 SPARQL SELECT DISTINCT ?class (COUNT(?e)AS ?frequency)  
 where { select DISTINCT ?e ?class where { ?e rdf:type ?class .}} 
  GROUP BY ?class  ORDER BY DESC(?frequency);  

curl --request POST 'http://10.161.202.101:8890/sparql/?' --header 'Accept-Encoding: gzip' --data 'format=outputformat' --data-urlencode 'query= SELECT DISTINCT ?class  (COUNT( ?instance) AS ?frequency)  
FROM <http://dbpedia.org>  WHERE {?instance rdf:type ?class .    } GROUP BY ?class ORDER BY DESC(?frequency)' --output 'out_cout.csv'

isql 8890 user pass exec="SELECT DISTINCT ?class  (COUNT( ?instance) AS ?frequency)  
FROM <http://dbpedia.org>  WHERE {?instance rdf:type ?class .    } GROUP BY ?class 
 ORDER BY DESC(?frequency)" > {/home/gabuoda/count_class.{txt}}
"""

start_time = time.time()
classes_and_freq()
end_time = time.time()

print('Duration = {} sec'.format(end_time-start_time))
