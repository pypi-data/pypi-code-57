from rdfframes.knowledge_graph import KnowledgeGraph
from rdfframes.dataset.rdfpredicate import RDFPredicate
from rdfframes.client.http_client import HttpClientDataFormat, HttpClient
import time
__author__ = "Ghadeer"


def expand_optional():
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

    graph = KnowledgeGraph(
        graph_name = 'dblp',
        graph_uri='http://dblp.l3s.de',
        prefixes={
            "xsd": "http://www.w3.org/2001/XMLSchema#",
            "swrc": "http://swrc.ontoware.org/ontology#",
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "dc": "http://purl.org/dc/elements/1.1/",
            "dcterm": "http://purl.org/dc/terms/",
            "dblprc": "http://dblp.l3s.de/d2r/resource/conferences/"
      })
    dataset = graph.entities(class_name='swrc:InProceedings',
                             new_dataset_name='papers',
                             entities_col_name='paper')
    dataset = dataset.expand(src_col_name='paper', predicate_list=[
        RDFPredicate('dc:title', 'title'),
        RDFPredicate('dc:creator', 'author'),
        RDFPredicate('dcterm:issued', 'date', True),
        RDFPredicate('swrc:series', 'conference', True)]).select_cols(['paper','title','date','author','conference'])
    #print("SPARQL Query = \n{}".format(dataset.to_sparql()))
    df = dataset.execute(client, return_format=output_format)
    #print(df)


"""
optimized


PREFIX  swrc: <http://swrc.ontoware.org/ontology#>
PREFIX  rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX  dcterm: <http://purl.org/dc/terms/>
PREFIX  xsd:  <http://www.w3.org/2001/XMLSchema#>
PREFIX  dc:   <http://purl.org/dc/elements/1.1/>
PREFIX  dblprc: <http://dblp.l3s.de/d2r/resource/conferences/>
SELECT DISTINCT ?paper ?title ?date ?author ?conference
FROM <http://dblp.l3s.de>
WHERE
  { ?paper  dc:title       ?title ;
            rdf:type       swrc:InProceedings ;
            dc:creator  ?author.
            
    OPTIONAL
      { ?paper sdcterm:issued  ?date. }
    OPTIONAL
      { ?paper  swrc:series  ?conference. }
  }


PREFIX  swrc: <http://swrc.ontoware.org/ontology#>
PREFIX  rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX  dcterm: <http://purl.org/dc/terms/>
PREFIX  xsd:  <http://www.w3.org/2001/XMLSchema#>
PREFIX  dc:   <http://purl.org/dc/elements/1.1/>
PREFIX  dblprc: <http://dblp.l3s.de/d2r/resource/conferences/>
SELECT  ?paper ?title ?date ?author ?conference 
FROM <http://dblp.l3s.de>
WHERE
  { ?paper  dc:title       ?title ;
            rdf:type       swrc:InProceedings ;
            dcterm:issued  ?date ;
            dc:creator     ?author ;
            swrc:series    ?conference
  }

naive:

PREFIX  swrc: <http://swrc.ontoware.org/ontology#>
PREFIX  rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX  dcterm: <http://purl.org/dc/terms/>
PREFIX  xsd:  <http://www.w3.org/2001/XMLSchema#>
PREFIX  dc:   <http://purl.org/dc/elements/1.1/>
PREFIX  dblprc: <http://dblp.l3s.de/d2r/resource/conferences/>
SELECT  ?paper ?title ?date ?author ?conference
FROM <http://dblp.l3s.de>
WHERE
  { { SELECT  ?paper ?title
      WHERE
        { ?paper  dc:title  ?title }
    }
    { SELECT  ?paper
      WHERE
        { ?paper  rdf:type  swrc:InProceedings }
    }
    { SELECT  ?paper ?date
      WHERE
        { ?paper  dcterm:issued  ?date }
    }
    OPTIONAL
      { { SELECT  ?paper ?author
          WHERE
            { ?paper  dc:creator  ?author }
        }
      }
    OPTIONAL
      { { SELECT  ?paper ?conference
          WHERE
            { ?paper  swrc:series  ?conference }
        }
      }
  }
"""

start_time = time.time()
expand_optional()
end_time = time.time()

print('Duration = {} sec'.format(end_time-start_time))
