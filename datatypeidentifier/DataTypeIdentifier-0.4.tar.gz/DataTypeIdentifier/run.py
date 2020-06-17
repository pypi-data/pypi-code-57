# -*- coding: utf-8 -*-
from data_type_identifier_generator import DataTypeIdentifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import load_model
from sklearn.utils import shuffle
from os.path import join
from pandas import DataFrame, read_csv


"""
############################################
############# MAIN OBJECT ##################
############################################
"""
#Using LabelEncoder implied that we want to keep a certain order of modalities while we are encoding a variable. 
#Here we have no order but the target variable only has two modalities. So there's no problem using it.
#We could have also used OneHotEncoder instead.  
data_type_identifier = DataTypeIdentifier(LabelEncoder)


"""
############################################
######## DATA PREPROCESSING ################
############################################
"""
# 1-Loading data from two different sources
categorical_numerical_data  = read_csv(join("data","data.csv"), sep=",", index_col=False) 
features_transposed_2       = read_csv(join("data","CC_training.csv"), sep=",", index_col=False, encoding="-ISO8859-1")
target_variable_2           = read_csv(join("data","y.csv"), sep=",")

# 2-Separating our features from our target variable
features        = categorical_numerical_data.iloc[:,:-1]
target_variable = categorical_numerical_data.iloc[:,-1]

# 3-Transposing our feature data frame to implement a column type analysis
features_transposed = features.T

# 4-Keeping the initial data type of every single feature
features_transposed     = data_type_identifier.keep_initial_data_types(features_transposed)
features_transposed_2   = data_type_identifier.keep_initial_data_types(features_transposed_2)

# 5-Building our training set
features_and_target     = data_type_identifier.build_final_set(features_transposed, target_variable)
features_and_target_2   = data_type_identifier.build_final_set(features_transposed_2, target_variable_2)
X_train                 = concat((features_and_target["new_features"], features_and_target_2["new_features"]))
y_train                 = concat((features_and_target["target_variable_encoded"],features_and_target_2["target_variable_encoded"]))
mappings                = data_type_identifier.get_target_variable_class_mappings() # 0 for categorical and 1 for numerical when this model was built 

# 6-Shuffling our data
X_train , y_train = shuffle(X_train, y_train) 

"""
############################################
############## TRAINING ####################
############################################
"""
data_type_identifier_model=data_type_identifier.sigmoid_neuron(X=X_train,
                                                               y=y_train,
                                                               path=join("model_and_checkpoint","data_type_identifier.h5"), 
                                                               epoch=300, 
                                                               validation_split=0.1, 
                                                               batch_size=20)

"""
############################################
##############SAVING VARIABLES##############
############################################
"""
data_type_identifier.save_variables(join("saved_variables","mappings.pickle"), mappings)
data_type_identifier.save_variables(join("saved_variables","X_train.pickle"), X_train)
data_type_identifier.save_variables(join("saved_variables","y_train.pickle"), y_train) 


"""
############################################
################ TESTING ###################
############################################
"""
# 1-Loading important variables
mappings = data_type_identifier.load_variables(join("saved_variables","mappings.pickle"))

# 2-Loading the model and the test datasets
data_type_identifier_model = load_model(join("model_and_checkpoint","data_type_identifier.h5"))
X_test                     = read_csv(join("data","CC_training.csv"), sep=",", encoding="ISO-8859-1")
y_test                     = read_csv(join("data","y.csv"), sep=",")

# 3-Predictions on test set
new_test_set_predictions = data_type_identifier.predict(X_test, mappings, data_type_identifier_model)

# 4-Classification report
report = classification_report(y_true=y_test, y_pred=new_test_set_predictions, output_dict=True)
report = DataFrame(report).transpose()
report.to_csv(join("data","report.csv"))


