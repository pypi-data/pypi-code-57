import itertools
from typing import Dict, List
import collections

from tokenizer_tools.tagset.offset.analysis.express_pattern import \
    ExpressPattern
from tokenizer_tools.tagset.offset.corpus import Corpus
from tokenizer_tools.tagset.offset.analysis.read_markdown import read_markdown


# TODO: PatternCorpus seems is a better name than this
class CorpusPattern(Corpus):
    @classmethod
    def create_from_corpus(cls, corpus: Corpus) -> "CorpusPattern":
        pattern_set = collections.defaultdict(list)
        for doc in corpus:
            pattern = ExpressPattern.convert_to_pattern(doc)
            pattern_set[pattern].append(doc)

        # add docs to doc pattern
        for k, v in pattern_set.items():
            for doc in v:
                k.add_doc(doc)

        return cls(set(pattern_set.keys()))

    def render(self, dictionary: Dict[str, List[str]]):
        doc_list = []

        for pattern in self:
            placeholder_names = [i.entity for i in pattern.get_placeholders()]
            pattern_specific_dictionary = {i: dictionary[i] for i in placeholder_names}

            #
            instance_list_variable = list(itertools.product(*pattern_specific_dictionary.values()))

            for instance_variable in instance_list_variable:
                instance_mapping = dict(
                    zip(pattern_specific_dictionary.keys(),
                        instance_variable))

                doc = pattern.render(instance_mapping)
                doc_list.append(doc)

        return Corpus(doc_list)

    def _render_single_pattern(self, pattern: ExpressPattern):
        pass

    def _generate_entity_candidate(self) -> List[Dict[str, str]]:
        raise NotImplementedError()

    @classmethod
    def read_from_file(cls, data_file):
        with open(data_file) as fd:
            doc_list = read_markdown(fd.read())

        return cls(doc_list)

    def convert_to_md(self) -> str:
        output = ""

        group_by_intent = collections.defaultdict(list)
        for doc in self:
            group_by_intent[doc.intent].append(doc)

        for intent, docs in group_by_intent.items():
            output += "# {}\n".format(intent)

            for doc in docs:
                output += "* {}\n".format(doc.convert_to_md())

            output += "\n"

        return output

    def write_to_file(self, output_file):
        with open(output_file, "wt") as fd:
            fd.write(self.convert_to_md())
