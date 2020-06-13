from functools import lru_cache
from transformers.tokenization_gpt2 import GPT2TokenizerFast as GPT2Tokenizer


@lru_cache()
def get(name="byte-pair-encoding-v0"):
    if name == "byte-pair-encoding-v0":
        return GPT2Tokenizer.from_pretrained("gpt2-xl")
    else:
        raise ValueError(
            f"This version of the 'openai' package does not support this encoding: {name}. (HINT: you may need to open your 'openai' pip package.)"
        )
