import os
import sys
import yaml
import json
import decimal

data_yaml_file = '/data.yml'


def get_data_yaml_dict(connection_type):
    try:
        sFile = os.path.abspath(sys.modules['__main__'].__file__)
    except:
        sFile = sys.executable
    return yaml.load(open(os.path.dirname(sFile) + data_yaml_file), Loader=yaml.FullLoader)[connection_type]


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)
