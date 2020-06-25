from flask import Flask, jsonify, request
from unicode_write.inverted_index import InvertedIndex, LevenshteinRankingInvertedIndex
from unicode_write.utils import get_unicode_mapping, stem, get_emojis, merge_mappings, UnicodeWriter, get_cache_path


names = get_unicode_mapping()
emojis = get_emojis()
mapping = merge_mappings(names, emojis)
writer = UnicodeWriter(mapping)
ii = LevenshteinRankingInvertedIndex(preprocess=stem)
ii.index(mapping.keys())

app = Flask(__name__)

@app.route("/search", methods={"POST"})
def search():
    query = request.json["query"]
    return jsonify(ii.search(query))


@app.route("/unicode", methods={"POST"})
def write():
    codepoint = request.json["codepoint"]
    return jsonify({"unicode": writer(codepoint)})
