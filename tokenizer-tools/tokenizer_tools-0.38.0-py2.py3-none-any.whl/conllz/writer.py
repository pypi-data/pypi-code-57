import copy
import json
import uuid
from typing import List

from tokenizer_tools.conllz.sentence import SentenceX


def write_conllx(sentence_list: List[SentenceX], output_fd):
    for sentence in sentence_list:
        sentence_id = sentence.id

        for index, row in enumerate(sentence.read_as_row()):
            if index == 0:  # only write at head
                sentence_id = sentence_id if sentence_id else str(uuid.uuid4())
                meta = copy.deepcopy(sentence.meta)
                meta.update({"id": sentence_id})

                # remove None-valued meta
                meta = {k: v for k, v in meta.items() if v is not None}

                meta_string = json.dumps(meta, ensure_ascii=False)
                output_fd.write("{}\n".format("\t".join(["#", meta_string])))

            output_fd.write("{}".format("\t".join(row)))
            output_fd.write("\n")

        output_fd.write("\n")
