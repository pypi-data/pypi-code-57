import json
import os
from typing import Generator

from bavard.qa.bert.raw_input import RawInput


class SquadDataLoader:
    @staticmethod
    def read_examples(squad_path: str,
                      is_training: bool) -> Generator[RawInput, None, None]:

        with open(os.path.join(squad_path), encoding='utf-8') as f:
            data = json.load(f)

            items = data['data']

            for i, item in enumerate(items):
                for paragraph in item['paragraphs']:
                    context = paragraph['context']

                    for qas in paragraph['qas']:
                        qas_id = qas['id']
                        question = qas['question']
                        is_impossible = qas['is_impossible']

                        answers = qas['answers']

                        answer_text = ''
                        answer_start = 0

                        if not is_impossible:
                            if is_training:
                                assert len(answers) == 1
                            ans = answers[0]
                            answer_start = ans['answer_start']
                            answer_text = ans['text']

                        yield RawInput(question=question,
                                       context=context,
                                       is_training=is_training,
                                       id=qas_id,
                                       answer=answer_text,
                                       answer_start_char_idx=answer_start,
                                       is_impossible=is_impossible)
