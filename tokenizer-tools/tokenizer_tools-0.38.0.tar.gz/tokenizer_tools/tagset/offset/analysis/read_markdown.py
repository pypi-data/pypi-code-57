import functools
import re
from typing import List
from urllib.parse import unquote

from tokenizer_tools.tagset.offset.document import Document
from tokenizer_tools.tagset.offset.analysis.document_pattern import DocumentPattern
from tokenizer_tools.tagset.offset.analysis.entity_placeholder import EntityPlaceholder
from tokenizer_tools.tagset.offset.span import Span
from tokenizer_tools.tagset.offset.span_set import SpanSet

# pytype: disable=import-error
from mistletoe import Document as CommonMarkDocument
from mistletoe.block_token import Heading, List as BlockList, ListItem, Paragraph
from mistletoe.span_token import RawText, Link, SpanToken, _token_types
# pytype: enable=import-error


class EntityPlaceholderToken(SpanToken):
    parse_group = 1
    parse_inner = False
    precedence = 5
    pattern = re.compile(r"\< *(\w+?) *\>")

    def __init__(self, match):
        self.target = match.group(1)


# registry for recognize <xx> tag
_token_types.insert(6, EntityPlaceholderToken)


def create_doc(
    token_list: List[str], span_info_list: List[dict], placeholder_list, **kwargs
) -> Document:
    # span_info_list and placeholder_list only one
    if len(placeholder_list) == 0:
        document = Document(token_list)

        for k, v in kwargs.items():
            setattr(document, k, v)

        # 构建实体集合
        span_list = [
            Span(start=i["start"], end=i["end"], entity=i["type"])
            for i in span_info_list
        ]

        document.entities = SpanSet(span_list)

        return document
    else:
        doc_pattern = DocumentPattern(token_list)

        for k, v in kwargs.items():
            setattr(doc_pattern, k, v)

        # 构建实体集合
        span_list = [
            EntityPlaceholder(start=i["start"], end=i["end"], entity=i["type"])
            for i in placeholder_list
        ]

        doc_pattern.entities = SpanSet(span_list)

        return doc_pattern


def read_markdown(data: str) -> List[Document]:
    doc = CommonMarkDocument(data)

    doc_list = []

    current_intent = None
    for top_item in doc.children:
        if isinstance(top_item, Heading):  # this is a head
            # assert top_item.level == 1
            current_intent = top_item.content
        elif isinstance(top_item, BlockList):  # this is ner list
            for sub_item in top_item.children:  # sub item in list
                assert isinstance(sub_item, ListItem)
                assert sub_item.leader == "*"

                token_list = []
                span_list = []
                placeholder_list = []

                for element in sub_item.children:
                    assert isinstance(element, Paragraph)
                    for span_set in element.children:
                        if isinstance(span_set, RawText):  # plain text
                            partial_token_list = list(span_set.content)
                            token_list.extend(partial_token_list)

                        elif isinstance(span_set, Link):
                            entity_type = span_set.target

                            assert len(span_set.children) == 1

                            entity_value = span_set.children[0].content

                            partial_token_list = entity_value.split()

                            start_index = len(token_list)

                            span_list.append(
                                {
                                    "start": start_index,
                                    "end": len(token_list) + len(partial_token_list),
                                    "type": entity_type,
                                }
                            )

                            token_list.extend(partial_token_list)

                        elif isinstance(span_set, EntityPlaceholderToken):
                            entity_placeholder = span_set.target

                            placeholder_list.append(
                                {
                                    "start": len(token_list),
                                    "end": len(token_list) + 1,
                                    "type": entity_placeholder,
                                }
                            )

                            token_list.extend([entity_placeholder])

                doc = create_doc(
                    token_list,
                    span_list,
                    placeholder_list=placeholder_list,
                    intent=current_intent,
                )

                doc_list.append(doc)

    return doc_list
