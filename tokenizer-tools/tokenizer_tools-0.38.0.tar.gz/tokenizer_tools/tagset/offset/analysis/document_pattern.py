import copy
from collections import OrderedDict
from typing import List
import itertools

from tokenizer_tools.tagset.offset.analysis.entity_placeholder import EntityPlaceholder
from tokenizer_tools.tagset.offset.document import Document
from tokenizer_tools.tagset.offset.span import Span

# TODO: PatternDocument seems better than this name
class DocumentPattern(Document):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # docs which can reduce to this pattern
        self.docs = []

    @classmethod
    def build_from_document(cls, doc: Document) -> "DocumentPattern":
        doc_pattern = cls._copy_structure_from_doc(doc)
        doc_pattern._convert_span()

        return doc_pattern

    def _convert_span(self):
        span_set = self.span_set

        offset = 0

        for index, span in enumerate(span_set):
            # consider effect of offset
            real_start = span.start - offset
            real_end = span.end - offset

            placeholder = EntityPlaceholder(
                start=real_start, end=real_start + 1, entity=span.entity
            )

            span.host.text[real_start:real_end] = [placeholder.entity]

            # update offset
            offset_caused_by_this_turn = span.end - span.start - 1
            offset += offset_caused_by_this_turn

            # replace object in span_set
            span.host.span_set[index] = placeholder

    @classmethod
    def _copy_structure_from_doc(cls, doc) -> "DocumentPattern":
        dp = cls(copy.deepcopy(doc.text))

        attrs_need_be_copied = ["label", "domain", "intent", "function", "sub_function"]

        for attr in attrs_need_be_copied:
            setattr(dp, attr, getattr(doc, attr))

        dp.entities = copy.deepcopy(doc.entities)
        dp.entities.bind(dp)

        return dp

    def _copy_structure_as_doc(self) -> Document:
        doc = Document(copy.deepcopy(self.text))

        attrs_need_be_copied = ["label", "domain", "intent", "function", "sub_function"]

        for attr in attrs_need_be_copied:
            setattr(doc, attr, getattr(self, attr))

        doc.span_set = copy.deepcopy(self.span_set)
        doc.span_set.bind(doc)

        return doc

    def get_placeholders(self) -> List[EntityPlaceholder]:
        return [i for i in self.span_set if isinstance(i, EntityPlaceholder)]

    def render(self, kwargs) -> Document:
        # TODO: compute as stream of block will be more readable

        result_doc = self._copy_structure_as_doc()

        offset = 0
        for idx, span in enumerate(result_doc.span_set):
            if isinstance(span, EntityPlaceholder):
                new_value = kwargs[span.entity]

                # true start/end
                true_start = span.start + offset
                true_end = span.end + offset

                # update text
                result_doc.text[true_start:true_end] = new_value

                # compute new span start/end
                new_start = true_start
                new_end = true_start + len(new_value)

                # replace EntityPlaceholder with Span
                result_doc.span_set[idx] = Span(
                    start=new_start, end=new_end, entity=span.entity
                )

                # update offset
                offset += len(new_value) - 1

        return result_doc

    def batch_render(self, kwargs):
        doc_list = []
        placeholder_names = [i.entity for i in self.get_placeholders()]
        pattern_specific_dictionary = {i: kwargs[i] for i in placeholder_names}

        instance_list_variable = list(itertools.product(*pattern_specific_dictionary.values()))

        for instance_variable in instance_list_variable:
            instance_mapping = dict(
                zip(pattern_specific_dictionary.keys(),
                    instance_variable))

            doc = self.render(instance_mapping)

            doc_list.append(doc)

        return doc_list

    def __hash__(self):
        return hash(tuple(self.text))

    def __eq__(self, other):
        return self.text == other.text

    def convert_to_md(self):
        text_with_annotation = copy.deepcopy(self.text)
        for span in self.span_set:
            start_token = text_with_annotation[span.start]
            text_with_annotation[span.start] = "<{}".format(start_token)

            end_token = text_with_annotation[span.end - 1]
            text_with_annotation[span.end - 1] = "{}>".format(end_token)

        return "".join(text_with_annotation)

    def add_doc(self, doc: Document):
        self.docs.append(doc)

    def get_docs(self) -> List[Document]:
        return self.docs
