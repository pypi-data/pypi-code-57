from cytoolz.curried import assoc, compose
from genomoncology.parse.doctypes import DocType, __CHILD__, __TYPE__
from genomoncology.pipeline.transformers import register, name_mapping


def parse_score(value):
    try:
        if value:
            value = float(value)
        return value
    except ValueError:
        return None


def score_is_not_null(x):
    return x.get("score__float") is not None


NAME_MAPPING = {"gene": "gene", "score__float": "pLI"}

register(
    input_type=DocType.TSV,
    output_type=DocType.PLI,
    transformer=compose(
        lambda x: None if not score_is_not_null(x) else x,
        lambda x: assoc(
            x, "score__float", parse_score(x.get("score__float", ""))
        ),
        lambda x: assoc(x, __TYPE__, DocType.PLI.value),
        lambda x: assoc(x, "is_gene_annotation", True),
        name_mapping(NAME_MAPPING),
    ),
)

register(
    input_type=DocType.TSV,
    output_type=DocType.PLI,
    transformer=compose(lambda x: assoc(x, __CHILD__, DocType.PLI.value)),
    is_header=True,
)
