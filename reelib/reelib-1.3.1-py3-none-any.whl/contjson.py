import json


def load_from_file(filename, encode_format="utf-8"):
    """ファイルからJSONとしてロード"""

    return json.load(open(filename, "r", encoding=encode_format))


def save_to_file(json_obj, filename, indent=4, encode_format="utf-8"):
    """JSONをファイルへ保存"""

    json.dump(
        json_obj,
        open(filename, "w", encoding=encode_format),
        indent=indent,
        ensure_ascii=False,
    )


def print_json(json_obj, indent=4):
    """JSONを整形して表示"""

    print(json.dumps(json_obj, indent=indent, ensure_ascii=False))


def json_from_str(text):
    """str型からJSONへ変換"""

    return json.loads(text)


def json_to_str(json_obj):
    """JSONをstr型へ変換"""

    return json.dumps(json_obj, separators=(",", ":"), ensure_ascii=False)
