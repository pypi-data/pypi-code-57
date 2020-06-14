from lxml import html


class Hocron:

    def __init__(self, file_path):
        self.file_path = file_path
        self.doc = html.parse(file_path)

    @property
    def first_word(self):
        words = self.doc.xpath("//*[@class='ocrx_word']")

        if len(words) > 0:
            return words[0].text

        return None
