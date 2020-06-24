from .question_creator import QuestionCreator
from ..questions.question import Question, GETYARN_KEY, VIDEO, TWITTER_KEY, IMAGE
import random

PROBABILITY_OF_SHUFFLING_OPTIONS_IN_DUAL_VIDEO = 0.5

class MediasList():
    def __init__(self, links, media_types, phrases, correct_values):
        self.links = links
        self.media_types = media_types
        self.phrases = phrases
        self.correct_values = correct_values

class DualVideoQuestionCreator(QuestionCreator):

    def _get_medias(self, contents):
        """
        Gets links and media types lists depending on type
        """
        links = []
        medias = []
        phrases = []
        correct_values = []
        contents = self._reorder_content(contents)
        for content in contents:
            if content.source == GETYARN_KEY:
                link_mp4 = f"https://y.yarn.co/"f"{content.id}.mp4"
                links.append(link_mp4)
                medias.append(VIDEO)
            if content.source == TWITTER_KEY:
                link_jpg = content.image_link
                links.append(link_jpg)
                medias.append(IMAGE)
            phrases.append(content.phrase)
        number_of_contents = len(contents)
        correct_values = [False if index != self.correct_option_index else True
                          for index in range(0,number_of_contents)]
        return MediasList(links, medias, phrases, correct_values)

    def _reorder_content(self, contents):
        correct_option=contents[0]
        if random.random() < PROBABILITY_OF_SHUFFLING_OPTIONS_IN_DUAL_VIDEO:
            random.shuffle(contents)
        self.correct_option_index = contents.index(correct_option)
        return contents