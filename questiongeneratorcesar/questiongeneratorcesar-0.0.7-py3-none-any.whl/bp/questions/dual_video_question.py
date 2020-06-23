from . import question

class DualVideoQuestion(question.Question):

    def to_json(self):
        question_ = {question.ID: self.id,
                    question.MEDIA: [{question.MEDIA_TYPE: media_type, 
                                    question.MEDIA_LINK: link, 
                                    question.PHRASE: phrase, 
                                    question.CORRECT: correct_value}
                            for media_type, link, phrase, correct_value in zip(
                                self.media_types, self.links, self.phrases,
                                self.correct_values)],
                    question.PHRASE: self.phrase,
                    question.TRANSLATION_KEY: self.phrase_translation,
                    question.OPTIONS: self.options,
                    question.QUESTION_TYPE: self.question_type,
                    question.LEVEL: self.level,
                    question.IS_LAST_LEVEL: self.is_last_level,
                    question.TARGET_LEMMA: self.target_lemma,
                    question.MASTERED: self.mastered}
        return question_