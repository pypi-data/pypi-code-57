from io import TextIOWrapper, BytesIO
from json import dumps, loads
from csv import reader as read_csv_file
from json.decoder import JSONDecodeError
from requests import get


class ZuoraExportQueryResult:

    def __init__(self, raw_data, key_formatter=None):
        self.raw_data = raw_data
        try:
            assert callable(key_formatter)
            self.key_formatter = key_formatter
        except AssertionError:
            self.key_formatter = None

    @staticmethod
    def __format_key_name(key):
        formatted_key = (
            key.replace(":", "")
            .replace(" ", "")
            .replace("#", "")
            .replace("/", "")
            .replace("_", "")
            .replace("-", "")
            .replace('AccountAccount', 'account')
            .replace('SubscriptionSubscription', 'subscription')
            .replace('RevenueScheduleRevenueSchedule', 'RevenueSchedule')
        )

        # TODO: add more formatting cases
        if len(formatted_key) > 1:
            out_key = formatted_key[0].lower() + formatted_key[1:]
            return out_key

        elif len(formatted_key) == 1:
            return formatted_key.lower()

    def __str__(self):
        return str(self.raw_data)

    @property
    def dicts(self):
        keys = None
        for row in self.csv_decoded:
            if keys is None:
                formatter_func = self.key_formatter if self.key_formatter is not None else self.__format_key_name
                keys = [formatter_func(key).strip() for key in row]

            else:
                udr = dict(zip(keys, row))
                yield udr

    @property
    def json_formatted(self):
        return dumps([*self.dicts], indent=4)

    @property
    def csv_decoded(self):
        with TextIOWrapper(BytesIO(bytes(self.raw_data)), encoding='utf-8', newline='\r\n') as csv_file:
            return read_csv_file(csv_file, delimiter=',', quotechar='"')


class ZuoraResponse:
    def __init__(self, response):
        """

        :type response: requests.Response
        """
        self.raw_data = response.content
        try:
            self.as_dict = response.json()
            self.is_json_response = True
        except JSONDecodeError:
            self.is_json_response = False


class ZuoraQueryJobResponse:
    def __init__(self, query_job_id=None, output_format='JSON', custom_separator=None, items_num=0, response_url=None):
        self.query_job_id = query_job_id
        self.number_of_items = items_num
        self.raw_data = get(response_url).content if response_url is not None and items_num > 0 else None
        self.output_format = output_format
        self.custom_separator = custom_separator

    @property
    def response_items(self):
        if self.number_of_items > 0:
            with TextIOWrapper(BytesIO(bytes(self.raw_data)), encoding='utf-8', newline='\n') as response_file:

                if self.output_format == 'JSON':
                    for row in response_file:
                        yield loads(row.replace('\r', ''))

                else:
                    delimiters = {'CSV': ',',
                                  'TSV': '\t',
                                  'DSV': self.custom_separator}

                    data_set = read_csv_file(response_file, delimiter=delimiters[self.output_format], quotechar='"')
                    keys = None
                    for row in data_set:
                        if keys is None:
                            keys = row
                        else:
                            yield dict(zip(keys, row))

    def __str__(self):
        if self.raw_data is not None:
            return self.raw_data.decode(encoding='utf-8')
        else:
            return self.raw_data
