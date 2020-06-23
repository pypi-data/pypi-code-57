from swap.api.clients import UBLClient
from swap.api.parsers import InputDatasetsResponseParser
from swap.common.config import Settings

client = UBLClient()


class Dataset:
    def __init__(self, input_dataset):
        self.name = input_dataset.name
        self.input_dataset = input_dataset
        self.dataset_type = 'GCS'
        self.url = f'gs://{Settings.BUCKET}/{input_dataset.name}'


class CDFDataset:
    def __init__(self, dataset_id, survey_id="N/A"):
        if survey_id != "N/A":
            self.url = f'cdf://{survey_id}/{dataset_id}'
        else:
            self.url = f'cdf://{dataset_id}'
        self.name = dataset_id
        self.survey_id = survey_id
        self.dataset_id = dataset_id
        self.dataset_type = 'CDF'


def list_all():
    raw_result = client.get_input_datasets()
    parser = InputDatasetsResponseParser()
    input_datasets_response = parser.parse(raw_result).items
    output = []

    for input_dataset in input_datasets_response:
        dataset = Dataset(input_dataset=input_dataset)
        output.append(dataset)

    return output


def select(name):
    datasets = list_all()

    for dataset in datasets:
        if dataset.name == name:
            return dataset

    return None
