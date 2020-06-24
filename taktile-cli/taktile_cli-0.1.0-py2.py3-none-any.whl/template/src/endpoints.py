import joblib
import pandas as pd
from tktl import Tktl

# Instantiate Taktile client
tktl = Tktl()

# Load reference data
data_test = pd.read_parquet("assets/test.pqt")
label = "survived"
X_test = data_test.drop(columns=label)
y_test = data_test[label]

# Load model
model = joblib.load("assets/model.pkl")


# Define predict functions
@tktl.endpoint(kind="binary", X=X_test, y=y_test)
def binary(X):
    pred = model.predict_proba(X)[:, 1]
    return pred
