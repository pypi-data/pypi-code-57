import random as r
from . import char
from . import date
from . import num
from . import price
from . import word

def mock(schema_json=None, count=10):
    result = []
    for i in range(count):
        data = {}
        for key, value in schema_json.items():
            if value == "char":
                data[key] = char.mock()
            if value == "date":
                data[key] = str(date.mock())
            elif value == "num":
                data[key] = num.mock()
            elif value == "price":
                data[key] = price.mock()
            else:
                normalize_key = key.replace("_","")
                if "username" in normalize_key:
                    data[key] = word.mock(no_of_word=1)
                elif "name" in normalize_key:
                    data[key] = word.mock(no_of_word=r.choice([2,3]),upper_first_all=True)
                elif "gender" in normalize_key:
                    data[key] = word.mock_gender(upper_first=True)
                elif "phone" in normalize_key:
                    data[key] = word.mock_phone()
                elif "mail" in normalize_key:
                    data[key] = word.mock_email()
                elif "ipaddr" in normalize_key:
                    data[key] = word.mock_ip_address()
                else:
                    data[key] = word.mock(upper_first=True)
        
        result.append(data)

    return result