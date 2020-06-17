from d3m.metadata import base as meta_base
from d3m.metadata import pipeline as meta_pipeline

from d3m.primitives.data_transformation.simple_column_parser import DataFrameCommon as SimpleColumnParser
from d3m.primitives.data_transformation.extract_columns_by_semantic_types import Common as ExtractColumnsBySemanticTypes
from d3m.primitives.data_transformation.dataset_to_dataframe import Common as DatasetToDataFrame
from d3m.primitives.data_transformation.conditioner import Conditioner
from d3m.primitives.data_preprocessing.dataset_text_reader import DatasetTextReader
# from d3m.primitives.classification.bernoulli_naive_bayes import SKlearn as BernoulliNaiveBayes
from d3m.primitives.classification.random_forest import SKlearn as RandomForest
from d3m.primitives.classification.decision_tree import SKlearn as DecisionTree

from d3m.primitives.data_transformation.construct_predictions import Common as ConstructPredictions
from d3m.primitives.schema_discovery.profiler import Common as SimpleProfiler

from d3m.primitives.data_transformation.conditioner import StaticEnsembler

from sri.common import constants
from sri.pipelines.base import BasePipeline

class StaticEnsemblerPipeline(BasePipeline):
    def __init__(self):
        super().__init__(('185_baseball_MIN_METADATA',), True)

    def _gen_pipeline(self):

        # Create pipeline 1 elements
        tr1 = DatasetTextReader(hyperparams={})
        todf1 = DatasetToDataFrame(hyperparams=dict(dataframe_resource=None))
        simple_profiler1 = SimpleProfiler(hyperparams={})
        scp1 = SimpleColumnParser(hyperparams={})
        ext_attr1 = ExtractColumnsBySemanticTypes(hyperparams=dict(semantic_types=(constants.ATTRIBUTE_TYPE,)))
        ext_targ1 = ExtractColumnsBySemanticTypes(hyperparams=dict(semantic_types=(constants.TRUE_TARGET_TYPE,)))
        cond1 = Conditioner(hyperparams=dict(ensure_numeric=True, maximum_expansion=30))
        random_forest = RandomForest(hyperparams={})

        # Create pipeline 1 instance
        random_forest_pipeline = meta_pipeline.Pipeline()
        random_forest_pipeline.add_input(name = 'inputs')

        # Add pipeline 1 steps
        node1 = self._add_pipeline_step(random_forest_pipeline, tr1, inputs="inputs.0")
        input_node1 = self._add_pipeline_step(random_forest_pipeline, todf1, inputs=node1)
        node1 = self._add_pipeline_step(random_forest_pipeline, simple_profiler1, inputs=input_node1)
        tnode1 = self._add_pipeline_step(random_forest_pipeline, ext_targ1, inputs=node1)
        node1 = self._add_pipeline_step(random_forest_pipeline, scp1, inputs=node1)
        node1 = self._add_pipeline_step(random_forest_pipeline, ext_attr1, inputs=node1)
        node1 = self._add_pipeline_step(random_forest_pipeline, cond1, inputs=node1)
        node1 = self._add_pipeline_step(random_forest_pipeline, random_forest, inputs=node1, outputs=tnode1)

        # Create pipeline 2 elements
        tr2 = DatasetTextReader(hyperparams={})
        todf2 = DatasetToDataFrame(hyperparams=dict(dataframe_resource=None))
        simple_profiler2 = SimpleProfiler(hyperparams={})
        scp2 = SimpleColumnParser(hyperparams={})
        ext_attr2 = ExtractColumnsBySemanticTypes(hyperparams=dict(semantic_types=(constants.ATTRIBUTE_TYPE,)))
        ext_targ2 = ExtractColumnsBySemanticTypes(hyperparams=dict(semantic_types=(constants.TRUE_TARGET_TYPE,)))
        cond2 = Conditioner(hyperparams=dict(ensure_numeric=True, maximum_expansion=30))
        decision_tree = DecisionTree(hyperparams={})

        # Create pipeline 2 instance
        decision_tree_pipeline = meta_pipeline.Pipeline()
        decision_tree_pipeline.add_input(name = 'inputs')

        # Add pipeline 2 steps
        node2 = self._add_pipeline_step(decision_tree_pipeline, tr2, inputs="inputs.0")
        input_node2 = self._add_pipeline_step(decision_tree_pipeline, todf2, inputs=node2)
        node2 = self._add_pipeline_step(decision_tree_pipeline, simple_profiler2, inputs=input_node2)
        tnode2 = self._add_pipeline_step(decision_tree_pipeline, ext_targ2, inputs=node2)
        node2 = self._add_pipeline_step(decision_tree_pipeline, scp2, inputs=node2)
        node2 = self._add_pipeline_step(decision_tree_pipeline, ext_attr2, inputs=node2)
        node2 = self._add_pipeline_step(decision_tree_pipeline, cond2, inputs=node2)
        node2 = self._add_pipeline_step(decision_tree_pipeline, decision_tree, inputs=node2, outputs=tnode2)

        # Create composite pipeline to contain the static ensembler
        pipeline = meta_pipeline.Pipeline()

        # Create Static Ensembler and the end of the pipeline
        construct_pred = ConstructPredictions(hyperparams={})
        se = StaticEnsembler(hyperparams={})

        self._add_pipeline_step(pipeline, se, inputs1=random_forest_pipeline, inputs2=decision_tree_pipeline)

        node1 = self._add_pipeline_step(pipeline, construct_pred, inputs=node1, reference=input_node1)

        # Add pipeline output
        pipeline.add_output(name="Results", data_reference=node1)

        return pipeline
