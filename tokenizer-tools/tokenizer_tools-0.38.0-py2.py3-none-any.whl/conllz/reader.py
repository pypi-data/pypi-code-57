import io
import json
from typing import Generator, List, Tuple

from tokenizer_tools.conllz.sentence import SentenceX

Block = List[Tuple[int, str]]


def line_generator(fd) -> Generator[str, None, None]:
    for raw_line in fd:
        # remove newline
        line = raw_line.rstrip("\n\r")
        yield line


def block_generator(lines) -> Generator[Block, None, None]:
    block = []
    for line_num, line_str in enumerate(lines, start=1):
        if not line_str:  # empty line
            yield block

            # reset
            block = []

            # skip this line
            continue

        block.append((line_num, line_str))

    # last block
    if block:
        yield block


def load_conllx(fd: io.TextIOWrapper) -> Generator[SentenceX, None, None]:
    lines = line_generator(fd)
    blocks = block_generator(lines)
    for block in blocks:
        yield parse_block_to_sentence(block)


def parse_block_to_sentence(block: Block) -> SentenceX:
    sentence = SentenceX()
    for index, (line_num, raw_line) in enumerate(block):
        if index == 0:
            meta_string = raw_line.strip("#\t\n ")
            try:
                meta_data = json.loads(meta_string)
            except json.decoder.JSONDecodeError as e:
                raise ValueError("{}. At line {}: {}".format(e, line_num, raw_line))

            sentence.id = meta_data.pop("id")
            sentence.meta = meta_data

            continue  # read head is done

        # line = raw_line.strip()
        item = raw_line.split("\t")

        if not raw_line or not item:
            # skip
            continue

        sentence.write_as_row(item)

    return sentence


def read_conllx(input_fd) -> List[SentenceX]:
    return list(load_conllx(input_fd))


def read_conllx_from_string(str_content) -> List[SentenceX]:
    fd = io.StringIO(str_content)
    return list(load_conllx(fd))
