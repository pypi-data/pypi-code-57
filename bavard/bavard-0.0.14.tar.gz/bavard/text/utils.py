import collections
import logging
import unicodedata
from typing import List


def is_whitespace(char: str):
    """Checks whether `char` is a whitespace character."""
    if char == " " or char == "\t" or char == "\n" or char == "\r":
        return True
    cat = unicodedata.category(char)
    if cat == "Zs":
        return True
    return False


def get_char_to_word_map(text: str) -> List[int]:
    words = []
    char_to_word_idx = []
    prev_is_whitespace = True

    for char in text:
        if is_whitespace(char):
            prev_is_whitespace = True
            char_to_word_idx.append(len(words))

        else:
            if prev_is_whitespace:
                words.append(char)
            else:
                words[-1] += char
            prev_is_whitespace = False
            char_to_word_idx.append(len(words) - 1)
    return char_to_word_idx


def improve_answer_span(words, input_start, input_end, tokenizer, orig_answer_text):
    tok_answer_text = " ".join(tokenizer.tokenize(orig_answer_text))

    for new_start in range(input_start, input_end + 1):
        for new_end in range(input_end, new_start - 1, -1):
            text_span = " ".join(words[new_start:(new_end + 1)])
            if text_span == tok_answer_text:
                logging.info("improved answer span")
                return new_start, new_end

    return input_start, input_end


SlidingWindow = collections.namedtuple("SlidingWindow", ["start", "window"])


def get_sliding_windows(arr: List, window_size: int, stride: int) -> List[SlidingWindow]:

    def sliding_windows_helper(arr, start):
        if len(arr) <= window_size:
            return [SlidingWindow(start=start, window=arr)]

        window = SlidingWindow(start=start, window=arr[:window_size])
        remaining = sliding_windows_helper(arr[stride:], start + stride)
        return [window, *remaining]

    return sliding_windows_helper(arr, 0)

