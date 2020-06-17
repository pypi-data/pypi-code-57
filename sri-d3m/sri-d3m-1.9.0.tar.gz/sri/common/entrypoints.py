ENTRYPOINTS = {
    'd3m.primitives': {
        # Patched Primitives
        # 'time_series_forecasting.vector_autoregression.VARfix': 'sri.autoflow.var_fix:VARfix',

        # SRI Primitives
        'data_transformation.conditioner.Conditioner': 'sri.autoflow.conditioner:Conditioner',
        'data_preprocessing.dataset_text_reader.DatasetTextReader': 'sri.autoflow.dataset_text_reader:DatasetTextReader',
        'data_transformation.conditioner.StaticEnsembler': 'sri.autoflow.static_ensembler:StaticEnsembler',
        'data_transformation.simple_column_parser.DataFrameCommon': 'sri.autoflow.simple_column_parser:SimpleColumnParser',
        # 'regression.maple.Maple': 'sri.interpretml.maple_wrap:Maple',

        # Eriq's Primitives
        'learner.model.GeneralRelational': 'sri.psl.general_relational:GeneralRelational',
        # Disabled until graph extraction infrastrucure exists
        # 'vertex_classification.model.SRI': 'sri.psl.vertex_classification:VertexClassification',

        # Brian Sandberg from DARPA asked that we suppress MBL to prevent misuse 11/13/2019.
        # The entrypoint will be exposed for internal testing, but the primitive JSON will not be generated.
        # 'learner.mean_baseline.MeanBaseline': 'sri.baseline.mean:MeanBaseline',
    }
}

def get_entrypoints_definition():
    all_entrypoints = {}

    for (top_level, entrypoints) in ENTRYPOINTS.items():
        points = []

        for (entrypoint, target) in entrypoints.items():
            points.append("%s = %s" % (entrypoint, target))

        all_entrypoints[top_level] = points

    return all_entrypoints

# Get all the entrypoints.
def main():
    for (top_level, entrypoints) in ENTRYPOINTS.items():
        for entrypoint in entrypoints:
            print("%s.%s" % (top_level, entrypoint))

if __name__ == '__main__':
    main()
