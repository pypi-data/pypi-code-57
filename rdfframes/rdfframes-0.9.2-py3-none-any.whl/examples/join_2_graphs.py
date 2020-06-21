

# graphs that contain the predicate foaf:name
http://dblp.l3s.de
http://dbpedia.org

# graphs that contain the predicate foaf:name with their count in each graph
PREFIX foaf:  <http://xmlns.com/foaf/0.1/>
SELECT DISTINCT ?g COUNT (DISTINCT ?person)
WHERE {
    Graph ?g {?person foaf:name ?name}
} Group By ?g

http://dbpedia.org   6042572
http://dblp.l3s.de   1756129

#predicates occuring in yago and dbpedia
SELECT DISTINCT ?p
WHERE {
    Graph <http://dbpedia.org> {?s ?p ?o}
    Graph <http://yago-knowledge.org/> {?s2 ?p ?o2}
} Limit 10


# architects and their most frequently occuring predicates
PREFIX dbo: <http://dbpedia.org/ontology/>
SELECT ?p COUNT(?architect) as ?count_architects
FROM <http://dbpedia.org>
WHERE {?architect rdf:type dbo:Architect . ?architect ?p ?o} Group By ?p ORDER BY DESC(?count_architects) LIMIT 10

http://dbpedia.org/ontology/wikiPageWikiLink                                      151621
http://www.w3.org/1999/02/22-rdf-syntax-ns#type                                   42276
http://purl.org/dc/terms/subject                                                  23791
http://www.w3.org/2002/07/owl#sameAs                                              21231
http://dbpedia.org/property/wikiPageUsesTemplate                                  19521
http://dbpedia.org/ontology/wikiPageWikiLinkText                                  11208
http://dbpedia.org/ontology/wikiPageExternalLink                                  7915
http://xmlns.com/foaf/0.1/name                                                    4500
http://dbpedia.org/property/name                                                  3799
http://dbpedia.org/ontology/wikiPageID                                            3789



PREFIX dbo: <http://dbpedia.org/ontology/>
SELECT ?p COUNT(?player) as ?count_players
FROM <http://dbpedia.org>
WHERE {?player rdf:type dbo:BasketballPlayer . ?player ?p ?o} Group By ?p ORDER BY DESC(?count_players) LIMIT 10

http://dbpedia.org/ontology/wikiPageWikiLink                                      483890
http://www.w3.org/1999/02/22-rdf-syntax-ns#type                                   162260
http://purl.org/dc/terms/subject                                                  144379
http://dbpedia.org/property/wikiPageUsesTemplate                                  106935
http://www.w3.org/2002/07/owl#sameAs                                              80828
http://dbpedia.org/property/team                                                  57873
http://dbpedia.org/ontology/termPeriod                                            48838
http://dbpedia.org/property/years                                                 40880
http://dbpedia.org/ontology/wikiPageWikiLinkText                                  23258
http://dbpedia.org/ontology/wikiPageExternalLink     



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



# on http: 
curl --request POST 'http://10.161.202.101:8890/sparql/?'  --header 'Accept-Encoding: gzip' --data 'format=text/csv' --data-urlencode 'query=PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbp: <http://dbpedia.org/property/>
SELECT ?team COUNT(?player) as ?count_players
FROM <http://dbpedia.org>
WHERE {
?player rdf:type dbo:BasketballPlayer . 
?player dbp:team ?team .
?player dbp:years ?years .
?player dbo:termPeriod ?period .
} Group By ?team ' --output 'player_count.gz'

time: real	0m0.001s
number of rows: 8367 player_count
