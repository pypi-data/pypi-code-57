from bytegain.custom.model_data.row_handler import RowHandler
from bytegain.custom.model_data.bucket import ValueBucket
from bytegain.custom.model_data.extractor import RowExtractor
from bytegain.custom.cust.apartmentlist.al_multi_row_handler import ALMultiRowHandler


# # This WHERE is just for creating features.  For training data, see leads_from_redshift.
# WHERE =  """
# interest_created_at > timestamp '2016-01-01' and
# interest_created_at < timestamp '2016-08-01'
# """
# def _get_selector():
#       return read_from_db.Selector("apartmentlist.bytegain_leads", WHERE, "leased_at_notified_property", "interest_id")

"""
Creates a RowHandler for parsing AL data and handing to XGBoost.
"""


def create_multi_row_handler(feature_json):
    return ALMultiRowHandler(feature_json, label_bucket = ValueBucket("leased", RowExtractor("leased_at_notified_property"), has_null = False),
            id_extractor= RowExtractor("interest_id"))
