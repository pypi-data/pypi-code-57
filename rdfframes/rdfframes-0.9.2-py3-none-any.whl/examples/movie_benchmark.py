import sys
sys.path.insert(1, '/home/amohamed/RDFframes/')
from time import time
from rdfframes.knowledge_graph import KnowledgeGraph
from rdfframes.client.http_client import HttpClientDataFormat, HttpClient
from rdfframes.client.sparql_endpoint_client import SPARQLEndpointClient
from rdfframes.utils.constants import JoinType
__author__ = "Ghadeer"


endpoint = 'http://10.161.202.101:8890/sparql/'
port = 8890
output_format = HttpClientDataFormat.PANDAS_DF
max_rows = 1000000
timeout = 12000
"""
client = HttpClient(endpoint_url=endpoint,
  port=port,
    return_format=output_format,
    timeout=timeout,
    max_rows=max_rows
    )
"""
client = SPARQLEndpointClient(endpoint)

graph =  KnowledgeGraph(graph_name='dbpedia')


def movies_with_american_actors_cache():
    graph = KnowledgeGraph(graph_name='dbpedia')
    dataset = graph.feature_domain_range('dbpp:starring', 'movie', 'actor')\
        .expand('actor', [('dbpp:birthPlace', 'actor_country'), ('rdfs:label', 'actor_name')])\
        .expand('movie', [('rdfs:label', 'movie_name'), ('dcterms:subject', 'subject'),
                         ('dbpp:country', 'movie_country'), ('dbpp:genre', 'genre', True)])\
        .cache()
    # 26928 Rows. -- 4273 msec.
    american_actors = dataset.filter({'actor_country': ['regex(str(?actor_country), "USA")']})

    # 1606 Rows. -- 7659 msec.
    prolific_actors = dataset.group_by(['actor'])\
        .count('movie', 'movie_count', unique=True).filter({'movie_count': ['>= 20']})

    #663,769 Rows. -- 76704 msec.
    movies = american_actors.join(prolific_actors, join_col_name1='actor', join_type=JoinType.OuterJoin)\
        .join(dataset, join_col_name1='actor')
    #.select_cols(['movie_name', 'actor_name', 'genre'])

    sparql_query = movies.to_sparql()
    print(sparql_query)

    #df = movies.execute(client)
    #print(df.shape)

# 6370 Rows. -- 45812 msec.


def movies_with_american_actors():
  # 29355 Rows. -- 9645 msec.
    graph = KnowledgeGraph(graph_name='dbpedia')

    dataset1 = graph.feature_domain_range('dbpp:starring', 'movie1', 'actor')\
        .expand('actor', [('dbpp:birthPlace', 'actor_country1'), ('rdfs:label', 'actor_name1')])\
        .expand('movie1', [('rdfs:label', 'movie_name1'), ('dcterms:subject', 'subject1'),
                         ('dbpp:country', 'movie_country1'), ('dbpp:genre', 'genre1', True)])
    american_actors = dataset1.filter({'actor_country1': ['regex(str(?actor_country1), "USA")']})

    dataset2 = graph.feature_domain_range('dbpp:starring', 'movie2', 'actor')\
        .expand('actor', [('dbpp:birthPlace', 'actor_country2'), ('rdfs:label', 'actor_name2')])\
        .expand('movie2', [('rdfs:label', 'movie_name2'), ('dcterms:subject', 'subject2'),
                         ('dbpp:country', 'movie_country2'), ('dbpp:genre', 'genre2', True)])
    prolific_actors = dataset2.group_by(['actor'])\
        .count('movie2', 'movie_count2', unique=True).filter({'movie_count2': ['>= 20']})

    movies = american_actors.join(prolific_actors, join_col_name1='actor', join_type=JoinType.OuterJoin)\
    #    .join(dataset, join_col_name1='actor')
    #.select_cols(['movie_name', 'actor_name', 'genre'])

    sparql_query = movies.to_sparql()
    print(sparql_query)



start = time()
movies_with_american_actors_cache() ## change the type here.
duration = time()-start
print("Duration of movies_with_american_actors_cache datasets = {} sec".format(duration))

