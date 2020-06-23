GET_USER_RANDOM_QUESTIONS_WITH_CONTENT = """
MATCH (u:USER{{id:'{0}'}})
MATCH (el) - [:HAS_LEMMA]-> (l:LEMMA) <- [rel:HAS_LEMMA] - (w:WORD)
WHERE (u) - [:LIKES] -> (el) and l.text in {1}
OPTIONAL MATCH (u) -[rel1:HAS_SEEN] -(l)
WITH l.text as lemma, collect(distinct(w.text)) as word_list, rel1.level as level, rel1.mastered as mastered

CALL apoc.cypher.run("
    unwind {{word_list}} as x
    CALL apoc.cypher.run('
        WITH {{x}} AS word_
        MATCH (el) - [:HAS_CONTENT] -> (c:CONTENT) - [rel:HAS_WORD] -> (w:WORD{{text:word_}}) 
        WHERE (:USER{{id:\\"{0}\\"}}) - [:LIKES] ->(el:SERIES) 
        RETURN {{content:c, interest:el.name, word:w.text, pos:rel.pos}} as qu LIMIT {2}
        UNION ALL
        WITH {{x}} AS word_
        MATCH (el) - [:HAS_CONTENT] -> (c:CONTENT) - [rel:HAS_WORD] -> (w:WORD{{text:word_}})
        WHERE (:USER{{id:\\"{0}\\"}}) - [:LIKES] ->(el:MOVIE)
        RETURN {{content:c, interest:el.name, word:w.text, pos:rel.pos}} as qu LIMIT {2}
        UNION ALL
        WITH {{x}} AS word_
        MATCH (el) - [:HAS_CONTENT] -> (c:CONTENT) - [rel:HAS_WORD] -> (w:WORD{{text:word_}})
        WHERE (:USER{{id:\\"{0}\\"}}) - [:LIKES] ->(el:ARTIST)
        RETURN {{content:c, interest:el.name, word:w.text, pos:rel.pos}} as qu LIMIT {2}
    ',{{x:x}}) YIELD value
    with x, value.qu as content, rand() as rnd
    return x, content, rnd order by rnd limit 1
    ", {{word_list:word_list}}) YIELD value
RETURN lemma, value.x as word, value.content as content, level, mastered
"""


GET_USER_RANDOM_QUESTIONS_WITH_CONTENT_PAGINATED = """
WITH {} as word_list            
UNWIND word_list as x  
    CALL apoc.cypher.run("
        WITH {{x}} AS lemma_
        MATCH (el) - [:HAS_CONTENT] -> (c:CONTENT) - [rel:HAS_WORD] -> (w:WORD) -[:HAS_LEMMA]-> (l:LEMMA{{text:lemma_}})
        WHERE (:USER{{id:'{}'}}) - [:LIKES] ->(el)
        RETURN {{content:c, interest:el.name, word:w.text, pos:rel.pos, lemma:lemma_}} as qu SKIP {} LIMIT {}",
    {{x:x}}) YIELD value
return x, collect(value.qu) as content_list"""


GET_QUESTION_FROM_USER = """
UNWIND {1} as x
CALL apoc.cypher.run("
	WITH {{x}} AS word_ 
    MATCH (u:USER{{id:'{0}'}})
	MATCH (el) - [:HAS_CONTENT] -> (c:CONTENT) - [rel:HAS_WORD] -> (w:WORD) - [:HAS_LEMMA] -> (l:LEMMA{{text:word_}})
	WHERE (u) -[:LIKES] -> (el:ARTIST) or (u) -[:LIKES] -> (el:MOVIE) or (u) -[:LIKES] -> (el:SERIES)
	RETURN {{content:c, interest:el.name, word:w.text, pos:rel.pos, lemma:l.text}} as qu",
{{x:x}}) YIELD value
return value.qu as qu limit 1
"""

GET_QUESTION_PACKS = """
MATCH (questionPack:QUESTION_PACK) - [rel:HAS_QUESTION_TYPE] -> (questionType:QUESTION_TYPE)
WITH questionPack, rel.level as level, questionType order by level, rel.priority
RETURN questionPack as question_pack, level, collect(questionType) as question_types order by questionPack.code
"""

