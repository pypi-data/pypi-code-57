import json
from typing import Union

from tokenizer_tools.tagset.offset.corpus import Corpus


class CorpusToRasaJson:
    def __init__(self, corpus: Union[Corpus, None] = None):
        self.corpus = corpus  # type: Corpus

    def read_from_file(self, corpus_file):
        self.corpus = Corpus.read_from_file(corpus_file)

    def convert_to_file(self, output_file):
        json_data = self.convert_to_json()

        with open(output_file, "wt") as fd:
            json.dump(json_data, fd, ensure_ascii=False)

    def convert_to_json(self):
        pass

        rasa_data = {
            "rasa_nlu_data": {
                "common_examples": [],
                "regex_features": [],
                "lookup_tables": [],
                "entity_synonyms": [],
            }
        }

        common_examples = rasa_data["rasa_nlu_data"]["common_examples"]

        for offset_data in self.corpus:
            text_str = "".join(offset_data.text)

            offset_data.span_set.fill_text(text_str)

            data_item = {
                "text": text_str,
                "intent": offset_data.label,
                "entities": [
                    {
                        "start": i.start,
                        "end": i.end,
                        "value": i.value,
                        "entity": i.entity,
                    }
                    for i in offset_data.span_set
                ],
            }

            common_examples.append(data_item)

        return rasa_data
