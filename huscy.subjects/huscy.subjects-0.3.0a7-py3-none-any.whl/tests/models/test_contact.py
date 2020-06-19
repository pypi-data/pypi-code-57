from model_bakery import baker


def test_str_method():
    contact = baker.prepare('subjects.Contact', display_name='Dr. Hans Wurst')
    assert str(contact) == 'Dr. Hans Wurst'