GET_USER_RANDOM_QUESTIONS_WITH_CONTENT_BY_POS = """
WITH {0} as word_list
unwind word_list as x
CALL apoc.cypher.run("
    WITH {{x}} as x
    CALL apoc.cypher.run('
        WITH {{x}} AS x_
        MATCH (el) - [:HAS_CONTENT] -> (c:CONTENT) - [rel:HAS_WORD{{pos:x_.pos}}] -> (w:WORD) -[:HAS_LEMMA]-(l:LEMMA{{text:x_.text}})
        WHERE (:USER{{id:\\"{1}\\"}}) - [:LIKES] ->(el:SERIES)
        RETURN {{content:c, interest:el.name, word:w.text, pos:rel.pos}} as qu LIMIT {2}
       UNION ALL
        WITH {{x}} AS x_
        MATCH (el) - [:HAS_CONTENT] -> (c:CONTENT) - [rel:HAS_WORD{{pos:x_.pos}}] -> (w:WORD) - [:HAS_LEMMA]-(:LEMMA{{text:x_.text}})
        WHERE (:USER{{id:\\"{1}\\"}}) - [:LIKES] ->(el:MOVIE)
        RETURN {{content:c, interest:el.name, word:w.text, pos:rel.pos}} as qu LIMIT {2}
        UNION ALL
        WITH {{x}} AS x_
        MATCH (el) - [:HAS_CONTENT] -> (c:CONTENT) - [rel:HAS_WORD{{pos:x_.pos}}] -> (w:WORD) -[:HAS_LEMMA]-(:LEMMA{{text:x_.text}})
        WHERE (:USER{{id:\\"{1}\\"}}) - [:LIKES] ->(el:ARTIST)
        RETURN {{content:c, interest:el.name, word:w.text, pos:rel.pos}} as qu LIMIT {2}
    ', {{x:x}}) YIELD value
    with x, value.qu as content, rand() as rnd
    return x, content, rnd order by rnd limit 1
    ", {{x:x}}) YIELD value
RETURN value.x as word, value.content as content
"""

GET_USER_RANDOM_QUESTIONS_WITH_CONTENT_BY_POS_WITHOUT_LEXEMAS = """
WITH {0} as word_list
unwind word_list as x
CALL apoc.cypher.run("
    WITH {{x}} as x
    CALL apoc.cypher.run('
        WITH {{x}} AS x_
        MATCH (el) - [:HAS_CONTENT] -> (c:CONTENT) - [rel:HAS_WORD{{pos:x_.pos}}] -> (w:WORD{{text:x_.text}})
        WHERE (:USER{{id:\\"{1}\\"}}) - [:LIKES] ->(el:SERIES)
        RETURN {{content:c, interest:el.name, word:w.text, pos:rel.pos}} as qu LIMIT {2}
       UNION ALL
        WITH {{x}} AS x_
        MATCH (el) - [:HAS_CONTENT] -> (c:CONTENT) - [rel:HAS_WORD{{pos:x_.pos}}] -> (w:WORD{{text:x_.text}})
        WHERE (:USER{{id:\\"{1}\\"}}) - [:LIKES] ->(el:MOVIE)
        RETURN {{content:c, interest:el.name, word:w.text, pos:rel.pos}} as qu LIMIT {2}
        UNION ALL
        WITH {{x}} AS x_
        MATCH (el) - [:HAS_CONTENT] -> (c:CONTENT) - [rel:HAS_WORD{{pos:x_.pos}}] -> (w:WORD{{text:x_.text}})
        WHERE (:USER{{id:\\"{1}\\"}}) - [:LIKES] ->(el:ARTIST)
        RETURN {{content:c, interest:el.name, word:w.text, pos:rel.pos}} as qu LIMIT {2}
    ', {{x:x}}) YIELD value
    with x, value.qu as content, rand() as rnd
    return x, content, rnd order by rnd limit 1
    ", {{x:x}}) YIELD value
RETURN value.x as word, value.content as content
"""

GET_LEXEMAS_FROM_LEMMA = """
MATCH (l:LEMMA)
WHERE l.text = "{}"
MATCH (w:WORD) -[:HAS_LEMMA] -(l)
WHERE w.text <> l.text
RETURN w.text
"""
