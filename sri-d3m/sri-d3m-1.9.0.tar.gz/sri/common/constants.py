import os

D3M_INDEX = 'd3mIndex'
CONFIDENCE_COLUMN = 'confidence'
D3M_TABLE_KEY = 'learningData'

SEMANTIC_TYPE_PK = 'https://metadata.datadrivendiscovery.org/types/PrimaryKey'
SEMANTIC_TYPE_TARGET = 'https://metadata.datadrivendiscovery.org/types/PredictedTarget'
SEMANTIC_TYPE_CONFIDENCE = 'https://metadata.datadrivendiscovery.org/types/Confidence'
SUGGESTED_TARGET_TYPE = 'https://metadata.datadrivendiscovery.org/types/SuggestedTarget'
TRUE_TARGET_TYPE = 'https://metadata.datadrivendiscovery.org/types/TrueTarget'
TARGET_TYPE = 'https://metadata.datadrivendiscovery.org/types/Target'
ATTRIBUTE_TYPE = 'https://metadata.datadrivendiscovery.org/types/Attribute'
GRAPH_TYPE = 'https://metadata.datadrivendiscovery.org/types/Graph'
EDGE_LIST_TYPE = 'https://metadata.datadrivendiscovery.org/types/EdgeList'
TABLE_TYPE = 'https://metadata.datadrivendiscovery.org/types/Table'
ENTRY_POINT_TYPE = 'https://metadata.datadrivendiscovery.org/types/DatasetEntryPoint'
UNIQUE_KEY_TYPE = 'https://metadata.datadrivendiscovery.org/types/UniqueKey'
EDGE_SOURCE_TYPE = 'https://metadata.datadrivendiscovery.org/types/EdgeSource'
EDGE_TARGET_TYPE = 'https://metadata.datadrivendiscovery.org/types/EdgeTarget'
PRIMARY_KEY_TYPE = 'https://metadata.datadrivendiscovery.org/types/PrimaryKey'
CONTROL_PARAM_TYPE = 'https://metadata.datadrivendiscovery.org/types/ControlParameter'
FILE_NAME_TYPE = 'https://metadata.datadrivendiscovery.org/types/FileName'

BOOLEAN_TYPE = 'http://schema.org/Boolean'
CATEGORICAL_TYPE = 'https://metadata.datadrivendiscovery.org/types/CategoricalData'
INTEGER_TYPE = 'http://schema.org/Integer'
FLOAT_TYPE = 'http://schema.org/Float'
FLOAT_VECTOR_TYPE = 'https://metadata.datadrivendiscovery.org/types/FloatVector'
DATE_TIME_TYPE = 'http://schema.org/DateTime'
TEXT_TYPE = 'http://schema.org/Text'

# PSL-related constants.

PSL_CLI_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'psl', 'cli'))
PSL_CLI_JAR = os.path.abspath(os.path.join(PSL_CLI_DIR, 'psl-cli-2.3.0-SNAPSHOT-b5698f08.jar'))
RUN_OUT_DIRNAME = 'psl-out'

DATA_DIR_SUB = '{data_dir}'

DEFAULT_MEMORY_PERCENT = 0.75

# Keys for properties on nodes and edges.
SOURCE_GRAPH_KEY = 'sourceGraph'
WEIGHT_KEY = 'weight'
EDGE_TYPE_KEY = 'edgeType'
OBSERVED_KEY = 'observed'
INFERRED_KEY = 'inferred'
TARGET_KEY = 'inferenceTarget'
SOURCE_KEY = 'source'
DEST_KEY = 'dest'
