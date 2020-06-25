import json

from is_url import is_url

from file_util import File


class I:
    def __init__(self, input):
        self._input = input

    @property
    def input(self):
        return self._input

    @property
    def input_string(self):
        """
        :rtype: str
        """
        return self.input

    @property
    def is_string(self):
        return isinstance(self.input, str)

    @property
    def file(self):
        """
        :rtype: pobject.file.File
        """
        return File(self.input)

    @property
    def is_url(self):
        return is_url(self.input)

    @property
    def is_dict(self):
        return isinstance(self.input, dict)

    @property
    def line_count(self):
        line_count = len(self.input_string.split('\n'))
        return line_count

    @property
    def lines(self):
        return self.input_string.split('\n')

    @property
    def lines_with_text(self):
        lines_with_text = [line for line in self.lines if line.strip() != '']
        return lines_with_text

    @property
    def line_count_with_text(self):
        line_count_with_text = len(self.lines_with_text)
        return line_count_with_text

    @property
    def is_file_path(self):
        if self.is_string and ".yaml" in self.input:
            return True
        else:
            raise NotImplementedError

    def to_dict(self):
        if self.is_file_path:
            return self.file.to_dict()

    def to_json_string(self):
        output = json.dumps(self.input)
        return output