"""
Optimized with project

PREFIX  dbpp: <http://dbpedia.org/property/>
PREFIX  dcterms: <http://purl.org/dc/terms/>
PREFIX  rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX  dbpo: <http://dbpedia.org/ontology/>
PREFIX  dbpr: <http://dbpedia.org/resource/>

SELECT DISTINCT  *
FROM <http://dbpedia.org>
WHERE
  { { SELECT  *
      WHERE
        {   { SELECT  *
              WHERE
                { ?movie  dbpp:starring    ?actor ;
                          rdfs:label       ?film_name ;
                          dcterms:subject  ?subject ;
                          dbpp:country     ?movie_country .
                  ?actor  dbpp:birthPlace  ?actor_country ;
                          rdfs:label       ?actor_name
                  OPTIONAL
                    { ?movie  dbpp:genre  ?genre }
                  FILTER regex(str(?actor_country), "USA")
                }
            }
          UNION
            { SELECT  ?actor
              WHERE
                { SELECT DISTINCT  ?actor (COUNT(DISTINCT ?movie) AS ?movie_count)
                  WHERE
                    { ?movie  dbpp:starring    ?actor ;
                              rdfs:label       ?film_name ;
                              dcterms:subject  ?subject ;
                              dbpp:country     ?movie_country .
                      ?actor  dbpp:birthPlace  ?actor_country ;
                              rdfs:label       ?actor_name
                      OPTIONAL
                        { ?movie  dbpp:genre  ?genre }
                    }
                  GROUP BY ?actor
                  HAVING ( COUNT(DISTINCT ?movie) >= 200 )
                }
            }
        }
    }
    OPTIONAL
      { SELECT  *
        WHERE
          { ?movie  dbpp:starring    ?actor ;
                    rdfs:label       ?film_name ;
                    dcterms:subject  ?subject ;
                    dbpp:country     ?movie_country .
            ?actor  dbpp:birthPlace  ?actor_country ;
                    rdfs:label       ?actor_name
            OPTIONAL
              { ?movie  dbpp:genre  ?genre }
            FILTER regex(str(?actor_country), "USA")
          }
      }
    OPTIONAL
      { SELECT DISTINCT  ?actor (COUNT(DISTINCT ?movie) AS ?movie_count)
        WHERE
          { ?movie  dbpp:starring    ?actor ;
                    rdfs:label       ?film_name ;
                    dcterms:subject  ?subject ;
                    dbpp:country     ?movie_country .
            ?actor  dbpp:birthPlace  ?actor_country ;
                    rdfs:label       ?actor_name
            OPTIONAL
              { ?movie  dbpp:genre  ?genre }
          }
        GROUP BY ?actor
        HAVING ( COUNT(DISTINCT ?movie) >= 200)
      }
  }
"""



"""
RDFframes with the inner join at the end
PREFIX  dbpp: <http://dbpedia.org/property/>
PREFIX  dcterms: <http://purl.org/dc/terms/>
PREFIX  rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX  dbpo: <http://dbpedia.org/ontology/>
PREFIX  dbpr: <http://dbpedia.org/resource/>

SELECT  *
FROM <http://dbpedia.org>
WHERE
  { { SELECT  *
      WHERE
        { ?movie  dbpp:starring    ?actor .
          ?actor  dbpp:birthPlace  ?actor_country ;
                  rdfs:label       ?actor_name .
          ?movie  rdfs:label       ?movie_name ;
                  dcterms:subject  ?subject ;
                  dbpp:country     ?movie_country
          OPTIONAL
            { ?movie  dbpp:genre  ?genre }
        }
    }
      { SELECT  *
        WHERE
          { { SELECT  *
              WHERE
                { ?movie  dbpp:starring    ?actor .
                  ?actor  dbpp:birthPlace  ?actor_country ;
                          rdfs:label       ?actor_name .
                  ?movie  rdfs:label       ?movie_name ;
                          dcterms:subject  ?subject ;
                          dbpp:country     ?movie_country
                  FILTER regex(str(?actor_country), "USA")
                  OPTIONAL
                    { ?movie  dbpp:genre  ?genre }
                }
            }
            OPTIONAL
              { SELECT DISTINCT  ?actor (COUNT(DISTINCT ?movie) AS ?movie_count)
                WHERE
                  { ?movie  dbpp:starring    ?actor .
                    ?actor  dbpp:birthPlace  ?actor_country ;
                            rdfs:label       ?actor_name .
                    ?movie  rdfs:label       ?movie_name ;
                            dcterms:subject  ?subject ;
                            dbpp:country     ?movie_country
                    OPTIONAL
                      { ?movie  dbpp:genre  ?genre }
                  }
                GROUP BY ?actor
                HAVING ( COUNT(DISTINCT ?movie) >= 200 )
              }
          }
      }
    UNION
      { SELECT  *
        WHERE
          { { SELECT DISTINCT  ?actor (COUNT(DISTINCT ?movie) AS ?movie_count)
              WHERE
                { ?movie  dbpp:starring    ?actor .
                  ?actor  dbpp:birthPlace  ?actor_country ;
                          rdfs:label       ?actor_name .
                  ?movie  rdfs:label       ?movie_name ;
                          dcterms:subject  ?subject ;
                          dbpp:country     ?movie_country
                  OPTIONAL
                    { ?movie  dbpp:genre  ?genre }
                }
              GROUP BY ?actor
              HAVING ( COUNT(DISTINCT ?movie) >= 200 )
            }
            OPTIONAL
              { SELECT  *
                WHERE
                  { ?movie  dbpp:starring    ?actor .
                    ?actor  dbpp:birthPlace  ?actor_country ;
                            rdfs:label       ?actor_name .
                    ?movie  rdfs:label       ?movie_name ;
                            dcterms:subject  ?subject ;
                            dbpp:country     ?movie_country
                    FILTER regex(str(?actor_country), "USA")
                    OPTIONAL
                      { ?movie  dbpp:genre  ?genre }
                  }
              }
          }
      }
  }
"""



