ID = "id"
MEDIA = "media"
MEDIA_TYPE = "mediaType"
MEDIA_LINK = "link"
PHRASE = "phrase"
TRANSLATION_KEY = "phrase_translation"
QUESTION_TYPE = "questiontype"
OPTIONS = "options"
LEVEL = "level"
IS_LAST_LEVEL = "lastlevel"
TARGET_LEMMA = "targetlemma"
MASTERED = "mastered"
CORRECT = "correct"
N_BAITS = 3
GETYARN_KEY = "getyarn"
TWITTER_KEY = "twitter"
VIDEO = "video"
IMAGE = "image"
TEXT = "text"

class Question():
    def __init__(self):
        self.content_id = None
        self.target_lemma = None
        self.links = None
        self.media_types = None
        self.options = None
        self.phrase = None
        self.phrase_translation = None
        self.question_type = None
        self.baits_type = None
        self.level_to_master = 1
        self.level = 1
        self.mastered = False

    def __repr__(self):
        return "Question({})".format(self.id)  

    @property
    def id(self):
        return "{}_{}_{}_{}_{}".format(self.content_id, 
                                        self.target_lemma, 
                                        self.target_word, 
                                        self.question_type, 
                                        self.baits_type)
    
    @property
    def is_last_level(self):
        return self.level >= self.level_to_master

    def to_json(self):
        question = {ID: self.id,
                    MEDIA: [{MEDIA_TYPE: media_type, 
                                        MEDIA_LINK: link}
                                        for media_type, link in zip(self.media_types,
                                        self.links)],
                    PHRASE: self.phrase,
                    TRANSLATION_KEY: self.phrase_translation,
                    OPTIONS: self.options,
                    QUESTION_TYPE: self.question_type,
                    LEVEL: self.level,
                    IS_LAST_LEVEL: self.is_last_level,
                    TARGET_LEMMA: self.target_lemma,
                    MASTERED: self.mastered}
        return question

