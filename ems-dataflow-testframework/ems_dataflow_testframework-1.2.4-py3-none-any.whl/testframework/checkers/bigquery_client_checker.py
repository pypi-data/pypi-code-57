import logging

from google.cloud import bigquery
from pytest import fixture


class BigQueryClientChecker:

    def __init__(self, bq_client: bigquery.Client, expected_data_sets: set):
        self.__bq_client = bq_client
        logging.info("Project is: {}".format(self.__bq_client.project))
        self.__expected_data_sets = expected_data_sets

    def check_datasets(self, create_if_missing: bool=False):
        set_of_existing_data_set_names = set([ds.dataset_id for ds in self.__bq_client.list_datasets()])
        logging.info("Current data sets [{} pieces]: {}".format(
            len(set_of_existing_data_set_names),
            set_of_existing_data_set_names))

        missing_datasets = [ds for ds in self.__expected_data_sets.difference(set_of_existing_data_set_names)]

        logging.debug("Missing data sets are: {}".format(missing_datasets))

        if create_if_missing:
            for dataset_name in missing_datasets:
                logging.info("creating dataset {}".format(dataset_name))
                dataset_ref = self.__bq_client.dataset(dataset_name)
                dataset = bigquery.Dataset(dataset_ref)
                dataset.location = "EU"
                self.__bq_client.create_dataset(dataset)

            set_of_existing_data_set_names = self.__expected_data_sets

        return self.__expected_data_sets.issubset(set_of_existing_data_set_names)


@fixture(scope="function")
def bq_client_checker(request):
    bq_client, data_sets_expected = request.param
    checker = BigQueryClientChecker(bq_client, data_sets_expected)
    return checker
