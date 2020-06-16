import bytegain.custom.model_data.feature_analysis as feature_analysis


finance_features = feature_analysis.read_features('al_finance_v1.0.0')
interest_features = feature_analysis.read_features('interest_created_1h_v1.1.0')

interest_feature_dict ={}
for feature in interest_features:
    interest_feature_dict[feature._column] = feature

for feature in finance_features:
    if feature._column not in interest_feature_dict:
        print("Missing feature: %s" % feature._column)
        continue

    interest_feature = interest_feature_dict[feature._column]
    print("\n\nFeature: %s"  % feature._column)
    for i in range(len(feature.top_values())):
        if i >= len(interest_feature.top_values()):
            break
        print("%s %s" % (feature.top_values()[i], interest_feature.top_values()[i]))
