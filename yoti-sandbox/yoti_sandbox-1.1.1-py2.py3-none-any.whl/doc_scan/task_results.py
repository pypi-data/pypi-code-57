from yoti_python_sdk.doc_scan import constants
from yoti_python_sdk.utils import YotiSerializable


class SandboxTaskResults(YotiSerializable):
    def __init__(self, text_extraction_task):
        self.text_extraction_task = text_extraction_task

    def to_json(self):
        return {constants.ID_DOCUMENT_TEXT_DATA_EXTRACTION: self.text_extraction_task}


class SandboxTaskResultsBuilder(object):
    def __init__(self):
        self.__text_extraction_task = []

    def with_text_extraction_task(self, text_extraction_task):
        self.__text_extraction_task.append(text_extraction_task)
        return self

    def build(self):
        return SandboxTaskResults(self.__text_extraction_task)
