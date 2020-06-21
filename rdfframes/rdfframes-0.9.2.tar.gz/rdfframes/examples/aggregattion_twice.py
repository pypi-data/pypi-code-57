from time import time
from rdfframes.knowledge_graph import KnowledgeGraph
from rdfframes.client.http_client import HttpClientDataFormat, HttpClient


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

graph = KnowledgeGraph(graph_name='dbpedia')

def teams_and_places_count():
	players = graph.entities('dbpo:Athlete', entities_col_name='player')\
		.expand('player', [
			('dbpo:team', 'team'), ('dbpp:years', 'years'), ('dbpp:birthPlace', 'place'),
			('foaf:name' , 'name'), ('dbpp:clubs', 'clubs')]).cache()
	places = players.group_by(['place']).count('player', 'count_players', True)
	teams = players.group_by(['team']).count('player', 'count_players', True)

	df1 = places.execute(client, return_format=output_format)
	df2 = teams.execute(client, return_format=output_format)


"""
Optimized SPARQL 
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dbpp: <http://dbpedia.org/property/>
PREFIX dbpr: <http://dbpedia.org/resource/>
PREFIX dbpo: <http://dbpedia.org/ontology/>
SELECT ?team ?place ?count
FROM <http://dbpedia.org>
WHERE {
	{ SELECT DISTINCT ?team (COUNT(DISTINCT ?athlete)) as ?count
		WHERE {
		?athlete rdf:type dbpo:Athlete . 
		?athlete dbpo:team ?team .
		?athlete foaf:name ?name .
		?athlete dbpp:birthPlace ?place .
		?athlete dbpp:years ?years .
		?athlete dbpp:clubs ?clubs
		} GROUP BY ?team 
	} UNION
	{ SELECT DISTINCT ?place  (COUNT(DISTINCT ?athlete)) as ?count
		WHERE {
		?athlete rdf:type dbpo:Athlete . 
		?athlete dbpo:team ?team .
		?athlete foaf:name ?name .
		?athlete dbpp:birthPlace ?place .
		?athlete dbpp:years ?years .
		?athlete dbpp:clubs ?clubs
		} GROUP BY ?place
	}
	}
55959 Rows. -- 388002 msec.
55959 Rows. -- 392692 msec.

29086 Rows. -- 149326 msec. + 
"""
start = time()
teams_and_places_count()
duration = time()-start

print("Duration of teams_and_places_count = {} sec".format(duration))
# 29086 Rows. -- 149326 msec. + 
# 543.38503241539 sec


"""
Naive query
PREFIX  dbpp: <http://dbpedia.org/property/>
PREFIX  dbpo: <http://dbpedia.org/ontology/>
PREFIX  rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX  dcterms: <http://purl.org/dc/terms/>
PREFIX  rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX  dbpr: <http://dbpedia.org/resource/>
PREFIX  foaf: <http://xmlns.com/foaf/0.1/>

SELECT  ?team ?place ?count_players
FROM <http://dbpedia.org>
WHERE
  {   { SELECT  ?place ?count_players
        WHERE
          { { SELECT DISTINCT  ?place (COUNT(DISTINCT ?athlete) AS ?count_players)
              WHERE
                { SELECT DISTINCT  ?athlete ?team ?name ?place ?years ?clubs
                  WHERE
                    { { SELECT  ?athlete
                        WHERE
                          { ?athlete  rdf:type  dbpo:Athlete }
                      }
                      { SELECT  ?athlete ?team
                        WHERE
                          { ?athlete  dbpo:team  ?team }
                      }
                      { SELECT  ?athlete ?name
                        WHERE
                          { ?athlete  foaf:name  ?name }
                      }
                      { SELECT  ?athlete ?place
                        WHERE
                          { ?athlete  dbpp:birthPlace  ?place }
                      }
                      { SELECT  ?athlete ?years
                        WHERE
                          { ?athlete  dbpp:years  ?years }
                      }
                      { SELECT  ?athlete ?clubs
                        WHERE
                          { ?athlete  dbpp:clubs  ?clubs }
                      }
                    }
                }
              GROUP BY ?place
            }
          }
      }
    UNION
      { SELECT  ?team ?count_players
        WHERE
          { { SELECT DISTINCT  ?team (COUNT(DISTINCT ?athlete) AS ?count_players)
              WHERE
                { SELECT DISTINCT  ?athlete ?team ?name ?place ?years ?clubs
                  WHERE
                    { { SELECT  ?athlete
                        WHERE
                          { ?athlete  rdf:type  dbpo:Athlete }
                      }
                      { SELECT  ?athlete ?team
                        WHERE
                          { ?athlete  dbpo:team  ?team }
                      }
                      { SELECT  ?athlete ?name
                        WHERE
                          { ?athlete  foaf:name  ?name }
                      }
                      { SELECT  ?athlete ?place
                        WHERE
                          { ?athlete  dbpp:birthPlace  ?place }
                      }
                      { SELECT  ?athlete ?years
                        WHERE
                          { ?athlete  dbpp:years  ?years }
                      }
                      { SELECT  ?athlete ?clubs
                        WHERE
                          { ?athlete  dbpp:clubs  ?clubs }
                      }
                    }
                }
              GROUP BY ?team
            }
          }
      }
  }
"""
# 55959 Rows. -- 1656457 msec.


