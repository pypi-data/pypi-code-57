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

def athlete_places_player_count():
	players = graph.entities('dbpo:Athlete', entities_col_name='player')\
		.expand('player', [
			('dbpo:team', 'team'), ('dbpp:years', 'years'), ('dbpp:birthPlace', 'place'),
			('foaf:name' , 'name'), ('dbpp:clubs', 'clubs')])\
		.group_by(['place']).count('player', 'count_players', True)
	print(players.to_sparql())
	df = players.execute(client, return_format=output_format)
	#print(df.shape)


def basket_ball_teams_player_count():
	players = graph.entities('dbpo:BasketballPlayer', entities_col_name='player')\
		.expand('player', [('dbpp:team', 'team'), ('dbpp:years', 'years'), ('dbpo:termPeriod', 'period')])\
		.group_by(['team']).count('player', 'count_players', True)
	#print(players.to_sparql())
	df = players.execute(client, return_format=output_format)
	#print(df.shape)

start = time()
basket_ball_teams_player_count()
duration = time()-start

print("Duration of basket_ball_teams_player_count() = {} sec".format(duration))
# 7.063212156295776
# 7.021541357040405 sec
# [8352 rows x 2 columns]




"""
Optimized SPARQL query for basket_ball_teams_player_count on isql
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dbpp: <http://dbpedia.org/property/>
PREFIX dbpr: <http://dbpedia.org/resource/>
PREFIX dbpo: <http://dbpedia.org/ontology/>
SELECT DISTINCT ?team  (COUNT(DISTINCT ?player) AS ?count_players) 
FROM <http://dbpedia.org>
WHERE {
	?player rdf:type dbpo:BasketballPlayer .
	?player dbpp:team ?team .
	?player dbpp:years ?years .
	?player dbpo:termPeriod ?period .
	} GROUP BY ?team 
# 8352 Rows. -- 3537 msec.
# 8352 Rows. -- 3563 msec.
# 8352 Rows. -- 3594 msec.
"""


"""
Naive query for basket_ball_teams_player_count on isql
PREFIX  dbpp: <http://dbpedia.org/property/>
PREFIX  dbpo: <http://dbpedia.org/ontology/>
PREFIX  rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX  dcterms: <http://purl.org/dc/terms/>
PREFIX  rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX  dbpr: <http://dbpedia.org/resource/>

SELECT  ?team ?count_players
FROM <http://dbpedia.org>
WHERE
  { { SELECT DISTINCT  ?team (COUNT(DISTINCT ?player) AS ?count_players)
      WHERE
        { SELECT DISTINCT ?player ?team ?years ?period WHERE {
         { SELECT  ?player
            WHERE
              { ?player  rdf:type  dbpo:BasketballPlayer }
          }
          { SELECT  ?player ?team
            WHERE
              { ?player  dbpp:team  ?team }
          }
          { SELECT  ?player ?years
            WHERE
              { ?player  dbpp:years  ?years }
          }
          { SELECT  ?player ?period
            WHERE
              { ?player  dbpo:termPeriod  ?period }
          }
        }
        } GROUP BY ?team
    }
  }
# 8352 Rows. -- 11343 msec.
# 8352 Rows. -- 11781 msec.
# 8352 Rows. -- 11967 msec.
"""

start = time()
athlete_places_player_count()
duration = time()-start

print("Duration of athlete_places_player_count = {} sec".format(duration))


"""
Optimized SPARQL 
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dbpp: <http://dbpedia.org/property/>
PREFIX dbpr: <http://dbpedia.org/resource/>
PREFIX dbpo: <http://dbpedia.org/ontology/>
SELECT DISTINCT ?place  (COUNT(DISTINCT ?player) AS ?count_players) 
FROM <http://dbpedia.org>
WHERE {
	?player rdf:type dbpo:Athlete .
	?player dbpo:team ?team .
	?player dbpp:years ?years .
	?player dbpp:birthPlace ?place .
	?player foaf:name ?name .
	?player dbpp:clubs ?clubs .
	} GROUP BY ?place 

"""
# 26873 Rows. -- 117498 msec.


"""
Naive query for  athlete_places_player_count on isql
PREFIX  dbpp: <http://dbpedia.org/property/>
PREFIX  dbpo: <http://dbpedia.org/ontology/>
PREFIX  rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX  dcterms: <http://purl.org/dc/terms/>
PREFIX  rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX  dbpr: <http://dbpedia.org/resource/>
PREFIX  foaf: <http://xmlns.com/foaf/0.1/>

SELECT  ?place ?count_players
FROM <http://dbpedia.org>
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
"""
# 26873 Rows. -- 809352 msec.













