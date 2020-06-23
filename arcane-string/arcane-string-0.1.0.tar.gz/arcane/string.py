import re
import unicodedata


def strip_accents(text: str) -> str:
    return unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode("utf-8")


def to_pascal_case(text: str) -> str:
    if text == '':
        return ''
    text_stripped = strip_accents(text)
    return re.sub(
        r"(?:^|_|\W)+(.){0,1}",
        lambda m: m.group(1).upper() if m.group(1) is not None and re.match(r'[a-zA-Z0-9]', m.group(1)) else '',
        text_stripped
    )


def to_camel_case(text: str) -> str:
    pascal_text = to_pascal_case(text)
    if len(pascal_text) > 1:
        return pascal_text[0].lower() + pascal_text[1:]
    else:
        return pascal_text.lower()


def to_snake_case(text: str) -> str:
    camel_text = to_pascal_case(text)
    return re.sub(r"((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))", r"_\1", camel_text).lower()
