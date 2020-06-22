import copy
from typing import Tuple

from tokenizer_tools.conllz.sentence import Sentence, SentenceX
from tokenizer_tools.tagset.NER.BILUO import BILUOSequenceEncoderDecoder
from tokenizer_tools.tagset.offset.document import Document
from tokenizer_tools.tagset.exceptions import TagSetDecodeError

decoder = BILUOSequenceEncoderDecoder()


def conllx_to_offset(
    sentence_data: SentenceX, raise_exception=False, attr_index=0
) -> Tuple[Document, bool]:

    input_text = sentence_data.word_lines
    tags_seq = sentence_data.get_attribute_by_index(attr_index)

    failed = False
    meta = copy.deepcopy(sentence_data.meta)

    try:
        seq = decoder.to_offset(
            tags_seq,
            input_text,
            label=meta.pop("label", None),
            id=sentence_data.id,
            **meta
        )
    except TagSetDecodeError as e:
        if not raise_exception:
            # invalid tag sequence will raise exception
            # so return a empty result
            seq = Document(input_text)
            failed = True
        else:
            raise

    return seq, failed
