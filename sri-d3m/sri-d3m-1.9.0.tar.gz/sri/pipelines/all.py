# Information on all pipelines and which primitives are used.

import json

from sri.autoflow.static_ensembler import StaticEnsembler
from sri.autoflow.simple_column_parser import SimpleColumnParser
from sri.baseline.mean import MeanBaseline
from sri.pipelines.baseline_mean import MeanBaselinePipeline
from sri.pipelines.conditioner import ConditionerPipeline
from sri.pipelines.dataset_text_reader import DatasetTextReaderPipeline
from sri.pipelines.general_relational import GeneralRelationalPipeline
from sri.pipelines.simple_column_parser import SimpleColumnParserPipeline
from sri.pipelines.vertex_classification import VertexClassificationPipeline
from sri.psl.general_relational import GeneralRelational
from sri.psl.vertex_classification import VertexClassification

# The pipelines for these primitives will only be returned from get_pipelines() if
# the test argument is set to True.
TEST_ONLY_PRIMITIVES = {
    'd3m.primitives.learner.mean_baseline.MeanBaseline',
}

PIPELINES_BY_PRIMITIVE = {
    'd3m.primitives.learner.model.GeneralRelational': [
        GeneralRelationalPipeline,
    ],
    'd3m.primitives.data_transformation.conditioner.Conditioner': [
        ConditionerPipeline,
    ],
    'd3m.primitives.data_preprocessing.dataset_text_reader.DatasetTextReader': [
        DatasetTextReaderPipeline,
    ],
    'd3m.primitives.data_transformation.simple_column_parser.DataFrameCommon': [
        SimpleColumnParserPipeline,
    ],
    'd3m.primitives.learner.mean_baseline.MeanBaseline': [
        MeanBaselinePipeline,
    ],
    # Disable until the graph extraction (from a dataset) infrastructure exists.
    # 'd3m.primitives.vertex_classification.model.SRI': [
    #     VertexClassificationPipeline,
    # ],
}

def get_primitives():
    return PIPELINES_BY_PRIMITIVE.keys()

def get_pipelines(primitive = None, test = False):
    if (primitive is not None):
        if (primitive not in PIPELINES_BY_PRIMITIVE):
            return []
        return PIPELINES_BY_PRIMITIVE[primitive]

    pipelines = set()
    for (primitive, primitive_pipelines) in PIPELINES_BY_PRIMITIVE.items():
        if (not test and primitive in TEST_ONLY_PRIMITIVES):
            continue

        pipelines = pipelines | set(primitive_pipelines)

    return pipelines

if __name__ == '__main__':
    output = PIPELINES_BY_PRIMITIVE.copy()
    for key in output:
        output[key] = [pipeline.__name__ for pipeline in output[key]]
    print(json.dumps(output, indent = 4))
