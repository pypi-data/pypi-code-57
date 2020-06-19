from model_bakery import baker


def test_str_method():
    address = baker.prepare('subjects.Address',
                            street='Ernst-Thälmann-Str. 1',
                            city='Neuenhagen bei Berlin',
                            zip_code='15366',
                            country='DE')
    assert str(address) == 'Ernst-Thälmann-Str. 1, 15366, Neuenhagen bei Berlin, DE'
