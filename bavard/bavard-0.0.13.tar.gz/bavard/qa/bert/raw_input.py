from typing import Optional

from bavard.text import utils


class RawInput:
    def __init__(self,
                 question: str,
                 context: str,
                 is_training: bool,
                 id: Optional[str] = None,
                 answer: Optional[str] = None,
                 answer_start_char_idx: Optional[int] = None,
                 is_impossible: Optional[bool] = None):
        if is_training:
            assert is_impossible is not None
            if not is_impossible:
                assert answer is not None
                assert answer_start_char_idx is not None

        self.id = id
        self.question = question
        self.context = context
        self.is_training = is_training
        self.answer = answer
        self.answer_start_char_idx = answer_start_char_idx
        self.is_impossible = is_impossible

        if is_training:
            char_to_word_map = utils.get_char_to_word_map(context)
            self.answer_end_char_idx = answer_start_char_idx + len(answer) - 1

            self.answer_start_word_idx = char_to_word_map[answer_start_char_idx]
            self.answer_end_word_idx = char_to_word_map[self.answer_end_char_idx]

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        s = "---\n"
        if self.id is not None:
            s += f"id: {self.id}"
        s += f"question: {self.question}"
        s += f"\ncontext: {self.context}"
        s += f"\nis_training: {self.is_training}"
        s += f"\nis_impossible: {self.is_impossible}"

        if self.is_impossible is False:
            s += f"\nanswer: {self.answer}"
        return s
