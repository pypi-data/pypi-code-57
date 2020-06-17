from d3m.metadata import base as meta_base
from d3m.metadata import pipeline as meta_pipeline
from d3m.primitives.data_transformation.column_parser import Common as ColumnParser
from d3m.primitives.data_transformation.construct_predictions import Common as ConstrucutPredictions
from d3m.primitives.data_transformation.dataset_to_dataframe import Common as DatasetToDataframe
from d3m.primitives.data_transformation.extract_columns_by_structural_types import Common as ExtractColumnsByStructuralTypes
from d3m.primitives.schema_discovery.profiler import Common as Profiler

import sri.pipelines.datasets as datasets
from sri.pipelines.base import BasePipeline
from sri.psl.general_relational import GeneralRelational

# These datasets are irregular (outside the normal slow/block list).
SKIP_DATASETS = set([
])

class GeneralRelationalPipeline(BasePipeline):
    # CHALLENGE_PROBLEMS = ['LL0_acled_reduced', '38_sick', '56_sunspots_monthly', 'LL1_TXT_CLS_airline_opinion']
    CHALLENGE_PROBLEMS = ['185_baseball_MIN_METADATA']

    def __init__(self):
        problems = set(datasets.get_dataset_names()) - SKIP_DATASETS
        super().__init__(problems, True)

    def _gen_pipeline(self):
        pipeline = meta_pipeline.Pipeline()
        pipeline.add_input(name = 'inputs')

        # Get the dataset as a dataframe.
        step_0 = meta_pipeline.PrimitiveStep(primitive_description = DatasetToDataframe.metadata.query())
        step_0.add_argument(
                name = 'inputs',
                argument_type = meta_base.ArgumentType.CONTAINER,
                data_reference = 'inputs.0'
        )
        step_0.add_output('produce')
        pipeline.add_step(step_0)

        # Infer types and roles for the columns.
        step_1 = meta_pipeline.PrimitiveStep(primitive_description = Profiler.metadata.query())
        step_1.add_argument(
                name = 'inputs',
                argument_type = meta_base.ArgumentType.CONTAINER,
                data_reference = 'steps.0.produce'
        )
        step_1.add_output('produce')
        pipeline.add_step(step_1)

        # Remove columns that do not have a structural type.
        step_2 = meta_pipeline.PrimitiveStep(primitive_description = ExtractColumnsByStructuralTypes.metadata.query())
        step_2.add_argument(
                name = 'inputs',
                argument_type = meta_base.ArgumentType.CONTAINER,
                data_reference = 'steps.1.produce'
        )
        step_2.add_output('produce')
        pipeline.add_step(step_2)

        # Parse column values into their inferred types.
        step_3 = meta_pipeline.PrimitiveStep(primitive_description = ColumnParser.metadata.query())
        step_3.add_argument(
                name = 'inputs',
                argument_type = meta_base.ArgumentType.CONTAINER,
                data_reference = 'steps.2.produce'
        )
        step_3.add_output('produce')
        pipeline.add_step(step_3)

        # Run our actual primitive.
        step_4 = meta_pipeline.PrimitiveStep(primitive_description = GeneralRelational.metadata.query())
        step_4.add_argument(
                name = 'inputs',
                argument_type = meta_base.ArgumentType.CONTAINER,
                data_reference = 'steps.3.produce'
        )
        step_4.add_argument(
                name = 'outputs',
                argument_type = meta_base.ArgumentType.CONTAINER,
                data_reference = 'steps.3.produce'
        )
        step_4.add_output('produce')
        pipeline.add_step(step_4)

        # Format the predictions properly.
        # Additionally, pass in an annotated (typed) frame so this primitive can infer the correct columns.
        step_5 = meta_pipeline.PrimitiveStep(primitive_description = ConstrucutPredictions.metadata.query())
        step_5.add_argument(
                name = 'inputs',
                argument_type = meta_base.ArgumentType.CONTAINER,
                data_reference = 'steps.4.produce'
        )
        step_5.add_argument(
                name = 'reference',
                argument_type = meta_base.ArgumentType.CONTAINER,
                data_reference = 'steps.3.produce'
        )
        step_5.add_output('produce')
        pipeline.add_step(step_5)

        # Adding output step to the pipeline
        pipeline.add_output(name = 'results', data_reference = 'steps.5.produce')

        return pipeline
