import pytest

from dli.client.exceptions import CatalogueEntityNotFoundException


@pytest.mark.integration
def test_files_method_in_dataset_with_qa_env(csv_dataset):
    for x in csv_dataset.instances.all():
        print('csv_dataset', x)
    c = csv_dataset.instances.latest()
    c_files = c.files()
    assert c_files is not None


@pytest.mark.integration
@pytest.mark.xfail
def test_dataset_partitions(csv_dataset):
    partitions = csv_dataset._partitions()
    assert set(partitions['as_of_date']) == set(
        '2020-01-27', '2020-01-28', '2020-01-29', '2020-01-30', '2020-01-31'
    )
    assert partitions['location'] == ['us']
    assert partitions['as_of_date'] == ['2000-01-01']


@pytest.mark.integration
@pytest.mark.xfail
def test_files_method_in_empty_dataset_with_qa_env(empty_dataset):
    with pytest.raises(CatalogueEntityNotFoundException):
        empty_dataset.instances.latest().files()


@pytest.mark.integration
@pytest.mark.xfail
def test_empty_package_with_qa_env(package, client):
    client.get_package(name=package.name)
