import copy
from typing import List

from tokenizer_tools.tagset.offset.document_compare_ways import DocumentCompareWays
from tokenizer_tools.tagset.offset.sequence import Sequence


class Document(Sequence):
    @property
    def intent(self):
        return self.extra_attr.get("intent")

    @intent.setter
    def intent(self, intent):
        self.extra_attr["intent"] = intent

    @property
    def function(self):
        return self.extra_attr.get("function")

    @function.setter
    def function(self, function):
        self.extra_attr["function"] = function

    @property
    def sub_function(self):
        return self.extra_attr.get("sub_function")

    @sub_function.setter
    def sub_function(self, sub_function):
        self.extra_attr["sub_function"] = sub_function

    @property
    def domain(self):
        return self.extra_attr.get("domain")

    @domain.setter
    def domain(self, domain):
        self.extra_attr["domain"] = domain

    @property
    def entities(self):
        return self.span_set

    @entities.setter
    def entities(self, entities):
        entities.bind(self)
        self.span_set = entities

    def set_compare_way(self, compare_way: DocumentCompareWays):
        self.set_compare_method(compare_way.value["eq"])
        self.set_hash_method(compare_way.value["hash"])

    def convert_to_md(self) -> str:
        text_list = copy.deepcopy(self.text)

        for span in self.entities:
            text_list[span.start] = "[" + text_list[span.start]
            text_list[span.end - 1] = text_list[span.end - 1] + "]({})".format(
                span.entity
            )

        return "".join(text_list)

    def __str__(self):
        return "<D: {domain}, F: {function}, S: {sub_function}, I: {intent}>    {body}".format(
            domain=self.domain,
            function=self.function,
            sub_function=self.sub_function,
            intent=self.intent,
            body=self.convert_to_md(),
        )

    def __deepcopy__(self, memodict={}) -> "Document":
        cls = self.__class__
        doc = cls(copy.deepcopy(self.text))

        attrs_need_be_copied = ["domain", "intent", "function", "sub_function"]

        for attr in attrs_need_be_copied:
            setattr(doc, attr, getattr(self, attr))

        doc.entities = copy.deepcopy(self.entities)

        return doc

    def compare_entities(self, other):
        return self.text == other.text and self.span_set == other.span_set

    def entity_biluo_tags(self) -> List[str]:
        # put import statement here for avoid circular import
        from tokenizer_tools.tagset.NER.BILUO import BILUOEncoderDecoder

        tags = ["O"] * len(self.text)

        for span in self.span_set:
            encoder = BILUOEncoderDecoder(span.entity)
            tags[span.start : span.end] = encoder.encode(span.value)

        return tags
