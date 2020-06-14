from lxml import html

from .line_pattern import LinePattern


class Hocron:
    """
    Receives hocr file type as input and provides
    a set of API function for metadata extraction.
    """

    def __init__(self, file_path):
        self.file_path = file_path
        self.doc = html.parse(file_path)

    @property
    def first_word(self):
        words = self.doc.xpath("//*[@class='ocrx_word']")

        if len(words) > 0:
            return words[0].text

        return None

    def get_labeled_value(self, line_pattern):
        """
        line_pattern is an instance of hocron.line_pattern.LinePattern
        """

        lines = self.doc.xpath("//*[@class='ocr_line']")

        for curr_line in lines:
            words = curr_line.xpath(".//*[@class='ocrx_word']")
            line_of_words = [w.text for w in words]
            matched_words = line_pattern.match(line_of_words)

            if matched_words:
                return line_pattern.get_value(matched_words)

        return None


__all__ = [
    'Hocron',
    'LinePattern'
]
