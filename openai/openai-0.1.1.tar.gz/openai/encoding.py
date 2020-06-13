from functools import lru_cache


@lru_cache()
def get(name):
    # Slow import
    from transformers.tokenization_gpt2 import GPT2TokenizerFast as GPT2Tokenizer

    if name == "byte-pair-encoding-v0":
        encoding = GPT2Tokenizer.from_pretrained("gpt2-xl")
        # Need to set or else we get a warning here
        encoding.pad_token = encoding.special_tokens_map["eos_token"]
        # HuggingFace's implementation tokenizes <|endoftext|> to a single token
        eot_token, = encoding.encode(encoding.special_tokens_map["eos_token"])
        encoding.eot_token = eot_token
        return encoding
    else:
        raise ValueError(
            f"This version of the 'openai' package does not support this encoding: {name}. (HINT: you may need to update your 'openai' pip package.)"
        )
