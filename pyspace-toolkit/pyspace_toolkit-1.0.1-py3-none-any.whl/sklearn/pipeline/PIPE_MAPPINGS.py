# %%
import pyspace

# %%
import sklearn

# %%
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

# %%
from sklearn.decomposition import PCA, TruncatedSVD

# %%
from sklearn.svm import LinearSVC

# %%
from sklearn.cluster import AgglomerativeClustering

# %%
PIPE_MAPPINGS = {
    'pdseries': pyspace.sklearn.core.transformer.common_transformers.pdSeriesTransformer,
    'pdvalues': pyspace.sklearn.core.transformer.common_transformers.pdValuesTransformer,
    'npfloat64': pyspace.sklearn.core.transformer.common_transformers.npFloat64Transformer,
    'toarray': pyspace.sklearn.core.transformer.common_transformers.DenseTransformer,
    'identity': pyspace.sklearn.core.transformer.common_transformers.IdentityTransformer,
    
    'tokenize': pyspace.sklearn.core.transformer.text_transformers.TokenizerTransformer,
    'ontoken': pyspace.sklearn.core.transformer.text_transformers.TokenTransformer,
    'onsent': pyspace.sklearn.core.transformer.text_transformers.SentenceTransformer,
    
    'wordvector': pyspace.sklearn.core.transformer.text_transformers.WordvectorTransformer,
    'discrete': pyspace.sklearn.core.transformer.text_transformers.WordvectorDiscreteTransformer,

    'onehot': OneHotEncoder,
    'tfidf': TfidfVectorizer,
    'tf': CountVectorizer,
    'mtfidf': pyspace.sklearn.core.transformer.text_transformers.SupervisedMergedTfidfTransformer,
    'cdfidf': pyspace.sklearn.core.transformer.text_transformers.SupervisedCdfidfTransformer,
    
    'pca': PCA,
    'tsvd': TruncatedSVD,
    
    'lsvm': LinearSVC,
    'lsvm+': pyspace.sklearn.core.model.custom_classifier.LinearSVCExtended,
    
    'agg+': pyspace.sklearn.core.model.custom_cluster.AgglomerativeClusteringThreshold,
    'agg': AgglomerativeClustering,
    
    'hierarchic': pyspace.sklearn.core.model.custom_classifier.HierarchicalClassifierExtended,
}

# %%
try:
    import lightgbm
    PIPE_MAPPINGS['lgbm'] = lightgbm.LGBMClassifier
except:
    pass

# %%
try:
    import xgboost
    PIPE_MAPPINGS['xgb'] = xgboost.XGBClassifier
except:
    pass
