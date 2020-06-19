from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from .base_socket import SocketBase

class AutoFeatureSocket(SocketBase):
    def __init__(self, with_default):
        super().__init__(with_default)
    
        self.numeric_socket = AutoNumericFeatureSocket(with_default)
        self.categorical_socket = AutoCategoricalFeatureSocket(with_default)
    
    def fit(self, X):
        self.num_cols, self.cat_cols = self._derive_column_types(X)
        
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', self.numeric_socket._plugs_to_pipe(), self.num_cols),
                ('cat', self.categorical_socket._plugs_to_pipe(), self.cat_cols)])
        
        self.pipe = Pipeline(steps=[('preprocessor', preprocessor)])
        self.pipe.fit(X)

    def transform(self, X):
        return self.pipe.transform(X)
    
    def _derive_column_types(self, X):
        col_types = X.infer_objects().dtypes
        numeric_features = []
        categorical_features = []
        
        for index, value in col_types.items():
            if value == 'object':
                categorical_features.append(index)
            else:
                numeric_features.append(index)
        
        return numeric_features, categorical_features
        

class AutoNumericFeatureSocket(SocketBase):
    def __init__(self, with_default):
        super().__init__(with_default)

        if with_default:
            self.register(SimpleImputer(strategy='median'))
            self.register(StandardScaler())
    
class AutoCategoricalFeatureSocket(SocketBase):
    def __init__(self, with_default):
        super().__init__(with_default)

        if with_default:
            self.register(SimpleImputer(strategy='constant', fill_value='missing'))
            self.register(OneHotEncoder(handle_unknown='ignore'))