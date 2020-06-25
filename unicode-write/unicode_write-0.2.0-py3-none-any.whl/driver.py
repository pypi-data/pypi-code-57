import os
import pickle
import argparse
import unicodedata
import pyperclip
from prompt_toolkit import prompt
from inverted_index.prompt import SearchCompleter
from inverted_index.inverted_index import InvertedIndex, LevenshteinRankingInvertedIndex
from unicode_write.utils import get_unicode_mapping, stem, get_emojis, merge_mappings, UnicodeWriter, get_cache_path


def main():
    cache = get_cache_path()
    if os.path.exists(cache):
        with open(cache, "rb") as f:
            writer, ii = pickle.load(f)
    else:
        names = get_unicode_mapping()
        emojis = get_emojis()
        mapping = merge_mappings(names, emojis)
        writer = UnicodeWriter(mapping)
        ii = LevenshteinRankingInvertedIndex(preprocess=stem)
        ii.index(mapping.keys())
        with open(cache, "wb") as wf:
            pickle.dump([writer, ii], wf)

    text = prompt("> ", completer=SearchCompleter(ii), complete_while_typing=False)
    print(writer(text))
    pyperclip.copy(writer(text))


if __name__ == "__main__":
    main()
