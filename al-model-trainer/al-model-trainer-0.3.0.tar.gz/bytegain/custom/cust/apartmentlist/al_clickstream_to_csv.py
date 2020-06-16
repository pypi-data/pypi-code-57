import bytegain.custom.model_data.read_from_db as read_from_db
import bytegain.custom.model_data.feature_analysis as feature_analysis
import bytegain.custom.cust.apartmentlist.al_handler_from_features as al_handler_from_features
import csv

def get_selector():
    return read_from_db.Selector("interest_web_tracks_10", None, "leased_at_notified_property", "interest_id", "original_timestamp")

def create_csv_from_row_handler(filename, password = None, row_limit = None):
    selector = get_selector()
    row_handler = al_handler_from_features.create_multi_row_handler('web_tracks.json')
    read_from_db.generate_row_handler_stats(password, 'apartmentlist', selector, row_handler)
    data,labels,ids,rh  = read_from_db.create_datasets(password, 'apartmentlist', selector, row_handler, row_limit = row_limit)

    with open(filename, "w") as f:
        writer = csv.writer(f, delimiter='|')
        for event,label,id in zip(data, labels, ids):
            row = [id, int(label[0])]
            row.extend([",".join([str(e) for e in x]) for x in event])
            writer.writerow(row)

def run_feature_analysis(filename):
    data_info = feature_analysis.DataInfo('apartmentlist', get_selector(), None)
    features = feature_analysis.process_features(data_info)
    feature_analysis.save_features(filename, features)
    return features
