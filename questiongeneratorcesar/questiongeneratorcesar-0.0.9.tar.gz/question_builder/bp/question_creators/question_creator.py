from question_builder.data import DataQuestion
from ..questions import question
import random 
import re

class QuestionCreator():
    def __init__(self, content_repository):
        self.content_repository = content_repository

    def _get_links_and_media_types(self, content):
        """
        Gets links and media types lists depending on type
        """
        if content.source == question.GETYARN_KEY:
            link_jpg = f"https://y.yarn.co/{content.id}_screenshot.jpg"
            link_mp4 = f"https://y.yarn.co/"f"{content.id}.mp4"
            links = [link_jpg, link_mp4]
            media_types = [question.IMAGE, question.VIDEO]
        if content.source == question.TWITTER_KEY:
            link_jpg = content.image_link
            links = [link_jpg]
            media_types = [question.IMAGE]
        return links, media_types

    def _get_translation(self, content):
        if hasattr(content, 'translation'):
            if content.translation is not None:
                phrase_translation = content.translation.strip()
            else:
                phrase_translation = ""
        else:
            phrase_translation = ""
        return phrase_translation

    def _remove_word(self, phrase, word):
        blank_line = '_'*len(word)
        phrase = re.sub(r"\b" + word + r"(\b|(?=n't))",
                        r' '+ blank_line +' ', phrase, flags=re.I)
        phrase = self._clean_phrase(phrase)
        return phrase

    def _underline_word(self, phrase, word):
        splitted = re.split(word, phrase, flags=re.IGNORECASE)
        formated_word = "\u0332".join(word + " ")
        phrase = formated_word.join(splitted)
        phrase = self._clean_phrase(phrase)
        return phrase

    def _clean_phrase(self, phrase):
        phrase = re.sub(r"(&.*?;)", "", phrase) # &amp; and others
        phrase = re.sub(r"(http[s]?://(.*?)( |,|;|\Z))", "... ", phrase) #URL
        phrase = phrase.replace("\n", " ") # \n
        return phrase

    def _get_options(self, correct_answer, baits):
        """
        Get the baits and the words, and make an array of Options Objects in
        which word is set to True, and all others are False
        """
        options = [{question.TEXT: correct_answer, question.CORRECT: True}]
        for bait in baits:
            options.append({question.TEXT: bait, question.CORRECT: False})
        random.shuffle(options)
        return options
