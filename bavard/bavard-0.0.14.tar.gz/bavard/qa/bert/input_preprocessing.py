from typing import List

from official.nlp.bert.tokenization import FullTokenizer

from bavard.qa.bert.input_features import InputFeatures
from bavard.qa.bert.raw_input import RawInput
from bavard.text import utils


def raw_input_to_features(tokenizer: FullTokenizer,
                          raw_input: RawInput,
                          max_seq_len: int,
                          max_question_len: int,
                          stride: int,
                          is_training: bool) -> List[InputFeatures]:
    question_tokens = tokenizer.tokenize(raw_input.question)

    # truncate question length
    question_tokens = question_tokens[:max_question_len]

    context_words = raw_input.context.split()
    context_tokens = []
    token_to_word_idx = []
    word_to_token_idx = []
    for (i, word) in enumerate(context_words):
        word_to_token_idx.append(len(context_tokens))
        word_tokens = tokenizer.tokenize(word)
        for token in word_tokens:
            token_to_word_idx.append(i)
            context_tokens.append(token)

    start_token_idx = None
    end_token_idx = None
    if is_training and raw_input.is_impossible:
        start_token_idx = -1
        end_token_idx = -1
    elif is_training:
        start_token_idx = word_to_token_idx[raw_input.answer_start_word_idx]

        if raw_input.answer_end_word_idx < len(context_words) - 1:
            end_token_idx = word_to_token_idx[raw_input.answer_end_word_idx + 1] - 1
        else:
            end_token_idx = len(context_tokens) - 1

        start_token_idx, end_token_idx = utils.improve_answer_span(
            context_words,
            start_token_idx,
            end_token_idx,
            tokenizer,
            raw_input.answer)

    # The -3 accounts for [CLS], [SEP] and [SEP]
    max_context_len = max_seq_len - len(question_tokens) - 3
    context_windows = utils.get_sliding_windows(context_tokens, max_context_len, stride)

    result = []
    for window in context_windows:
        input_features = context_window_to_features(tokenizer=tokenizer,
                                                    max_seq_len=max_seq_len,
                                                    token_to_word_idx=token_to_word_idx,
                                                    context_window=window,
                                                    question_tokens=question_tokens,
                                                    start_token_idx=start_token_idx,
                                                    end_token_idx=end_token_idx,
                                                    is_impossible=raw_input.is_impossible,
                                                    is_training=is_training)
        result.append(input_features)
    return result


def context_window_to_features(tokenizer: FullTokenizer,
                               max_seq_len: int,
                               token_to_word_idx: List[int],
                               context_window: utils.SlidingWindow,
                               question_tokens: List[str],
                               start_token_idx: int,
                               end_token_idx: int,
                               is_impossible: bool,
                               is_training: bool) -> InputFeatures:
    # 1. Get answer start/end indices for the window

    window_ans_start_idx = None
    window_ans_end_idx = None

    if is_training:
        window_ans_start_idx = 0
        window_ans_end_idx = 0

    if is_training and not is_impossible:
        window_start = context_window.start
        window_end = window_start + len(context_window.window) - 1

        if window_start <= start_token_idx and window_end >= end_token_idx:
            window_ans_start_idx = start_token_idx - window_start + 1
            window_ans_end_idx = end_token_idx - window_start + 1
        else:
            is_impossible = True

    window_token_to_word_idx = []
    for i in range(len(context_window.window)):
        token_i = i + context_window.start
        window_token_to_word_idx.append(token_to_word_idx[token_i])

    # 2. Get the input features

    input_context_tokens = ['[CLS]', *context_window.window, '[SEP]']
    input_question_tokens = [*question_tokens, '[SEP]']
    all_tokens = input_context_tokens + input_question_tokens

    context_ids = tokenizer.convert_tokens_to_ids(input_context_tokens)
    question_ids = tokenizer.convert_tokens_to_ids(input_question_tokens)

    input_ids = context_ids + question_ids
    input_mask = [1] * len(input_ids)
    segment_ids = [0] * len(context_ids) + [1] * len(question_ids)

    # Zero-pad up to the sequence length.
    while len(input_ids) < max_seq_len:
        input_ids.append(0)
        input_mask.append(0)
        segment_ids.append(0)

    assert len(input_ids) == max_seq_len
    assert len(input_mask) == max_seq_len
    assert len(segment_ids) == max_seq_len

    return InputFeatures(tokens=all_tokens,
                         token_to_word_idx=window_token_to_word_idx,
                         input_ids=input_ids,
                         input_mask=input_mask,
                         segment_ids=segment_ids,
                         ans_start_idx=window_ans_start_idx,
                         ans_end_idx=window_ans_end_idx,
                         is_impossible=is_impossible)