"""
Naive

PREFIX  dbpp: <http://dbpedia.org/property/>
PREFIX  dcterms: <http://purl.org/dc/terms/>
PREFIX  rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX  dbpo: <http://dbpedia.org/ontology/>
PREFIX  dbpr: <http://dbpedia.org/resource/>

SELECT  *
FROM <http://dbpedia.org>
WHERE
  { { SELECT  *
      WHERE
        { {SELECT * WHERE {?movie  dbpp:starring    ?actor .}}
          {SELECT * WHERE {?actor  dbpp:birthPlace  ?actor_country }}
          {SELECT * WHERE { ?actor       rdfs:label       ?actor_name .}}
          {SELECT * WHERE {?movie  rdfs:label       ?movie_name }}
          {SELECT * WHERE {   ?movie     dcterms:subject  ?subject }}
          {SELECT * WHERE {  ?movie      dbpp:country     ?movie_country}}
          OPTIONAL
            { ?movie  dbpp:genre  ?genre }
        }
    }
    {   { SELECT  *
          WHERE
            { { SELECT  *
                WHERE
                  { { SELECT  *
                      WHERE
                        { ?movie  dbpp:starring  ?actor }
                    }
                    { SELECT  *
                      WHERE
                        { ?actor  dbpp:birthPlace  ?actor_country }
                    }
                    { SELECT  *
                      WHERE
                        { ?actor  rdfs:label  ?actor_name }
                    }
                    { SELECT  *
                      WHERE
                        { ?movie  rdfs:label  ?movie_name }
                    }
                    { SELECT  *
                      WHERE
                        { ?movie  dcterms:subject  ?subject }
                    }
                    { SELECT  *
                      WHERE
                        { ?movie  dbpp:country  ?movie_country }
                    }
                    FILTER regex(str(?actor_country), "USA")
                    { SELECT  *
                      WHERE
                        { OPTIONAL
                            { ?movie  dbpp:genre  ?genre }
                        }
                    }
                  }
              }
              OPTIONAL
                { SELECT DISTINCT  ?actor (COUNT(DISTINCT ?movie) AS ?movie_count)
                  WHERE
                    { { SELECT  *
                        WHERE
                          { ?movie  dbpp:starring  ?actor }
                      }
                      { SELECT  *
                        WHERE
                          { ?actor  dbpp:birthPlace  ?actor_country }
                      }
                      { SELECT  *
                        WHERE
                          { ?actor  rdfs:label  ?actor_name }
                      }
                      { SELECT  *
                        WHERE
                          { ?movie  rdfs:label  ?movie_name }
                      }
                      { SELECT  *
                        WHERE
                          { ?movie  dcterms:subject  ?subject }
                      }
                      { SELECT  *
                        WHERE
                          { ?movie  dbpp:country  ?movie_country }
                      }
                      { SELECT  *
                        WHERE
                          { OPTIONAL
                              { ?movie  dbpp:genre  ?genre }
                          }
                      }
                    }
                  GROUP BY ?actor
                  HAVING ( COUNT(DISTINCT ?movie) >= 200 )
                }
            }
        }
      UNION
        { SELECT  *
          WHERE
            { { SELECT DISTINCT  ?actor (COUNT(DISTINCT ?movie) AS ?movie_count)
                WHERE
                  { { SELECT  *
                      WHERE
                        { ?movie  dbpp:starring  ?actor }
                    }
                    { SELECT  *
                      WHERE
                        { ?actor  dbpp:birthPlace  ?actor_country }
                    }
                    { SELECT  *
                      WHERE
                        { ?actor  rdfs:label  ?actor_name }
                    }
                    { SELECT  *
                      WHERE
                        { ?movie  rdfs:label  ?movie_name }
                    }
                    { SELECT  *
                      WHERE
                        { ?movie  dcterms:subject  ?subject }
                    }
                    { SELECT  *
                      WHERE
                        { ?movie  dbpp:country  ?movie_country }
                    }
                    { SELECT  *
                      WHERE
                        { OPTIONAL
                            { ?movie  dbpp:genre  ?genre }
                        }
                    }
                  }
                GROUP BY ?actor
                HAVING ( COUNT(DISTINCT ?movie) >= 200 )
              }
              OPTIONAL
                { SELECT  *
                  WHERE
                    { { SELECT  *
                        WHERE
                          { ?movie  dbpp:starring  ?actor }
                      }
                      { SELECT  *
                        WHERE
                          { ?actor  dbpp:birthPlace  ?actor_country }
                      }
                      { SELECT  *
                        WHERE
                          { ?actor  rdfs:label  ?actor_name }
                      }
                      { SELECT  *
                        WHERE
                          { ?movie  rdfs:label  ?movie_name }
                      }
                      { SELECT  *
                        WHERE
                          { ?movie  dcterms:subject  ?subject }
                      }
                      { SELECT  *
                        WHERE
                          { ?movie  dbpp:country  ?movie_country }
                      }
                      FILTER regex(str(?actor_country), "USA")
                      { SELECT  *
                        WHERE
                          { OPTIONAL
                              { ?movie  dbpp:genre  ?genre }
                          }
                      }
                    }
                }
            }
        }
    }
  }
"""